from flask import Blueprint

# Importando o Blueprint de itens
from .itens_controller import itens_bp

def init_app_routes_web(app):

    web_bp = Blueprint('web', __name__, url_prefix='/web')  
    # Rota para listar a home do web
    @web_bp.route('/')
    def index():
        return 'web'

    # Criando o Blueprint principal do web
    app.register_blueprint(web_bp)

    # Criando o Blueprint principal do web/alguma coisa
    app.register_blueprint(itens_bp)
