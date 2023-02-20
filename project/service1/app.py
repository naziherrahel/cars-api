from flask import Flask, jsonify, request
from db import conn, cursor
from service2.db import conn as conn2, cursor as cursor2
import psycopg2
import requests

app = Flask(__name__)

# Define routes for users
@app.route('/users', methods=['GET'])
def get_users():
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    return jsonify(users)

@app.route('/users', methods=['POST'])
def create_user():
    email = request.json['email']
    password = request.json['password']
    nickname = request.json['nickname']
    cursor.execute('INSERT INTO users (email, password, nickname) VALUES (%s, %s, %s)',
                   (email, password, nickname))
    conn.commit()
    return jsonify({'message': 'User created successfully'})

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    cursor.execute('SELECT * FROM users WHERE id=%s', (user_id,))
    user = cursor.fetchone()
    if user:
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'})

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    # Check if user exists in the database
    cursor.execute("SELECT * FROM users WHERE id = %s ", (user_id,))
    user = cursor.fetchone()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Get request data and validate it
    data = request.get_json()
    try:
        email = data['email']
        password = data['password']
        nickname = data['nickname']
        date_reg = data['date_reg']
    except KeyError:
        return jsonify({'error': 'Invalid request data'}), 400

    # Update user in the database
    cursor.execute("UPDATE users SET email = %s, password = %s, nickname = %s, date_reg = %s WHERE id = %s",
                (email, password, nickname, date_reg, user_id))
    conn.commit()

    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Check if user exists in the database
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Delete user from the database
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()

    return jsonify({'message': 'User deleted successfully'})

# the CRUD endpoint for the car table in the first service
 
# Create a new car
@app.route('/cars', methods=['POST'])
def create_car():
    data = request.json
    name = data['name']
    number = data['number']
    user_id = data['user_id']
    try:
        cursor.execute('INSERT INTO cars (name, number, user_id) VALUES (%s, %s, %s)', (name, number, user_id))
        conn.commit()
        return jsonify({'message': 'Car created successfully'}), 201
    except:
        conn.rollback()
        return jsonify({'message': 'Error occurred while creating the car'}), 500

# Get all cars
@app.route('/cars', methods=['GET'])
def get_cars():
    try:
        cursor.execute('SELECT * FROM cars')
        cars = cursor.fetchall()
        return jsonify({'cars': cars}), 200
    except:
        return jsonify({'message': 'Error occurred while fetching cars'}), 500

# Get a car by ID
@app.route('/cars/<int:car_id>', methods=['GET'])
def get_car(car_id):
    try:
        cursor.execute('SELECT * FROM cars WHERE id = %s', (car_id,))
        car = cursor.fetchone()
        if car is not None:
            return jsonify({'car': car}), 200
        else:
            return jsonify({'message': 'Car not found'}), 404
    except:
        return jsonify({'message': 'Error occurred while fetching the car'}), 500

# Update a car by ID
@app.route('/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    data = request.json
    name = data['name']
    number = data['number']
    user_id = data['user_id']
    try:
        cursor.execute('UPDATE cars SET name=%s, number=%s, user_id=%s WHERE id=%s', (name, number, user_id, car_id))
        conn.commit()
        return jsonify({'message': 'Car updated successfully'}), 200
    except:
        conn.rollback()
        return jsonify({'message': 'Error occurred while updating the car'}), 500

# Delete a car by ID
@app.route('/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    try:
        cursor.execute('DELETE FROM cars WHERE id = %s', (car_id,))
        conn.commit()
        return jsonify({'message': 'Car deleted successfully'}), 200
    except:
        conn.rollback()
        return jsonify({'message': 'Error occurred while deleting the car'}), 500


# register a new car for a specific user
@app.route('/users/<int:user_id>/cars', methods=['POST'])
def register_ca(user_id):
    # Get car data from request body
    data = request.get_json()
    name = data['name']
    number = data['number']
    auto_market_id = data['auto_market_id']

    # Send request to the second service to add the car to its database
    response = requests.post('http://localhost/cars', json=data)
    if response.status_code != 200:
        return jsonify({'message': 'Error adding car to second service'}), 500

    # Get the ID of the newly added car from the second service's response
    car_id = response.json()['id']

    # Add the car to the first service's database and associate it with the specified user
    query = 'INSERT INTO cars (name, number, auto_market_id, user_id) VALUES (%s, %s, %s, %s)'
    cursor.execute(query, (name, number, auto_market_id, user_id))
    conn.commit()

    return jsonify({'message': 'Car added successfully!', 'car_id': car_id})





if __name__ == '__main__':
    app.run(debug=True)
