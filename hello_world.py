import logging
import datetime
from google.cloud import datastore
from flask import json
from flask import jsonify
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


items = {}
ds_client = datastore.Client()


class Item(object):

    KIND = 'Item'
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.create_time = kwargs.get('create_time')
        if not self.create_time:
            self.create_time = datetime.datetime.utcnow()
        self.update_time = kwargs.get('update_time')
        if not self.update_time:
            self.update_time = datetime.datetime.utcnow()
        self.value = kwargs.get('value')

    def toDict(self):
        return self.__dict__

    def save(self, id_=None):
        if not id_:
            key = ds_client.key(self.KIND)
            item = datastore.Entity(key=key)
            for key, value in self.toDict().iteritems():
                item[key] = value
            ds_client.put(item)
            return item.key.name
        else:
            item = self.get(id_)
        pass

    def get(self, id_):
        pass

    def list(self):
        pass


class ItemController(Resource):

    def get(self, id_):
        return  jsonify({id_: items.get(id_).toDict()})

    def put(self, id_):
        item = Item(id=id_, **(request.get_json()))
        items[id_] = item
        return  jsonify({id_: items.get(id_).toDict()})

class ItemsController(Resource):

    def get(self):
        return jsonify({'items': [i.toDict() for i in items.itervalues()]})

    def post(self):
        logging.error(request.get_json())
        item = Item(**(request.get_json()))
        id_ = item.save()
        return  jsonify({id_: item.toDict()})


api.add_resource(ItemController, '/<string:id_>')
api.add_resource(ItemsController, '/')

if __name__ == '__main__':
    app.run(debug=True)
