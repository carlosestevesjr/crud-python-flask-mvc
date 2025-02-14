from flask import Blueprint

# Importando o Blueprint de itens
from .itens_controller import api_itens_bp

def init_app_routes_api(app):

    api_bp = Blueprint('api', __name__, url_prefix='/api')  
    # Rota para listar a home do api
    @api_bp.route('/')
    def index():
        return 'api'

    # Criando o Blueprint principal do api
    app.register_blueprint(api_bp)

    # Criando o Blueprint principal do api/alguma coisa
    app.register_blueprint(api_itens_bp)
