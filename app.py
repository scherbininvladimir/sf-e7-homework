# Flask 
#   https://habr.com/ru/post/246699/

# adverts = [
#     {
#         'id': 1,
#         'title': 'Дом',
#         'date': '6/Mar/2020',
#         'message': 'Продам дом в деревне',
#         'author': 'Иван Иванов'
#     },
#     {
#         'id': 2,
#         'title': 'Квартира',
#         'date': '16/Mar/2020',
#         'message': 'Продам квартиру в Раменском',
#         'author': 'Петр Петров'
#     },    
# ]

import datetime
from flask import Flask, abort, make_response, request, jsonify
from pymongo import MongoClient

mongo_client = MongoClient('192.168.0.6')
db = mongo_client.e7db

app = Flask(__name__)

def encode(d):
    if "_id" in d:
        d["_id"] = str(d["_id"])
    return d

@app.route('/bboard/adverts', methods=['GET'])
def get_adverts():
    adverts = [a for a in db.adverts.find()]    
    adverts = list(map(encode, adverts))
    return jsonify({'adverts': adverts})

@app.route('/bboard/adverts/<int:advert_id>')
def get_advert(advert_id):
    advert = list(filter(lambda t: t['id'] == advert_id, adverts))
    if len(advert) == 0:
        abort(404)
    return jsonify({'task': advert[0]})

@app.route('/bboard/adverts', methods=['POST'])
def create_advert():
    if not request.json or not 'title' in request.json:
        abort(400)
    advert = {
        'title': request.json['title'],
        'message': request.json.get('message', ""),
        'author': request.json.get('author', ""),
        'date': str(datetime.datetime.now())
    }
    db.adverts.insert(advert)
    print(advert)
    return "advert"
    # return jsonify({'advert': advert}), 201



    


@app.route('/bboard/adverts/<int:advert_id>', methods=['PUT'])
def update_task(advert_id):
    advert = list(filter(lambda t: t['id'] == advert_id, adverts))
    if len(advert) == 0:
        abort(404)
    if not request.json:
        abort(400)
    advert[0]['title'] = request.json.get('title', advert[0]['title'])
    advert[0]['message'] = request.json.get('message', advert[0]['message'])
    return jsonify({'advert': advert[0]})

@app.route('/bboard/adverts/<int:advert_id>', methods=['DELETE'])
def delete_task(advert_id):
    advert = list(filter(lambda t: t['id'] == advert_id, adverts))
    if len(advert) == 0:
        abort(404)
    adverts.remove(advert[0])
    return jsonify({'result': True})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)

