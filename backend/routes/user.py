# User profile page
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import User, UserPerformance 
from datetime import datetime

user = Namespace("user")

user_model = user.model(
    "User",
    {
        "id": fields.Integer(),
        "username": fields.String(),
        "email": fields.String(),
        "points": fields.Integer(),
        "created_at": fields.DateTime(dt_format='iso8601')
    }
)

user.route("/profile")
class UserProfileResource(Resource):
#     @user.marshal_with(user_model)
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)

        user_profile = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at,
            "points": user.get_points(),
            "performance": user.get_performance()
        }

        return jsonify(user_profile), 200
    
    

