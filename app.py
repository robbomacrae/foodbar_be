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
            'image_path':'https://cdn.shopify.com/s/files/1/1539/5375/products/SP500P_San_Pellegrino_Sparkling_Mineral_Water_PET_24x500ml_large_2x.jpg?v=1513893896',
            'ingredients':['carbonated mineral water'],
        },{
            'item_id':100002,
            'item_name':'Red Bull',
            'price': 0.0,
            'image_path':'https://target.scene7.com/is/image/Target/GUEST_815596f4-1479-4085-aa75-1ed074c45e65?wid=488&hei=488&fmt=pjpeg',
            'ingredients':['carbonated water','citric acid','taurine','sodium bicarbonate','glucuronolactone','caffeine','B vitamins','sucrose','glucose'],
        },{
            'item_id':100003,
            'item_name':'Coca-Cola',
            'price': 0.0,
            'image_path':'https://cdn.shopify.com/s/files/1/0039/0574/9105/products/316a9d959edca55087286782fa2397fa_700x700.jpg?v=1539162994',
            'ingredients':['carbonated water','high-fructose corn syrup','caffeine','phosphoric acid','caramel color','natural flavorings'],
        },{
            'item_id':100004,
            'item_name':'Diet Coke',
            'price': 0.0,
            'image_path':'https://onlinecashandcarry.co.uk/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/d/i/diet_coke_150ml.jpg',
            'ingredients':['carbonated water','aspartame','caffeine','phosphoric acid','caramel color','natural flavorings','potassium benzonate'],
        },{
            'item_id':100005,
            'item_name':'Lemon La Croix',
            'price': 0.0,
            'image_path':'https://scontent.harristeeter.com/legacy/productimagesroot/DJ/7/318137.jpg',
            'ingredients':['carbonated water','natural essence'],
        },{
            'item_id':100006,
            'item_name':'Lime La Croix',
            'price': 0.0,
            'image_path':'https://scontent.harristeeter.com/legacy/productimagesroot/DJ/6/318136.jpg',
            'ingredients':['carbonated water','natural essence'],
        }]
        },{
        'category_name':'soup',
        'items':[{
            'item_id':1001,
            'item_name':'tomato soup',
            'price': 4.99,
            'image_path':'https://www.yummymummykitchen.com/wp-content/uploads/2018/03/32444-how-to-make-tomato-soup-with-fresh-tomatoes.jpg',
            'ingredients':['tomato','olive oil','flour','onion']
        },{
            'item_id':1002,
            'item_name':'french onion soup',
            'price': 4.99,
            'image_path':'https://food.fnr.sndimg.com/content/dam/images/food/fullset/2013/6/28/0/IG0508_French-Onion-Soup_s4x3.jpg.rend.hgtvcom.826.620.suffix/1375577926918.jpeg',
            'ingredients':['onion','olive oil','mozzarella cheese','garlic']
        },
        {
            'item_id':1003,
            'item_name':'clam chowder',
            'price': 5.99,
            'image_path':'https://www.spendwithpennies.com/wp-content/uploads/2018/01/New-England-Clam-Chowder-3.jpg',
            'ingredients':['clams','onion','celery','potatoes','carrots','flour']
        }]
    },{
        'category_id':2,
        'category_name':'salad',
        'items':[
            {'item_id':2001,'item_name':'garden salad','price': 8.99,
        'image_path': 'https://food.fnr.sndimg.com/content/dam/images/food/fullset/2018/3/8/0/FNM_040118-Olive-Garden-Style-House-Salad_s4x3.jpg.rend.hgtvcom.616.462.suffix/1520543510452.jpeg','ingredients':['lettuce','spinnach','tomato','cheddar cheese']}
        ]
    }]))
    db.session.commit()
    db.session.add(Order(vendor_id=1, order={'table_number':5, 'items':[{'item_id':1001,'item_name':'tomato soup'},{'item_id':1001,'item_name':'tomato soup'},{'item_id':1002,'item_name':'french onion soup'},{'item_id':2001,'item_name':'garden salad'}]}))
    db.session.add(Order(vendor_id=1, order={'table_number':2, 'items':[{'item_id':2001,'item_name':'garden salad'}]}))
    db.session.commit()
    r = db.session.query(Vendor).first()
    return jsonify(r.to_json())
    
@app.route('/test')
def test():
    db.session.add(Result(url='test'))
    db.session.commit()
    r = db.session.query(Result).first()
    return jsonify(r.to_json())

@app.route('/')
def hello():
    return "Hello World!"

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
    for r in Order.query.filter_by(vendor_id=vendor_id).all():
        items = r.order.get('items')
        item_map = {}
        for i in items:
            if i.get('item_name') in item_map.keys():
                item_map[i.get('item_name')] += 1
            else:
                item_map[i.get('item_name')] = 1
        for k, v in item_map.items():
            json_data.append({
                'id': r.id,
                'name': k,
                'count': v,
                'table_number': r.order.get('table_number'),
            })
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
            if i.get('item_name') in item_map.keys():
                item_map[i.get('item_name')] += 1
            else:
                item_map[i.get('item_name')] = 1
        for k, v in item_map.items():
            json_data.append({
                'name': k,
                'count': v,
                'table_number': r.order.get('table_number'),
            })
    return jsonify(json_data)

if __name__ == '__main__':
    app.run()
