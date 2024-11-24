# User profile page
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import User
from backend.routes.book import interaction_model

user_ns = Namespace("user", description="Namespace for user profile")

user_model = user_ns.model(
    "User",
    {
        "id": fields.Integer(),
        "username": fields.String(),
        "email": fields.String(),
        "points": fields.Integer(),
        "created_at": fields.DateTime(dt_format='iso8601')
    }
)

@user_ns.route("/profile")
class UserProfileResource(Resource):
    @user_ns.marshal_with(user_model)
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)

        return user
    
    

