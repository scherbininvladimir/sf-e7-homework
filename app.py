#   https://habr.com/ru/post/246699/

import datetime
from flask import Flask, abort, make_response, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_caching import Cache

config = {
    "DEBUG": True,      
    "CACHE_TYPE": "redis",
    "CACHE_REDIS_HOST": "localhost",
    "CACHE_DEFAULT_TIMEOUT": 300
}

mongo_client = MongoClient('192.168.0.6')
db = mongo_client.e7db

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)

def encode(d):
    if "_id" in d:
        d["_id"] = str(d["_id"])
    return d

@app.route('/tst')
@cache.cached(timeout=50)
def get_time():
    return str(datetime.datetime.now())

@app.route('/bboard/adverts')
@cache.cached(timeout=50)
def get_adverts():
    adverts = [encode(a) for a in db.adverts.find()]    
    return jsonify({'adverts': adverts})

@app.route('/bboard/adverts/<advert_id>')
def get_advert(advert_id):
    advert = db.adverts.find_one({"_id": ObjectId(advert_id)})
    if not advert or len(advert) == 0:
        abort(404)
    return jsonify({'advert': encode(advert)})

@app.route('/bboard/adverts/stat/<advert_id>')
def get_advert_stat(advert_id):
    advert = db.adverts.find_one({"_id": ObjectId(advert_id)})
    if not advert or len(advert) == 0:
        abort(404)
    return jsonify({'comments': len(advert['comments']), 'tags': len(advert['tags'])})

@app.route('/bboard/adverts', methods=['POST'])
def create_advert():
    if not request.json or not 'title' in request.json:
        abort(400)
    if 'tags' in request.json and not isinstance(request.get_json()['tags'], list):
        abort(400)
    if  'comments' in request.json and not isinstance(request.json['comments'], list):
        abort(400)
    advert = {
        'title': request.json['title'],
        'message': request.json.get('message', ""),
        'author': request.json.get('author', ""),
        'date': str(datetime.datetime.now()),
        'tags': request.json.get('tags', []),
        'comments': request.json.get('comments', [])
    }
    db.adverts.insert_one(advert)
    return jsonify({'advert': encode(advert)}), 201

@app.route('/bboard/adverts/<advert_id>', methods=['PUT'])
def update_task(advert_id):
    advert = db.adverts.find_one({"_id": ObjectId(advert_id)})
    if len(advert) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'tag' in request.json:
        advert['tags'].append(request.json.get('tag'))
    if 'comment' in request.json:
        advert['comments'].append(request.json.get('comment'))
    db.adverts.update_one({
                            "_id": ObjectId(advert_id)
                          }, 
                          {
                            '$set':{
                                    "tags": advert['tags'], 
                                    "comments": advert['comments']
                            }
                        })
    advert = db.adverts.find_one({"_id": ObjectId(advert_id)})
    return jsonify({'advert': encode(advert)})

@app.route('/bboard/adverts/<advert_id>', methods=['DELETE'])
def delete_advert(advert_id):
    advert = db.adverts.find_one({"_id": ObjectId(advert_id)})
    if not advert or len(advert) == 0:
        abort(404)
    db.adverts.delete_one(advert)
    return jsonify({'result': True})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)

