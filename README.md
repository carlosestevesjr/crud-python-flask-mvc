#Comandos básicos do projeto

## criar ambiente
python3 -m venv venv

## ativar ambiente Linux MacOs
source ./venv/bin/activate

## ativar ambiente Windows
myenv\Scripts\activate

## nova aba do terminal start fila
celery -A app.redis.tasks worker --loglevel=info --concurrency=1 -Q selenium_queue

## instalar dependências
pip3 install -r requirements.txt 

## rodar
python3 run.py 
