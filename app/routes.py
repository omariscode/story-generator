import os
import google.generativeai as genai
from app import app, db, client, IMAGE_DIR
from firebase_admin import auth, firestore
from flask import request, jsonify, send_from_directory
from email_validator import EmailNotValidError, validate_email

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        try:
            valid_email = validate_email(email).email
        except EmailNotValidError as e:
            return jsonify({"error": "Email invalido: {e}"})

        user = auth.create_user(
            email=valid_email,
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
    email = request.json.get('mail')
    password = request.json.get('password')
    try:
        decoded_token = auth.get_user_by_email(email)
        return jsonify({'success': True, 'user': decoded_token})
    except Exception as e:
        return jsonify({'success': False, 'error': f'Token ínvalido: {e}'}), 401

@app.route('/generate-story', methods=['POST'])
def generate_story_and_cover():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    actors = data.get('actors')

    genai.configure(api_key="AIzaSyA5kPPoMJEXttOXRxpcnwBTXG_JxB7NhLA")
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(
        f"Cria uma história infantil com base no título: {title}, descrição: {description}, atores: {actors}. Boa, comprida e criativa."
    )

    story_text = ""
    if response.candidates and response.candidates[0].content.parts:
        story_text = response.candidates[0].content.parts[0].text

    try:
        image = client.text_to_image(title)

        image_filename = f"{title.replace(' ', '_')}.jpg"
        image_path = os.path.join(IMAGE_DIR, image_filename) 
        image.save(image_path, "JPEG")
        image_url = f"/images/{image_filename}"
    except Exception as e:
        return jsonify({"success": False, "message": f"Erro ao gerar a imagem: {str(e)}"}), 500
    
    db.collection('stories').add({
        'title': title,
        'description': description,
        'story': story_text,
        'cover_url': image_url,
        'created_at': firestore.SERVER_TIMESTAMP
    })

    return jsonify({
        'success': True,
        'story': story_text,
        'cover_url': image_url
    })

@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_DIR, filename)
    
@app.route('/get-stories', methods=['GET'])
def get_stories():
    stories = []
    docs = db.collection('stories').stream()
    for doc in docs:
        stories.append(doc.to_dict())
    return jsonify({'success': True, 'stories': stories})
