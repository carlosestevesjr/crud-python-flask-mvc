# Importando e registrando os Blueprints
from flask import render_template, jsonify
from app.redis.celery_config import celery  # Importando a instância do Celery já configurada

import redis
# Cria o cliente Redis utilizando a mesma URL do broker do Celery
redis_client = redis.Redis.from_url(celery.conf.broker_url)

def init_app_routes(app):

    # Registra as rotas
    # Mova as importações para dentro da função para evitar importação circular
    from app.redis.tasks import process_task, fetch_article_titles
    tasks = {"process_task": process_task, "fetch_article_titles": fetch_article_titles}

    def get_queue_status():
        queue_info = {
            'pending': redis_client.llen('celery'),  # Número de tarefas pendentes na fila
            'active': [],
            'completed': []
        }
        
        inspector = celery.control.inspect()
        active_tasks = inspector.active() or {}
        # Busca as chaves que armazenam os resultados das tasks
        completed_tasks_keys = redis_client.keys('celery-task-meta-*')
        
        # Processa tarefas ativas
        for worker, tasks in active_tasks.items():
            for task in tasks:
                queue_info['active'].append({
                    'id': task['id'],
                    'name': task['name'],
                    'args': task['args'],
                    'kwargs': task['kwargs'],
                    'worker': worker
                })
        
        # Processa tarefas completadas: extrai o ID e usa celery.AsyncResult para obter o resultado completo
        for task_key in completed_tasks_keys:
            key_str = task_key.decode('utf-8')
            # Extraindo o ID da task removendo o prefixo 'celery-task-meta-'
            task_id = key_str.replace("celery-task-meta-", "")
            task_result = celery.AsyncResult(task_id)
            queue_info['completed'].append({
                'task_id': task_id,
                'status': task_result.status,
                'result': task_result.result,
                'traceback': task_result.traceback,
                'children': task_result.children,
                'date_done': getattr(task_result, "date_done", None)
            })
        
        return queue_info

    @app.route('/queue/status', methods=['GET'])
    def queue_status():
        status = get_queue_status()
        return jsonify(status)
    
    # Rota para enfileirar a tarefa de pegar os títulos
    @app.route('/enqueue_articles')
    def enqueue_articles():
        # Gera um task_id aleatório
        task = tasks['fetch_article_titles'].apply_async()  # Enfileira a tarefa
        return jsonify({"task_id": task.id})

    # Rota para enfileirar a tarefa de soma (exemplo simples)
    @app.route('/enqueue_sum')
    def enqueue_sum():
        task = tasks['process_task'].apply_async(args=[10, 20])  # Enfileira a tarefa
        return jsonify({"task_id": task.id})

    # Rota para obter o status da tarefa
    @app.route('/task/<task_id>', methods=['GET'])
    def get_task(task_id):
        # Recupera o resultado da task a partir do ID
        task_result = celery.AsyncResult(task_id)
        
        response = {
            "task_id": task_id,
            "status": task_result.status,
            "result": task_result.result,
            "traceback": task_result.traceback,
            "children": task_result.children,
            # Dependendo da versão/configuração, 'date_done' pode não estar disponível
            "date_done": getattr(task_result, "date_done", None)
        }
        
        return jsonify(response)

    # Rota principal para o dashboard
    @app.route('/')
    def dashboard():
        status = get_queue_status()
        return render_template('dashboard.html', queue_info=status)
    
    # Rota personalizada para erros 404
    @app.errorhandler(404)
    def not_found_error(error):
        return "Página não encontrada!", 404
    
     # Rota personalizada para erros 500
    @app.errorhandler(500)
    def internal_error(error):
        return "Ocorreu um erro interno no servidor!", 500
  
    # Importando todas as rotas abaixo web
    from app.controllers.web.web_controller import init_app_routes_web
    init_app_routes_web(app)

    # Importando todas as rotas abaixo api 
    from app.controllers.api.api_controller import init_app_routes_api
    init_app_routes_api(app)
