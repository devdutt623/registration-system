from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM registration').fetchall()
    conn.close()
    return jsonify([dict(user) for user in users])

@app.route('/user', methods=['POST'])
def add_user():
    data = request.json
    name, email, dob = data['name'], data['email'], data['dob']
    conn = get_db_connection()
    conn.execute('INSERT INTO registration (name, email, dob) VALUES (?, ?, ?)', (name, email, dob))
    conn.commit()
    conn.close()
    return jsonify({'message': 'User added successfully'}), 201

@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    name, email, dob = data['name'], data['email'], data['dob']
    conn = get_db_connection()
    conn.execute('UPDATE registration SET name = ?, email = ?, dob = ? WHERE id = ?', (name, email, dob, id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'User updated successfully'})

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM registration WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'User deleted successfully'})

if __name__ == '__main__':
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS registration (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        dob TEXT NOT NULL)''')
    conn.close()
    app.run(debug=True)
