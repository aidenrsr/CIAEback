from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import GameScore

game_score_ns = Namespace("games", description="Game score")

gamescore_model = game_score_ns.model(
    "Score",
    {
        "score": fields.Integer(required=True),
    }
)


@game_score_ns.route("/game_score")
class GameScoreResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        current_score = GameScore.query.filter_by(user_id=user_id).first()

        if current_score:
            return jsonify({"Highscore": current_score.score})
        else:
            return jsonify({"Highscore": 0})

    @jwt_required()
    @game_score_ns.expect(gamescore_model)
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()

        new_score = data.get("score")

        current_score = GameScore.query.filter_by(user_id=user_id).first()

        if current_score:
            if new_score > current_score.score:
                current_score.score = new_score
                current_score.save()
                return jsonify({"Highscore": current_score.score}), 200
        else:
            new_entry = GameScore(user_id=user_id, score=new_score)
            new_entry.save()
            return jsonify({"Highscore": new_score}), 201

        return jsonify({"message": "Score not updated", "Highscore": current_score.score}), 200