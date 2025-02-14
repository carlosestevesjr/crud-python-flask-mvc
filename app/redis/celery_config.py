from celery import Celery
from kombu import Queue

def make_celery():
    celery = Celery(
        "tasks",
        broker="redis://localhost:6379/0",
        backend="redis://localhost:6379/0",
        broker_connection_retry_on_startup=True, # here it is!!!
        include=["app.redis.tasks"]  # Atualiza o caminho do módulo
    )

    # Configura a fila personalizada "selenium_queue"
    celery.conf.task_queues = [
        Queue("selenium_queue")
    ]

    # Define "selenium_queue" como fila padrão
    celery.conf.task_default_queue = "selenium_queue"

    return celery

celery = make_celery()
