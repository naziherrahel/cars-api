from flask import Flask, jsonify, request
from db import cursor2, conn2 as cursor, conn

app = Flask(__name__)

# CREATE endpoint for firms
@app.route('/firms', methods=['POST'])
def create_firm():
    data = request.get_json()
    name = data['name']

    # Insert the new firm into the database
    cursor.execute('INSERT INTO firms (name) VALUES (%s) RETURNING id, name', (name,))
    conn.commit()

    # Fetch the new firm data
    new_firm = cursor.fetchone()

    # Return the new firm as JSON
    return jsonify(new_firm)

# READ endpoint for firms
@app.route('/firms/<int:firm_id>', methods=['GET'])
def get_firm(firm_id):
    # Fetch the firm from the database
    cursor.execute('SELECT * FROM firms WHERE id = %s', (firm_id,))
    firm = cursor.fetchone()

    # Return the firm as JSON
    return jsonify(firm)

# UPDATE endpoint for firms
@app.route('/firms/<int:firm_id>', methods=['PUT'])
def update_firm(firm_id):
    data = request.get_json()
    name = data['name']

    # Update the firm in the database
    cursor.execute('UPDATE firms SET name = %s WHERE id = %s RETURNING id, name', (name, firm_id))
    conn.commit()

    # Fetch the updated firm data
    updated_firm = cursor.fetchone()

    # Return the updated firm as JSON
    return jsonify(updated_firm)

# DELETE endpoint for firms
@app.route('/firms/<int:firm_id>', methods=['DELETE'])
def delete_firm(firm_id):
    # Delete the firm from the database
    cursor.execute('DELETE FROM firms WHERE id = %s', (firm_id,))
    conn.commit()

    # Return a success message as JSON
    return jsonify({'message': 'Firm deleted successfully'})

# Create an auto market
@app.route('/auto_market', methods=['POST'])
def add_auto_market():
    name = request.json['name']
    firma_id = request.json['firma_id']

    # Insert new auto market into the database
    cursor.execute('INSERT INTO auto_markets (name, firma_id) VALUES (%s, %s) RETURNING id, name, firma_id',
                   (name, firma_id))
    conn.commit()
    auto_market = cursor.fetchone()

    # Return the newly created auto market as JSON
    return jsonify(auto_market)

# Get all auto markets
@app.route('/auto_market', methods=['GET'])
def get_all_auto_markets():
    cursor.execute('SELECT id, name, firma_id FROM auto_markets')
    auto_markets = cursor.fetchall()

    # Return all auto markets as JSON
    return jsonify(auto_markets)

# Get a single auto market by ID
@app.route('/auto_market/<int:auto_market_id>', methods=['GET'])
def get_auto_market_by_id(auto_market_id):
    cursor.execute('SELECT id, name, firma_id FROM auto_markets WHERE id = %s', (auto_market_id,))
    auto_market = cursor.fetchone()

    # Check if auto market exists
    if not auto_market:
        return jsonify({'error': 'Auto market not found'}), 404

    # Return the auto market as JSON
    return jsonify(auto_market)

# Update an existing auto market
@app.route('/auto_market/<int:auto_market_id>', methods=['PUT'])
def update_auto_market(auto_market_id):
    name = request.json['name']
    firma_id = request.json['firma_id']

    # Update auto market in the database
    cursor.execute('UPDATE auto_markets SET name = %s, firma_id = %s WHERE id = %s RETURNING id, name, firma_id',
                   (name, firma_id, auto_market_id))
    conn.commit()
    auto_market = cursor.fetchone()

    # Check if auto market exists
    if not auto_market:
        return jsonify({'error': 'Auto market not found'}), 404

    # Return the updated auto market as JSON
    return jsonify(auto_market)

# Delete an auto market
@app.route('/auto_market/<int:auto_market_id>', methods=['DELETE'])
def delete_auto_market(auto_market_id):
    # Delete auto market from the database
    cursor.execute('DELETE FROM auto_markets WHERE id = %s', (auto_market_id,))
    conn.commit()

    # Check if auto market was deleted
    if cursor.rowcount == 0:
        return jsonify({'error': 'Auto market not found'}), 404

    # Return success message as JSON
    return jsonify({'message': 'Auto market deleted successfully'})

# Create a new car
@app.route('/cars', methods=['POST'])
def add_car():
    data = request.get_json()
    name = data['name']
    number = data['number']
    auto_market_id = data['auto_market_id']
    query = 'INSERT INTO cars (name, number, auto_market_id) VALUES (%s, %s, %s)'
    cursor.execute(query, (name, number, auto_market_id))
    conn.commit()
    return jsonify({'message': 'Car added successfully!'})

# Retrieve all cars
@app.route('/cars', methods=['GET'])
def get_all_cars():
    query = 'SELECT * FROM cars'
    cursor.execute(query)
    cars = cursor.fetchall()
    return jsonify(cars)

# Retrieve a single car
@app.route('/cars/<int:car_id>', methods=['GET'])
def get_car(car_id):
    query = 'SELECT * FROM cars WHERE id=%s'
    cursor.execute(query, (car_id,))
    car = cursor.fetchone()
    if car:
        return jsonify(car)
    else:
        return jsonify({'message': 'Car not found'}), 404

# Update a car
@app.route('/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    data = request.get_json()
    name = data['name']
    number = data['number']
    auto_market_id = data['auto_market_id']
    query = 'UPDATE cars SET name=%s, number=%s, auto_market_id=%s WHERE id=%s'
    cursor.execute(query, (name, number, auto_market_id, car_id))
    conn.commit()
    return jsonify({'message': 'Car updated successfully!'})

# Delete a car
@app.route('/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    query = 'DELETE FROM cars WHERE id=%s'
    cursor.execute(query, (car_id,))
    conn.commit()
    return jsonify({'message': 'Car deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)