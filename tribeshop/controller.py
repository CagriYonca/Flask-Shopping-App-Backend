from flask import Flask, Response, request
from flask_mongoengine import MongoEngine
from tribeshop.models import Yak, Tribe
import tribeshop.services as serv
import xmltodict
import json


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'tribe-db',
    'host': 'mongodb+srv://admin:admin@tribe-db.jymzx.mongodb.net/tribe-db?retryWrites=true&w=majority'
}
app.config['JSON_SORT_KEYS'] = False

db = MongoEngine()
db.init_app(app)


@app.route('/setup')
def setup(file_name='herd.xml'):
    Yak.objects().delete()
    Tribe.objects().delete()
    with open(file_name, 'rb') as file:
        xml = xmltodict.parse(file.read())
        temp_tribe_list = []
        for item in xml['herd']['labyak']:
            yak_object = Yak(name=item['@name'], age=item['@age'], sex=item['@sex'])
            yak_object.save()
            temp_tribe_list.append(yak_object.id)
        Tribe(tribe=temp_tribe_list).save()
    return Response(json.dumps({'result': 'Success'}), mimetype='application/json', status=200)


@app.route('/yak-shop/herd/<int:T>', methods=['GET'])
def return_herd(T):
    serv.produce_for_t_days(T)
    result = {
        'herd': serv.get_tribe_info(T)
    }
    return Response(json.dumps(result), mimetype='application/json', status=200)


@app.route('/yak-shop/stock/<int:T>', methods=['GET'])
def return_stock(T):
    total_milk, total_wool, _ = serv.produce_for_t_days(T)
    result = {
        'milk': total_milk,
        'skins': total_wool
    }
    tribe = Tribe.objects.first()
    tribe.update(
        total_milk=result.get('milk'),
        total_wool=result.get('skins'))
    return Response(json.dumps(result), mimetype='application/json', status=200)


@app.route('/yak-shop/order/<int:T>', methods=['POST'])
def add_order(T):
    data = json.loads(request.data)
    result = serv.check_stock_info(T, data)
    print(result)
    if 'milk' in result and 'skins' in result:
        return Response(json.dumps(result), mimetype='application/json', status=201)
    elif 'milk' in result or 'skins' in result:
        return Response(json.dumps(result), mimetype='application/json', status=206)
    else:
        return Response(mimetype='application/json', status=404)        
