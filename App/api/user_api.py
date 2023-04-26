from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="cs232-pw",
    database="cs232-mysql"
)

@app.route('/users', methods=['GET'])
def get_all_users():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    return jsonify(users)

@app.route('/users/<int:user_id', methods=['GET'])
def get_user(user_id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    return jsonify(user)

@app.route('/users', methods=['POST'])
def create_user():
    cursor = db.cursor()
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    cursor.execute("INSERT INTO Users (username, password, email) VALUES (%s, %s, %s,)", (username, password, email))
    db.commit()
    return jsonify({"message": "User created successfully"})

@app.route('/users/<int:user_id', methods=['PUT'])
def update_user(user_id):
    cursor = db.cursor()
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    cursor.execute("UPDATE Users SET username=%s, password=%s email=%s WHERE id=%s", (username, password, email, user_id))
    db.commit()
    return jsonify({"message": "User updated successfully"})

@app.route('/users/<int:user_id', methods=['DELETE'])
def delete_user(user_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM Users WHERE id=%s", (user_id,))
    db.commit()
    return jsonify({"message": "User deleted successfully"})