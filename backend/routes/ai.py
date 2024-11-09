from vector_db import create_db, load_db
from flask import Blueprint, redirect, session, url_for, request, jsonify
import os.path

ai_router = Blueprint('ai', __name__)

@ai_router.get('/practice_questions')
def generate_pratice_questions():

    data = request.get_json()
    
    subject = data.get("subject")
    storage_path = data.get("storage_path")
    query = data.get("query")

    if not os.path.exists(storage_path):
        create_db(subject, storage_path)
    db = load_db(storage_path)

    query_engine = db.as_query_engine()
    response = query_engine.query(query)

    return str(response)


    


