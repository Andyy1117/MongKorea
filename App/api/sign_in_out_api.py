from flask import Flask, request, redirect, Blueprint
import mysql.connector

app = Flask(__name__)

# assume you have already defined the connect_db() function

sign_in_out_api_blueprint = Blueprint("sign_in_api_blueprint", __name__)

def connect_db(config):
    conn = mysql.connector.connect(
        host=config["DBHOST"],
        user=config["DBUSERNAME"],
        password=config["DBPASSWORD"],
        database=config["DATABASE"]
    )
    return conn

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    # connect to the database
    conn = connect_db(config)
    cursor = conn.cursor(dictionary=True)

    # query the database for the user with the matching email and password
    cursor.execute("SELECT * FROM Users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()

    # if a matching user is found, redirect to the portfolio page
    if user:
        return redirect('/portfolio')

    # if no matching user is found, show an error message
    else:
        return "Invalid email or password. Please try again."

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    # Register the user with the external API
    response = requests.post(EXTERNAL_API_URL + "/auth/register", json={"username": username, "email": email, "password": password})

    if response.ok:
        # If registration is successful, return a success message as JSON
        response_data = response.json()
        access_token = response_data.get("access_token")

        # connect to the database
        conn = connect_db(config)
        cursor = conn.cursor()

        # insert the new user's data into the database
        query = "INSERT INTO Users (username, password, email) VALUES (%s, %s, %s)"
        values = (username, password, email)
        cursor.execute(query, values)
        conn.commit()

        return jsonify({'message': 'success', 'access_token': access_token}), 200

    # If registration fails, return an error message as JSON
    return jsonify({'message': 'error'}), 401

@app.route('/')
def index():
    return render_template('index.html')