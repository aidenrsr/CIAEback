from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from dotenv import load_dotenv
from backend.models import UserBookInteraction, Chapter
import openai
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_KEY")

ai_ns = Namespace("ResponseAI", description="A namespace for ResponseAI")

def grade(response_text, chapter_content):
    # Grading scale table form
    grading_scale_table = {
        "Identification": [
            (0, 19, "No connection to the character or personal experience"),
            (20, 39, "Minimal connection to the character or personal experience"),
            (40, 59, "Partial understanding of the character's experience or limited personal connection"),
            (60, 79, "Moderate understanding of the character's experience and some personal connection"),
            (80, 100, "Clear understanding of the character's experience and strong personal connection")
        ],
        "Catharsis": [
            (0, 19, "Irrelevant response or no emotional engagement"),
            (20, 39, "Minimal relevance or weak emotional engagement"),
            (40, 59, "Somewhat relevant response with limited emotional reflection"),
            (60, 79, "Moderately relevant response showing some emotional reflection"),
            (80, 100, "Highly relevant response showing significant emotional reflection")
        ],
        "Insight": [
            (0, 19, "Little to no reflection on experiences or application of learning"),
            (20, 39, "Minimal reflection on experiences or application of learning"),
            (40, 59, "Some reflection on experiences, but limited application of learning"),
            (60, 79, "Moderate reflection and partial application of learning to new situations"),
            (80, 100, "Thorough reflection and clear application of learning to new situations")
        ]
    }

    grading_scale = "\n".join(
        f"{criterion}:\n" +
        "\n".join(f"- {minScore}-{maxScore}: {description}" for minScore, maxScore, description in options)
        for criterion, options in grading_scale_table.items()
    )
    
    # Promp needs to be adjusted
    prompt = f"""
        You are a grading assistant. Grade the following written response based on the criteria provided in the grading scale.
        Reference the provided chapter content to evaluate the response appropriately.
        Return three integers corresponding to the grades.

        Grading Scale:
        {scale_text}

        Chapter Context:
        {chapter_content}

        Response to grade:
        "{response}"

        Return the grades as integers in the format: Identification, Catharsis, Insight.
    """

    completion = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[{"role": "system", "content": "You are an expert grader."},
                  {"role": "user", "content": prompt}]
    )

    output = completion['choices'][0]['message']['content'].strip()


    try:
        grades = tuple(map(int, output.split(',')))
    except ValueError:
        raise ValueError(f"Unexpected response from model: {output}")
    
    return grades


@ai_ns.route("Grade/<int:book_id>/Chapter/<int:chapter_id>")
class GradeResponse(Resource):
    @jwt_required()
    def post(self, book_id, chapter_id):

        # Get user
        user_id = get_jwt_identity()

        toUpdate = UserBookInteraction.query.filter_by(user_id=userid, book_id=book_id).first_or_404()
        chapter = Chapter.query.filter_by(book_id=book_id, chapter_id=chapter_id).first_or_404().content
        content = chapter.content

        # Request the response
        data = request.get_json()

        response_grade = grade(data.get("Response"), content)

        result = [
            {
                "IdentificationScore": response_grade[0],
                "CatharsisScore": response_grade[1],
                "InsightScore": response_grade[2],
            }
        ]

        toUpdate.update(response_grade[0], response_grade[1], response_grade[2])

        return result
