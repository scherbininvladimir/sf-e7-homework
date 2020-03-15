MONGO_HOST= '192.168.0.6'
MONGO_PORT = 27017

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']

DOMAIN = {
    'advert': {
        'schema': {
            'title': {
                'type': 'string'
            },
            'data': {
                'type': 'date'
            },
            'message': {
                'type': 'string'
            }
            'author': {
                'type': 'string'
            }
        }
    }
}

