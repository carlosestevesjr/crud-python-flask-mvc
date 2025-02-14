from flask import Blueprint, request, jsonify
from app import db
from app.models.Item import Item

# Criando o Blueprint para itens
api_itens_bp = Blueprint('api_itens', __name__, url_prefix='/api/itens')

# Rota para listar os itens
@api_itens_bp.route('/')
def index():
    items_ = Item.query.all()
    return jsonify(items_)

# Rota para criar um item
@api_itens_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        new_item = Item(name=name, description=description)
        db.session.add(new_item)
        db.session.commit()
        return "Post Create"
    return "Get Create"

# Rota para atualizar um item
@api_itens_bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    item = Item.query.get_or_404(id)
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        db.session.commit()
        return "Post Update"
    return "Get Update"

# Rota para deletar um item
@api_itens_bp.route('/delete/<int:id>')
def delete(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return "Delete"
