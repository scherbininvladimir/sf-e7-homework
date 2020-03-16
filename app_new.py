from flask import Flask, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

mongo_client = MongoClient('192.168.0.6')
db = mongo_client.e7db

app = Flask(__name__)

def encode(d):
    if "_id" in d:
        d["_id"] = str(d["_id"])
    return d

@app.route('/bboard', methods=['GET'])
def get_adverts():
    adverts = [encode(a) for a in db.adverts.find()]
    return jsonify({'tasks': adverts})

@app.route('/bboard/<advert_id>', methods=['GET'])
def get_advert(advert_id):
    advert = db.adverts.find_one({"_id": ObjectId(advert_id)})
    if len(advert) == 0:
        abort(404)
    return jsonify({'advert': encode(advert)})

if __name__ == '__main__':
    app.run(debug=True)