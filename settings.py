MONGO_HOST= '192.168.0.6'
MONGO_PORT = 27017

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']

DOMAIN = {
    'user': {
        'schema': {
            'firstname': {
                'type': 'string'
            },
            'lastname': {
                'type': 'string'
            },
            'phone': {
                'type': 'string'
            }
        }
    }
}