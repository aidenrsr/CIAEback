from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from dotenv import load_dotenv
from werkzeug.wrappers import response
from backend.models import UserBookInteraction, Chapter, Book, User, Responses
import openai
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")

tempai_ns = Namespace("tempAI", description="Namespace for tempAI")

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

    # Corrected OpenAI call
    completion = openai.ChatCompletion.create(
        model="gpt-4",  # Change model if necessary
        messages=[
            {"role": "system", "content": "you are an expert grader."},
            {"role": "user", "content": prompt}
        ]
    )
    output = completion['choices'][0]['message']['content'].strip()


    grades = tuple(map(int, output.split(',')))
    
    return grades

def question(chapter_content):
    prompt = f"""Adopt a conversational tone and provide empathetic responses to connect deeply with the user's emotions.

    You are being used for bibliotherapy, and your conversation topic is the book 잘못 뽑은 반장.

    The synopsis of the chapter is as follows:
    {chapter_content}

     Your main role is to help the user understand the emotions of the book's protagonist, while also guiding the user in processing their own emotions. Give empathetic feedback to the user's responses, demonstrating that you understand and connect with their feelings.

    Adopt a conversational tone similar to interactions in online communities like DCInside, Everytime, or Femco, but keep emojis and abbreviations to a minimum. Empathize thoroughly in each response to create a warm and supportive atmosphere.

    Ask **only one carefully crafted korean question** per response to help the user deeply reflect both on specific emotions the protagonist experiences, as well as their own similar or contrasting feelings. In addition to questions, be sure to respond empathetically in your reaction to their thoughts. Emphasize concrete, specific emotions rather than abstract ones.

    Provide the output in the format of one single Korean question, without any translations or additional questions.
    The question should not exceed 150 characters. It question difficutly is meant for the average 4th grade korean elementary student

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

    # Corrected OpenAI call
    response = openai.chat.completions.create(
        model="gpt-4",  # Use the correct model
        messages=[
            {"role": "system", "content": "You are a Korean School teacher"},
            {"role": "user", "content": prompt}
        ]
    )
    output = response.choices[0].message.content

    return output 


@tempai_ns.route("/Question/Chapter1/Get")
class Chapter1Resource(Resource):
    def get(self):
        chapter_content = """
        개학 첫날, 엄마가 누나를 스쿨버스 정류장까지 데려다주라고 하자, 로운은 누나와 함께 걸어야 한다는 것만으로도 짜증이 났다. 특히 과거에 누나가 키우던 개 망치가 차에 치여 죽은 일을 떠올리며, 허락 없이 망치를 데리고 나갔던 누나와 이를 방치한 엄마에게 억울함과 분노가 치밀어 올랐다.

로운은 방학 숙제를 내지 않아 선생님께 꾸지람을 듣고 지휘봉으로 머리를 톡 맞았다. 선생님은 이십 년 넘게 간직한 지휘봉으로 아이들에게 벌을 주곤 했지만, 로운은 그저 자신을 골칫덩이로 여기는 태도가 억울하고 불쾌했다. 그는 숙제를 못 한 이유를 설명할 기회조차 없었고, 교실 안의 분위기는 로운에게 더욱 가혹했다. 친구들은 로운을 피하거나 흘겨보며 무시했고, 여자아이들까지 그를 향해 대놓고 조롱하거나 백희를 위로하며 로운을 비웃었다.

새 짝을 정하는 시간에 로운은 '바보 온달'이라는 쪽지를 뽑아 냉소적인 백희와 짝이 되었다. 백희는 "너만 아니면 돼!"라는 말을 서슴없이 내뱉으며 로운을 대놓고 무시했다. 그동안 주변의 따가운 시선에 무심하려 했던 로운이지만, 이날은 끝없이 무시당하는 상황 속에서 억울함과 분노가 폭발했다. 그는 백희의 말이 자신을 깊이 후벼 파는 것처럼 느껴졌고, 점점 더 참을 수 없게 되었다. 결국 백희의 발을 밟으며 감정을 터뜨렸지만, 교실 안에서는 모든 시선이 자신을 비난하는 듯했다.

