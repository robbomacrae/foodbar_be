import json
from config import DevelopmentConfig
from flask import abort
from flask import jsonify
from flask import Flask
from flask import request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Order, Result, Vendor

@app.route('/reset_db')
def reset_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    return 'db reset'

@app.route('/seed_db')
def seed_db():
    db.session.add(Vendor(
        name = 'YCombinator',
        image_path = 'https://cdn.freebiesupply.com/logos/thumbs/2x/y-combinator-logo.png',
        menu = [{
        'category_id':1,
        'category_name':'drinks',
        'items':[{
            'item_id':100001,
            'item_name':'San Pellegrino Sparkling Mineral Water',
            'price': 0.0,
            'image_path':'https://i.imgur.com/PhL9pDa.png',
            'ingredients':['carbonated mineral water'],
            'sold_out': False,
        },{
            'item_id':100002,
            'item_name':'Red Bull',
            'price': 0.0,
            'image_path':'https://i.imgur.com/toam81D.png',
            'ingredients':['carbonated water','citric acid','taurine','sodium bicarbonate','glucuronolactone','caffeine','B vitamins','sucrose','glucose'],
            'sold_out': False,
        },{
            'item_id':100003,
            'item_name':'Coca-Cola',
            'price': 0.0,
            'image_path':'https://i.imgur.com/fAUnPag.png',
            'ingredients':['carbonated water','high-fructose corn syrup','caffeine','phosphoric acid','caramel color','natural flavorings'],
            'sold_out': False,
        },{
            'item_id':100004,
            'item_name':'Diet Coke',
            'price': 0.0,
            'image_path':'https://i.imgur.com/QenwOaz.png',
            'ingredients':['carbonated water','aspartame','caffeine','phosphoric acid','caramel color','natural flavorings','potassium benzonate'],
            'sold_out': False,
        },{
            'item_id':100005,
            'item_name':'Lemon La Croix',
            'price': 0.0,
            'image_path':'https://i.imgur.com/z3szJoY.png',
            'ingredients':['carbonated water','natural essence'],
            'sold_out': False,
        },{
            'item_id':100006,
            'item_name':'Lime La Croix',
            'price': 0.0,
            'image_path':'https://i.imgur.com/MsJLZbX.png',
            'ingredients':['carbonated water','natural essence'],
            'sold_out': False,
        }]
        },{
            'category_name':'snacks',
            'items':[
                {
                    'item_id':200001,
                    'item_name':'Apple',
                    'price': 0.0,
                    'image_path':'https://i.imgur.com/CGPNqar.png',
                    'ingredients':['apple'],
                    'sold_out': False,
                },{
                    'item_id':200002,
                    'item_name':'Tangerine',
                    'price': 0.0,
                    'image_path':'https://i.imgur.com/SBoPfji.png',
                    'ingredients':['tangerine'],
                    'sold_out': False,
                },{
                    'item_id':200003,
                    'item_name':'Philippine Brand Dried Mango',
                    'price': 0.0,
                    'image_path':'https://i.imgur.com/mcYK0ux.png',
                    'ingredients':['mangoes', 'sugar', 'sodium metabisulfite'],
                    'sold_out': False,
                },{
                    'item_id':200004,
                    'item_name':'Cookie',
                    'price': 0.0,
                    'image_path':'https://i.imgur.com/GyqlOPI.png',
                    'ingredients':['butter','sugar','egg','flour','vanilla extract','baking soda','chocolate chips'],
                    'sold_out': False,
                },{
                    'item_id':200005,
                    'item_name':'Poke',
                    'price': 0.0,
                    'image_path':'https://i.imgur.com/eGtI9pF.png',
                    'ingredients':['rice','tuna','edamame beans','green onions','soy sauce'],
                    'sold_out': True,
                }
            ]
        },{
        'category_name':'soup',
        'items':[{
            'item_id':300001,
            'item_name':'tomato soup',
            'price': 4.99,
            'image_path':'https://i.imgur.com/ubjMT8N.png',
            'ingredients':['tomato','olive oil','flour','onion'],
            'sold_out': True,
        },{
            'item_id':300002,
            'item_name':'french onion soup',
            'price': 4.99,
            'image_path':'https://i.imgur.com/MXilBQ7.png',
            'ingredients':['onion','olive oil','mozzarella cheese','garlic'],
            'sold_out': True,
        },
        {
            'item_id':300003,
            'item_name':'clam chowder',
            'price': 5.99,
            'image_path':'https://i.imgur.com/0r26qkn.png',
            'ingredients':['clams','onion','celery','potatoes','carrots','flour'],
            'sold_out': True,
        }]
    }]))
    db.session.commit()
    db.session.add(Order(vendor_id=1, order={'table_number':5, 'items':[{'item_id':1001,'item_name':'tomato soup'},{'item_id':1001,'item_name':'tomato soup'},{'item_id':1002,'item_name':'french onion soup'},{'item_id':2001,'item_name':'garden salad'}]}))
    db.session.add(Order(vendor_id=1, order={'table_number':2, 'special_instructions':None, 'user_id': 1, 'items':[{'item_id':2001,'item_name':'garden salad'}]}))
    db.session.commit()
    r = db.session.query(Vendor).first()
    return jsonify(r.to_json())
    
