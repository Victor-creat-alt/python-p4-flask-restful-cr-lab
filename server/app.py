#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'  # Database connection
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable unnecessary tracking
app.json.compact = True  # Compact JSON formatting

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        """Retrieve all plant records."""
        plants = Plant.query.all()  # Get all plants from the database
        return [plant.to_dict() for plant in plants], 200  # Return as a list with HTTP 200 status

    def post(self):
        """Create a new plant record."""
        data = request.get_json()  # Retrieve JSON data from the request body
        new_plant = Plant(
            name=data.get('name'),
            image=data.get('image'),
            price=data.get('price')
        )
        db.session.add(new_plant)  # Add the new plant to the database
        db.session.commit()  # Commit the transaction
        return new_plant.to_dict(), 201  # Return the created plant with HTTP 201 status

class PlantByID(Resource):
    def get(self, id):
        """Retrieve a specific plant record by ID."""
        plant = Plant.query.get(id)  # Get the plant by ID
        if plant:
            return plant.to_dict(), 200  # Return the plant data with HTTP 200 status
        return {"error": "Plant not found"}, 404  # Return error if the plant does not exist

# Register the resources with their routes
api.add_resource(Plants, '/plants')  # Routes for the Plants resource
api.add_resource(PlantByID, '/plants/<int:id>')  # Routes for specific Plant by ID

if __name__ == '__main__':
    app.run(port=5555, debug=True)  # Run the app on port 5555
