# User profile page
from flask import request, jsonify
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import User, UserPerformance, UserPoint
from backend.ext import db

user = Namespace("user")


user.route("/profile")
class UserProfileResource(Resource):
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
    
    

