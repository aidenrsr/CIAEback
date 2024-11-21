# scores = Namespace("scores")

# @scores.route("/")
# class ScoresResource(Resource):
#     def get(self):
#         scores = Score.query.all()
#         result = [
#             {
#                 "identification_score": score.identification_score,
#                 "catharsis_score": score.catharsis_score,
#                 "insight_score": score.insight_score,
#                 "score_total": score.score_total,
#             }
#             for score in scores
#         ]
#         return jsonify(result)