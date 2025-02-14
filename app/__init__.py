from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'random_secret_key'
    app.config.from_object('config.Config')

    # Configuração de debug a partir do .env
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', '0') == '1'

    # Inicializa o banco de dados
    db.init_app(app)

    # Registra as rotas
    from app.routes import init_app_routes
    # Importa os modelos aqui para evitar erros de importação
    init_app_routes(app)

    CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)

    return app
