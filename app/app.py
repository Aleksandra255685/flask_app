from flask import Flask, request, jsonify, render_template
import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
with app.app_context():
    db.create_all()


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price}


@app.route('/', methods=['GET'])
def get_items():
    items = Item.query.all()
    if request.method == 'GET':
        return render_template('products.html', products=[item.to_dict() for item in items])


@app.route('/item_detail/<int:item_id>', methods=['GET'])
def item_details(item_id):
    if request.method == 'GET':
        item = Item.query.get(item_id)
        if item:
            return render_template('product.html', product=item.to_dict())
        return 'Объект не найден', 404


@app.route('/create_item', methods=['POST'])
def create_item():
    if request.method == 'POST':
        item = request.json
        new_item = Item(name=item['name'], price=item['price'])
        db.session.add(new_item)
        db.session.commit()
        return jsonify(new_item.to_dict()), 201
    return 'Объект не создан'


@app.route('/update_item/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    item = Item.query.get(item_id)
    if item:
        data = request.json
        item.name = data['name']
        item.price = data['price']
        db.session.commit()
        return jsonify(item.to_dict())
    return 'Объект не найден', 404


@app.route('/delete_item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item deleted"})
    return 'Объект не найден', 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8084)
