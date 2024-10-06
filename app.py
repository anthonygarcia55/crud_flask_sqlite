from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Necesario para usar flash messages
db = SQLAlchemy(app)

# Definición del modelo de datos
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Crear la base de datos
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    item_name = request.form.get('name')
    if item_name:
        new_item = Item(name=item_name)
        db.session.add(new_item)
        db.session.commit()
        flash('Item agregado exitosamente!', 'success')
    else:
        flash('El nombre del item no puede estar vacío.', 'error')
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    item = Item.query.get_or_404(id)
    
    if request.method == 'POST':
        item.name = request.form.get('name')
        db.session.commit()
        flash('Item actualizado exitosamente!', 'success')
        return redirect(url_for('index'))
    
    return render_template('edit.html', item=item)

@app.route('/delete/<int:id>')
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Item eliminado exitosamente!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)