@app.route('/menu')
def menu():
    vendor_id = request.args.get('vendor_id')
    if not vendor_id:
        abort(400, 'you must include a vendor_id')
    r = Vendor.query.filter_by(id=vendor_id).first()
    return jsonify(r.to_json())

@app.route('/order', methods=['GET', 'POST'])
def order():
    content = request.get_json()
    if request.method == 'POST':
        vendor_id = content.get('vendor_id')
        if not vendor_id:
            abort(400, 'you must include a vendor_id')
        order = Order(vendor_id, content)
        json_data = {}
        try:
            db.session.add(order)
            db.session.commit()
            json_data = {
                'order_id':order.id,
                'expected_wait_time':160,
            }
        except:
            abort(400, 'error in database')
        return jsonify(json_data)
    
    order_id = request.args.get('order_id')
    if not order_id:
        abort(400, 'you must include an order_id')
    r = Order.query.filter_by(id=order_id).first()
    return jsonify(r.to_json())

@app.route('/active_orders')
def active_orders():
    vendor_id = request.args.get('vendor_id')
    if not vendor_id:
        abort(400, 'you must include a vendor_id')
    json_data = []
    special_id = 0
    for r in Order.query.filter_by(vendor_id=vendor_id).all():
        items = r.order.get('items')
        item_map = {}
        for i in items:
            key = i.get('item_name')
            if key in item_map.keys():
                item_map[key] += 1
            else:
                item_map[key] = 1
        for k, v in item_map.items():
            json_data.append({
                'special_id': special_id,
                'id': r.id,
                'name': k,
                'count': v,
                'special_instructions': r.order.get('special_instructions'),
                'user_id': r.order.get('user_id'),
                'table_number': r.order.get('table_number'),
            })
            special_id += 1
    return jsonify(json_data)

@app.route('/new_orders_raw')
def new_orders_raw():
    vendor_id = request.args.get('vendor_id')
    if not vendor_id:
        abort(400, 'you must include a vendor_id')
    json_data = []
    for r in Order.query.filter_by(vendor_id=vendor_id).all():
        order_json = r.order_json()
        json_data.append(order_json)
    return jsonify(json_data)

@app.route('/orders')
def new_orders():
    vendor_id = request.args.get('vendor_id')
    if not vendor_id:
        abort(400, 'you must include a vendor_id')
    json_data = []
    for r in Order.query.filter_by(vendor_id=vendor_id).all():
        items = r.order.get('items')
        item_map = {}
        for i in items:
            key = i.get('item_name')
            if key in item_map.keys():
                item_map[key] += 1
            else:
                item_map[key] = 1
        for k, v in item_map.items():
            json_data.append({
                'name': k,
                'count': v,
                'special_instructions':	r.order.get('special_instructions'),
                'user_id': r.order.get('user_id'),
                'table_number': r.order.get('table_number'),
            })
    return jsonify(json_data)

if __name__ == '__main__':
    app.run()
