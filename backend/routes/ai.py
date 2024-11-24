from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from dotenv import load_dotenv
from backend.models import UserBookInteraction, Chapter, Book, User
import openai
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_KEY")

ai_ns = Namespace("ResponseAI", description="A namespace for ResponseAI")

response_model = ai_ns.model(
    "Response",
    {
        "response": fields.String(),
        "question": fields.String(),
        "question_type": fields.String()
    }
)

question_model = ai_ns.model(
    "Question",
    {
        "question": fields.String(),
        "question_type": fields.String()
    }
)

def grade(response_text, chapter_content):
    # grading scale table form
    grading_scale_table = {
        "identification": [
            (0, 19, "no connection to the character or personal experience"),
            (20, 39, "minimal connection to the character or personal experience"),
            (40, 59, "partial understanding of the character's experience or limited personal connection"),
            (60, 79, "moderate understanding of the character's experience and some personal connection"),
            (80, 100, "clear understanding of the character's experience and strong personal connection")
        ],
        "catharsis": [
            (0, 19, "irrelevant response or no emotional engagement"),
            (20, 39, "minimal relevance or weak emotional engagement"),
            (40, 59, "somewhat relevant response with limited emotional reflection"),
            (60, 79, "moderately relevant response showing some emotional reflection"),
            (80, 100, "highly relevant response showing significant emotional reflection")
        ],
        "insight": [
            (0, 19, "little to no reflection on experiences or application of learning"),
            (20, 39, "minimal reflection on experiences or application of learning"),
            (40, 59, "some reflection on experiences, but limited application of learning"),
            (60, 79, "moderate reflection and partial application of learning to new situations"),
            (80, 100, "thorough reflection and clear application of learning to new situations")
        ]
    }

    grading_scale = "\n".join(
        f"{criterion}:\n" +
        "\n".join(f"- {minscore}-{maxscore}: {description}" for minscore, maxscore, description in options)
        for criterion, options in grading_scale_table.items()
    )
    
    # promp needs to be adjusted
    prompt = f"""
        you are a grading assistant. grade the following written response based on the criteria provided in the grading scale.
        reference the provided chapter content to evaluate the response appropriately.
        return three integers corresponding to the grades.

        grading scale:
        {grading_scale}

        chapter context:
        {chapter_content}

        response to grade:
        "{response_text}"

        return the grades as integers in the format: identification, catharsis, insight.
    """

    completion = openai.chatcompletion.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[{"role": "system", "content": "you are an expert grader."},
                  {"role": "user", "content": prompt}]
    )

    output = completion['choices'][0]['message']['content'].strip()


    try:
        grades = tuple(map(int, output.split(',')))
    except valueerror:
        raise valueerror(f"unexpected response from model: {output}")
    
    return grades

def question(book_title, chapter_content):
    prompt = f"""Adopt a conversational tone and provide empathetic responses to connect deeply with the user's emotions.

    You are being used for bibliotherapy, and your conversation topic is the book {book_title}.

    The synopsis of the chapter is as follows:
    {chapter_content}

     Your main role is to help the user understand the emotions of the book's protagonist, while also guiding the user in processing their own emotions. Give empathetic feedback to the user's responses, demonstrating that you understand and connect with their feelings.

    Adopt a conversational tone similar to interactions in online communities like DCInside, Everytime, or Femco, but keep emojis and abbreviations to a minimum. Empathize thoroughly in each response to create a warm and supportive atmosphere.

    Ask **only one carefully crafted korean question** per response to help the user deeply reflect both on specific emotions the protagonist experiences, as well as their own similar or contrasting feelings. In addition to questions, be sure to respond empathetically in your reaction to their thoughts. Emphasize concrete, specific emotions rather than abstract ones.

    Additionally, include the **type of the question** (one of: Identification, Catharsis, Insight). This should indicate the purpose of the question:
    - **Identification**: Helping the user identify and connect with the character's emotions.
    - **Catharsis**: Encouraging the user to release and process their own emotions through the character's experiences.
    - **Insight**: Guiding the user to reflect on their experiences and draw learning from them.

    Provide the output in the following format:
    ```
    Question: [Insert question here]
    Type: [Identification / Catharsis / Insight]
    ```

    # Steps

    1. Identify the protagonist's current emotional state in the context of their actions or experiences in the book.
    2. Formulate a question about a specific emotion linked to this state that encourages the user to share their thoughts.
    3. Provide empathetic responses to the user's reflections to show that you understand their feelings.
    4. Encourage the user to relate those emotions to their own experiences, focusing on a similarly specific emotional nuance.

    # Notes

    - Place emphasis on guiding the user to provide emotional insights not only into the book's protagonist but also themselves.
    - Use empathy-driven questions that explore the protagonist's emotions concretely and lead naturally into reflections tied to the user's feelings.
    - Respond to the user's answers with empathetic reactions before continuing with the next question to ensure user feels heard and understood. This helps strengthen the user's comfort and connection.
    - Only ask one well-defined, specific emotional question per response.
    - Shift focus from abstract emotions (e.g. “anger”) to nuanced, specific ones (e.g. “feeling betrayed or powerless”). 
    - Example empathetic statements: "That sounds really tough. I can see why you'd feel that way." or "It must have been overwhelming for you. It's completely understandable."
    """

    completion = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[{"role": "system", "content": "You are an korean reading comprehension teacher"},
                  {"role": "user", "content": prompt}]
    )

    output = completion['choices'][0]['message']['content'].strip()
    
    # Extracting the question and its type
    question = output.split("Question: ")[1].split("\n")[0].strip()
    question_type = output.split("Type: ")[1].strip()

    return question, question_type



@ai_ns.route("/Grade/Book/<int:book_id>/Chapter/<int:chapter_id>")
class GradeResponse(Resource):
    @ai_ns.expect(response_model)
    @jwt_required()
    def post(self, book_id, chapter_id):

        # Get user
        user_id = get_jwt_identity()

        toUpdate = UserBookInteraction.query.filter_by(user_id=user_id, book_id=book_id).first_or_404()
        chapter = Chapter.query.filter_by(book_id=book_id, chapter_id=chapter_id).first_or_404().content
        content = chapter.content

        # Request the response
        data = request.get_json()

        response_grade = grade(data.get("Response"), content)

        user = User.query.get(user_id)
        user.updateResponse(data.get(""))

        result = [
            {
                "IdentificationScore": response_grade[0],
                "CatharsisScore": response_grade[1],
                "InsightScore": response_grade[2],
            }
        ]

        toUpdate.update(response_grade[0], response_grade[1], response_grade[2])

        return result

@ai_ns.route("/Question/Book/<int:book_id>/Chapter/<int:chapter_id>")
class QuestionResponse(Resource):
    @ai_ns.marshal_with(question_model)
    def get(self, book_id, chapter_id):

        book = Book.query.filter_by(book_id=book_id).first()
        if not book:
            return jsonify({"message": "Book not found"}), 404
        book_title = book.title

        chapter = Chapter.query.filter_by(book_id=book_id, chapter_id=chapter_id).first_or_404()
        chapter_content = chapter.content

        question_result, question_type = question(book_title, chapter_content)

        # Return the result in the format defined by question_model
        return {
            "question": question_result,
            "question_type": question_type
        }


