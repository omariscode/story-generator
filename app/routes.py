import requests
from app import app, db
from firebase_admin import auth
from flask import request, jsonify
import google.generativeai as genai

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        user = auth.create_user(
            email=email,
            password=password
        )

        return jsonify({'success': True,'message': 'Usuário criado com sucesso!',
            'user': {
                'uid': user.uid,
                'email': user.email}
                }), 201
    
    except Exception as e:
        return jsonify({'success': False,'error': str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    token = request.json.get('token')
    try:
        decoded_token = auth.verify_id_token(token)
        return jsonify({'success': True, 'user': decoded_token})
    except Exception as e:
        return jsonify({'success': False, 'error': f'Invalid token: {e}'}), 401

@app.route('/generate-story', methods=['POST'])
def generate_story():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    actors = data.get('actors')
    
    genai.configure(api_key="AIzaSyA5kPPoMJEXttOXRxpcnwBTXG_JxB7NhLA")
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(f"Cria uma historia infantil com base o título: {title}, descrição: {description}, atores:{actors}. Boa, comprida e seja mesmo criativa.")
    story = response.content.get('story')  
        
    db.collection('stories').add({
        'title': title,
        'description': description,
        'story': story,
    })
        
    return jsonify({'success': True, 'story': story})
    

@app.route('/generate-cover', methods=['POST'])
def generate_cover():
    description = request.json.get('description')
    
    response = requests.post(
        'https://api.huggingface.co/models/some-model',
        headers={'Authorization': 'Bearer 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'},
        json={"description": description}
    )
    
    if response.status_code == 200:
        cover_url = response.json().get('cover_url')  
        return jsonify({'success': True, 'cover_url': cover_url})
    else:
        return jsonify({'success': False, 'error': 'Failed to generate cover'}), 500
    
@app.route('/get-stories', methods=['GET'])
def get_stories():
    stories = []
    docs = db.collection('stories').stream()
    for doc in docs:
        stories.append(doc.to_dict())
    return jsonify({'success': True, 'stories': stories})