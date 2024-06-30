#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries', methods=['GET'])
def get_bakeries():
    bakeries = Bakery.query.all()
    bakeries_list = [bakery.to_dict() for bakery in bakeries]
    return jsonify(bakeries_list), 200

@app.route('/bakeries/<int:id>', methods=['GET'])
def get_bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if not bakery:
        return make_response(jsonify({"error": "Bakery not found"}), 404)
    return jsonify(bakery.to_dict(rules=('-baked_goods.bakery', 'baked_goods'))), 200

@app.route('/baked_goods/by_price', methods=['GET'])
def get_baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_list = [bg.to_dict() for bg in baked_goods]
    return jsonify(baked_goods_list), 200

@app.route('/baked_goods/most_expensive', methods=['GET'])
def get_most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if not most_expensive:
        return make_response(jsonify({"error": "No baked goods available"}), 404)
    return jsonify(most_expensive.to_dict()), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
