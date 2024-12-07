from vector_db import create_db, load_db
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.chat_engine.types import ChatResponseGen
from pydantic import BaseModel, Field
from typing import List
from flask import Blueprint, request, jsonify
import os.path
import json
from typing import Dict

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
        example=[1, 2]
    )

ai_router = Blueprint('ai', __name__)

@ai_router.post('/practice_questions')
def generate_practice_questions():
    data = request.get_json()
    
    subject = data.get("subject")
    storage_path = data.get("storage_path")
    query = data.get("query")

    print(query)

    if not os.path.exists(storage_path):
        create_db(subject, storage_path)
    db = load_db(storage_path)

    query_engine = db.as_query_engine()

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
    
    Each question should have exactly 4 answer choices. The correct_answers array should contain the index (0-3) of the correct answer for each question. Make the correct choices vary dont always do the correct one in say index 0
    """

    try:
        response = query_engine.query(structured_query)
        response_text = str(response)
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        
        if json_start != -1 and json_end != -1:
            json_str = response_text[json_start:json_end]
            structured_output = json.loads(json_str) 
            return jsonify(structured_output)
        else:
            return jsonify({
                "error": "Could not parse JSON from response",
                "raw_response": str(response)
            }), 400

    except Exception as e:
        return jsonify({
            "error": str(e),
            "raw_response": str(response) if 'response' in locals() else None
        }), 500

# Single chat memory instance for the entire application
chat_memory = ChatMemoryBuffer.from_defaults(token_limit=1500)

# System message to encourage concise responses
SYSTEM_MESSAGE = """You are a helpful education assistant that provides clear, concise responses. 
Keep your answers focused and brief, ideally 1-2 short paragraphs maximum. 
Prioritize the most important information while maintaining accuracy.
Never give the answer directly but offer to teach or help."""

@ai_router.post('/chatbot')
def chatbot():
    data = request.get_json()
    
    message = data.get("message")
    storage_path = data.get("storage_path")
    
    if not message:
        return jsonify({"error": "Message is required"}), 400
        
    try:
        if not os.path.exists(storage_path):
            return jsonify({"error": "Storage path does not exist"}), 400
            
        db = load_db(storage_path)
        
        # Create chat engine with memory and system message
        chat_engine = db.as_chat_engine(
            memory=chat_memory,
            chat_mode="context",
            verbose=True,
            system_prompt=SYSTEM_MESSAGE
        )
        
        # Get response from chat engine
        response: ChatResponseGen = chat_engine.chat(message)
        response_message = str(response.response)
        
        # Get chat history
        chat_history = [
            {
                "role": msg.role,
                "content": msg.content
            }
            for msg in chat_memory.get()
        ]
        
        return jsonify({
            "response": response_message,
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Error processing chat message"
        }), 500
