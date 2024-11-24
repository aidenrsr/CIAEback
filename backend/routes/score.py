from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import GameScore

game_score_ns = Namespace("games", description="Game score")

gamescore_model = game_score_ns.model(
    "thread",
    {
        "score_id": fields.Integer(),
        "user_id": fields.Integer(),
        "score": fields.Integer()
    }
)

@game_score_ns.route("/game_score")
class HighestScoreResource(Resource):
    @jwt_required()
    @game_score_ns.expect(gamescore_model)
    def put(self):

        user_id = get_jwt_identity()
        data = request.get_json()

        new_score = data.get("score")

        current_score = GameScore.query.filter_by(user_id=user_id).first()

        if current_score:
            if new_score > current_score.score:
                current_score.score = new_score
                current_score.save()
                
                return jsonify({"score saved successfully"}), 200

        else:
            new_entry = GameScore(user_id=user_id, score=new_score)
            new_entry.save()

            return jsonify({"score added successfully"}), 201


    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        current_score = GameScore.query.filter_by(user_id=user_id).first()

        if current_score:
            return jsonify({"Highscore": current_score.score})
        else:
            return jsonify({"no score"})