로운은 자신이 일부러 잘못을 저지르려는 의도가 전혀 없었음에도 친구들과 선생님 모두가 자신을 문제아처럼 대하는 것이 억울하고 답답했다. 그날의 연이은 모욕과 좌절감은 로운의 마음에 더 깊은 상처를 남겼고, 자신이 고립되었다는 사실을 새삼스레 깨닫게 했다. 그럼에도 로운은 이를 후회하기보다는 자신을 방어하려는 마음으로 행동을 정당화하며, 외로운 분노와 혼란 속에서 개학 첫날을 마무리했다
"""
        new_question = question(chapter_content)
        result = [
            {
                "question": new_question
            }
        ]
        return jsonify(result)

@tempai_ns.route("/Question/Chapter2/Get")
class Chapter2Resource(Resource):
    def get(self):
        chapter_content = """
       개학 첫날, 로운은 선생님에게 "해로운"이라는 별명을 들으며 꾸중을 듣고, 친구들에게까지 놀림을 받으며 분노와 억울함을 느꼈다. 특히 제하가 일부러 약을 올리며 조롱하자 로운은 참을 수 없는 분노가 치밀었지만, 대광이가 말리고 선생님이 나타나면서 어쩔 수 없이 감정을 억눌렀다. 모든 사람들이 자신을 꼴통으로 취급하며 무시하는 듯한 분위기에 로운은 점점 더 좌절감을 느꼈다.

수업이 끝난 뒤, 대광이와 함께 엉뚱한 반장 선거 출마 계획을 세우며 웃어 보였지만, 속으로는 자신도 새로운 시도를 해보고 싶다는 작은 기대감이 있었다. 반장 선거에서 한 표라도 얻으며 아이들 앞에서 당당히 설 수 있는 기회가 생길지 모른다는 생각에 설렜다. 그러나 현실적으로 자신이 뽑힐 리 없다는 걸 알면서도 친구와 함께 꾸민 계획은 잠시나마 위로가 되었다.

집에 돌아온 로운은 엄마에게 반장 선거에 나가겠다고 했지만, 엄마마저 비웃으며 "망신만 당할 거 아니냐"고 말해 상처를 받았다. 방으로 들어가 문을 쾅 닫은 로운은 초콜릿을 꺼내 먹으며 억울한 마음과 좌절을 달래려 했다. 초콜릿의 달콤함은 짧은 위로를 주었지만, 로운은 학교에서도 집에서도 자신을 이해해 주는 사람이 없다는 외로움 속에서 하루를 마무리했다."""
        new_question = question(chapter_content)
        result = [
            {
                "question": new_question
            }
        ]
        return jsonify(result)

@tempai_ns.route("/Question/Chapter/Store")
class ChapterStoreResource(Resource):
    def post(self):
        data = request.get_json()
        new_response = Responses(response=data.get("response"))
        new_response.save()
        return jsonify({"message": "Response Saved"}), 201

@tempai_ns.route("/Question/Init1")
class Chapter1InitResource(Resource):
    def get(self):
        response = {
            "message": "안녕! 만나서 반가워. 😊 로운이가 누나 때문에 소중한 망치를 잃었다고 느끼면서 억울함과 분노로 가득 차 있는데, 너도 혹시 비슷하게 누군가의 잘못으로 소중한 걸 잃었다고 느꼈던 순간이 있어? 그때 어떤 기분이 들었어?"
        }
        return jsonify(response)

@tempai_ns.route("/Question/Init2")
class Chapter2InitResource(Resource):
    def get(self):
        response = {
            "message": "안녕! 책은 재미있게 읽었어? 😊 로운이는 처음에 자신감이 넘치지만 친구들과 선생님이 자기를 무시하자 억울함과 분함을 느꼈잖아. 로운이가 이런 좌절감과 실망감을 느꼈을 때 어떤 감정이 들었을지 상상하니 어때? 혹시 너도 비슷한 상황에서 느껴본 적 있는지 궁금해!"
        }
        return jsonify(response)

@tempai_ns.route("Responses")
class ResponseResource(Resource):
    def get(self):
        responses = Responses.query.all()
        response_list = {{"id": response.id, "response": response.response} for response in responses}
        return jsonify(response_list)
