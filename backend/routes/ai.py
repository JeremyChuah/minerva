# from vector_db import create_db, load_db
# from flask import Blueprint, redirect, session, url_for, request, jsonify
# import os.path
# from pydantic import BaseModel, Field
# from llama_index.core.output_parsers.pydantic import PydanticOutputParser
# from llama_index.core.prompts import PromptTemplate
# from typing import List

# class PracticeQuestion(BaseModel):
#     questions: List[List[str]] = Field(
#         description="List of questions where each inner list contains the question text followed by answer choices",
#         example=[
#             ["What is the capital of France?", "London", "Paris", "Berlin", "Madrid"],
#             ["Which planet is closest to the Sun?", "Venus", "Mars", "Mercury", "Earth"]
#         ]
#     )
#     correct_answers: List[int] = Field(
#         description="List of indices indicating the correct answer for each question",
#         example=[1, 2]  # Paris is at index 1, Mercury is at index 2
#     )


# ai_router = Blueprint('ai', __name__)
# @ai_router.get('/practice_questions')
# def generate_pratice_questions():

#     data = request.get_json()
    
#     subject = data.get("subject")
#     storage_path = data.get("storage_path")
#     query = data.get("query")

#     if not os.path.exists(storage_path):
#         create_db(subject, storage_path)
#     db = load_db(storage_path)

#     query_engine = db.as_query_engine()
#     response = query_engine.query(query)

#     return str(response)

from vector_db import create_db, load_db
from llama_index.core.output_parsers.pydantic import PydanticOutputParser
from llama_index.core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import List
from flask import Blueprint, request, jsonify
import os.path
import json

class PracticeQuestion(BaseModel):
    questions: List[List[str]] = Field(
        description="List of questions where each inner list contains the question text followed by answer choices",
        example=[
            ["What is the capital of France?", "London", "Paris", "Berlin", "Madrid"],
            ["Which planet is closest to the Sun?", "Venus", "Mars", "Mercury", "Earth"]
        ]
    )
    correct_answers: List[int] = Field(
        description="List of indices indicating the correct answer for each question",
        example=[1, 2]  # Paris is at index 1, Mercury is at index 2
    )

ai_router = Blueprint('ai', __name__)

@ai_router.get('/practice_questions')
def generate_practice_questions():
    data = request.get_json()
    
    subject = data.get("subject")
    storage_path = data.get("storage_path")
    query = data.get("query")

    if not os.path.exists(storage_path):
        create_db(subject, storage_path)
    db = load_db(storage_path)

    # Create the query engine with a structured prompt
    query_engine = db.as_query_engine()
    
    # Modify the query to request the specific format we want
    structured_query = f"""
    Generate 10 multiple choice questions about: {query}
    
    Return the response in this exact JSON format:
    {{
        "questions": [
            ["What is the question?", "Choice 1", "Choice 2", "Choice 3", "Choice 4"],
            ["Another question?", "Choice 1", "Choice 2", "Choice 3", "Choice 4"]
        ],
        "correct_answers": [0, 1]
    }}
    
    Each question should have exactly 4 answer choices. The correct_answers array should contain the index (0-3) of the correct answer for each question.
    """

    try:
        response = query_engine.query(structured_query)
        
        # Extract the JSON string from the response
        # Find the first { and last } to extract the JSON portion
        response_text = str(response)
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        
        if json_start != -1 and json_end != -1:
            json_str = response_text[json_start:json_end]
            # Parse the JSON response
            structured_output = json.loads(json_str)
            
            return jsonify(structured_output)
        else:
            # If no JSON found, try to structure the response
            return jsonify({
                "error": "Could not parse JSON from response",
                "raw_response": str(response)
            }), 400

    except Exception as e:
        return jsonify({
            "error": str(e),
            "raw_response": str(response) if 'response' in locals() else None
        }), 500