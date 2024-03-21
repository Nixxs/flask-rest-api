from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, StoreModel
from schemas import TagSchema

blp = Blueprint("tags", __name__, description="Operations on tags")

@blp.route("/tag")
class Tag(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self):
        return TagModel.query.all()

    @blp.arguments(TagSchema)
    @blp.response(200, TagSchema)
    def post(self, tag_data):
        tag = TagModel(**tag_data)
        try:
            db.session.add(tag)
            db.session.commit()
            return tag
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting tag.")
    
@blp.route("/tag/<int:tag_id>")
class Tags(MethodView):
    @blp.arguments(TagSchema)
    @blp.response(200, TagSchema)
    def put(self, tag_data, tag_id):
        tag = TagModel.query.get(tag_id)
        if tag:
            tag.name = tag_data["name"]
            tag.store_id = tag_data["store_id"]
        else:
            abort(404, "tag not found.")
        
        db.session.add(tag)
        db.session. commit()

        return tag

    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        db.session.delete(tag)
        db.session.commit()
        return {"message":"tag deleted."}