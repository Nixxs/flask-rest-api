from flask import Flask, request
from flask_smorest import abort
from db import stores, items
import uuid

app = Flask(__name__)

@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}

@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found.")

@app.get("/store/<string:store_id>/items")
def get_items(store_id):
    store_items = []
    for item_id in items.keys():
        if items[item_id]["store_id"] == store_id:
            store_items.append(items[item_id])
    
    if len(store_items) > 0:
        return {"items": store_items}, 201
    else:
        abort(404, message="items not found.")

@app.post("/store")
def create_store():
    store_data = request.get_json()

    # if name not in payload 400
    if ("name" not in store_data):
        abort(400, message="Bad request. please include 'name' in the payload")

    # if store name already exists reject
    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(400, message=f"Store already exists.")

    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store

    return store, 201

@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted"}, 201
    except KeyError:
        abort(404, message="store not found")

@app.put("/stores/<string:store_id>")
def update_store(store_id):
    store_data = request.get_json()
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

@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}

@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found.")
    
@app.post("/item")
def create_item():
    item_data = request.get_json()
    # if payload is no good send 400
    if (
            "price" not in item_data 
            or "store_id" not in item_data
            or "name" not in item_data
        ):
        abort(400, message="Bad Request. Ensure price, store_id and name are included in the payload.")
    
    # if item already exists send 400
    for item in items.values():
        if (
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, message=f"Item already exists.")

    if item_data["store_id"] not in stores:
        abort(404, message="Store not found.")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item

    return item

@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted"}, 201
    except KeyError:
        abort(404, message="item not found")

@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if "price" not in item_data or "name" not in item_data:
        abort(400, message="Bad Request, please include price and name in payload")

    try:
        item = items[item_id]
        item |= item_data
        return item
    except KeyError:
        abort(404, message="item not found")