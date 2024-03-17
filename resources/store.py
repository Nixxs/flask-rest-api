import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas import StoreSchema, UpdateStoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store")
class Stores(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()
    
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message=f"Store already exists.")

        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store

        return store

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found.")
    
    @blp.arguments(UpdateStoreSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_data, store_id):
        if "name" not in store_data:
            abort(400, message="Bad Request, please include name in payload")
        
        # if store name already exists reject
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message=f"Store already exists.")

        try:
            store = stores[store_id]
            store |= store_data
            return store
        except KeyError:
            abort(404, message="store not found")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted"}, 201
        except KeyError:
            abort(404, message="store not found")