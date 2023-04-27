@app.route('/portfolio', methods=['POST'])
def create_portfolio():
    cursor = db.cursor()
    user_id = request.json['user_id']
    title = request.json['title']
    description = request.json.get('description', None)
    cursor.execute("INSERT INTO Portfolio (user_id, title, description) VALUES (%s, %s, %s)", (user_id, title, description))
    db.commit()
    return jsonify({"message": "Portfolio created successfully"})

@app.route('/portfolio/<int:portfolio_id>', methods=['GET'])
def get_portfolio(portfolio_id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Portfolio WHERE id = %s", (portfolio_id,))
    portfolio = cursor.fetchone()
    return jsonify(portfolio)

@app.route('/portfolio/<int:portfolio_id>', methods=['PUT'])
def update_portfolio(portfolio_id):
    cursor = db.cursor()
    title = request.json['title']
    description = request.json.get('description', None)
    cursor.execute("UPDATE Portfolio SET title=%s, description=%s WHERE id=%s", (title, description, portfolio_id))
    db.commit()
    return jsonify({"message": "Portfolio updated successfully"})

@app.route('/portfolio/<int:portfolio_id>', methods=['DELETE'])
def delete_portfolio(portfolio_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM Portfolio WHERE id=%s", (portfolio_id,))
    db.commit()
    return jsonify({"message": "Portfolio deleted successfully"})
