from flask import Blueprint, request, redirect, url_for, render_template
from app import db
from app.models.Item import Item

# Criando o Blueprint para itens
itens_bp = Blueprint('web_itens', __name__, url_prefix='/web/itens')

# Rota para listar os itens
@itens_bp.route('/')
def index():
    items_ = Item.query.all()
    return render_template('web/web_itens/index.html', items=items_)

# Rota para criar um item
@itens_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        new_item = Item(name=name, description=description)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('web_itens.index'))
    return render_template('web/web_itens/create.html')

# Rota para atualizar um item
@itens_bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    item = Item.query.get_or_404(id)
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        db.session.commit()
        return redirect(url_for('web_itens.index'))
    return render_template('web/web_itens/update.html', item=item)

# Rota para deletar um item
@itens_bp.route('/delete/<int:id>')
def delete(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('web_itens.index'))
