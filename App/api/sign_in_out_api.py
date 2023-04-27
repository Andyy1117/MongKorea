from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    # Your authentication code here...
    # Authenticate the user's credentials with the external API

    # If authentication is successful, return a success message as JSON
    return jsonify({'message': 'success'})

    # If authentication fails, return an error message as JSON
    return jsonify({'message': 'error'})

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    # Your registration code here...
    # Register the user with the external API

    # If registration is successful, return a success message as JSON
    return jsonify({'message': 'success'})

    # If registration fails, return an error message as JSON
    return jsonify({'message': 'error'})

@app.route('/')
def index():
    return render_templates('index.html')