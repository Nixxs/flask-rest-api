from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256

from db import db
from models import UserModel
from schemas import UserSchema

blp = Blueprint("Users", __name__, description="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
    #apply the schema to the incoming data this ensures that we are getting the data from the user in the correct format
    @blp.arguments(UserSchema)
    def post(self, user_data):
        
        if UserModel.query.filter_by(username=user_data["username"]).first():
            abort(400, message="User already exists.")
        
        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )

        db.session.add(user)
        db.session.commit()
        return {"message":"User created."}, 200

@blp.route("/user/<int:user_id>")
class User(MethodView):
    # ensures that we are returning the data in the correct format
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message":"User deleted."}, 200

@blp.route("/users")
class Users(MethodView):
    # ensures that we are returning the data in the correct format
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()