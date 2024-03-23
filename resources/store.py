from flask_jwt_extended import jwt_required, get_jwt_identity
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel
from schemas import StoreSchema, UpdateStoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store")
class Stores(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    @jwt_required()
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="store with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting item.")

        return store

@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
    
    @jwt_required()
    @blp.arguments(UpdateStoreSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_data, store_id):
        # this is how to get the user id from the token
        # userid = get_jwt_identity()
        # print(userid)
        store = StoreModel.query.get(store_id)

        # if the store exists
        if store:
            store.name = store_data["name"]
        else:
            abort(404, message="store does not exist")
        
        db.session.add(store)
        db.session.commit()

        return store

    @jwt_required()
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "store deleted."}