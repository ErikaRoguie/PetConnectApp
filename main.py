import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_restx import Api, Resource, fields
import uuid
import logging
from models import db, SuperPet, Inventory

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images/pets'
db.init_app(app)

# Initialize Flask-RestX
api = Api(app, version='1.0', title='Pet Connect API',
          description='A web application for managing and displaying pet information')

# Create namespaces
pets_ns = api.namespace('api/pets', description='Pet operations')
inventory_ns = api.namespace('api/inventory', description='Inventory operations')

# Define models for Swagger documentation
pet_model = api.model('Pet', {
    'id': fields.Integer(readonly=True, description='The pet identifier'),
    'name': fields.String(required=True, description='The pet name'),
    'species': fields.String(required=True, description='The pet species'),
    'breed': fields.String(description='The pet breed'),
    'age': fields.Integer(description='The pet age'),
    'gender': fields.String(description='The pet gender'),
    'color': fields.String(description='The pet color'),
    'hero_name': fields.String(description='The pet hero name'),
    'superpower': fields.String(description='The pet superpower'),
    'hero_type': fields.String(description='The type of hero'),
    'hero_appearance': fields.String(description='Description of hero appearance'),
    'image_url': fields.String(description='URL to pet image')
})

inventory_model = api.model('Inventory', {
    'id': fields.Integer(readonly=True, description='The inventory item identifier'),
    'pet_id': fields.Integer(required=True, description='The associated pet ID'),
    'quantity': fields.Integer(required=True, description='The quantity in stock'),
    'is_premade': fields.Boolean(description='Whether the item is premade')
})

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pets')
def pets():
    return render_template('pets.html')

@app.route('/catalogue')
def catalogue():
    try:
        app.logger.info("Attempting to fetch all pets from the database")
        pets = SuperPet.query.all()
        app.logger.info(f"Successfully fetched {len(pets)} pets")
        return render_template('catalogue.html', pets=pets)
    except Exception as e:
        app.logger.error(f"Error in catalogue route: {str(e)}")
        return f"An error occurred while loading the catalogue: {str(e)}", 500

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/inventory')
def inventory():
    return render_template('inventory.html')

@pets_ns.route('/')
class PetList(Resource):
    @pets_ns.doc('list_pets')
    @pets_ns.param('search', 'Search term for filtering pets')
    @pets_ns.marshal_list_with(pet_model)
    def get(self):
        """List all pets"""
        try:
            search = request.args.get('search', '')
            pets = SuperPet.query.filter(SuperPet.name.ilike(f'%{search}%')).all()
            return [pet.to_dict() for pet in pets]
        except Exception as e:
            api.abort(500, f"An error occurred while fetching pets: {str(e)}")

    @pets_ns.doc('create_pet')
    @pets_ns.expect(pet_model)
    @pets_ns.marshal_with(pet_model, code=201)
    def post(self):
        """Create a new pet"""
        try:
            data = request.form.to_dict()
            pet = SuperPet(**data)
            
            if 'image' in request.files:
                file = request.files['image']
                if file and allowed_file(file.filename):
                    filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    pet.image_url = f"/static/images/pets/{filename}"
            
            db.session.add(pet)
            db.session.commit()
            return pet.to_dict(), 201
        except Exception as e:
            api.abort(500, f"An error occurred while creating the pet: {str(e)}")

@pets_ns.route('/<int:pet_id>')
@pets_ns.param('pet_id', 'The pet identifier')
class Pet(Resource):
    @pets_ns.doc('get_pet')
    @pets_ns.marshal_with(pet_model)
    def get(self, pet_id):
        """Fetch a pet by ID"""
        try:
            pet = SuperPet.query.get_or_404(pet_id)
            return pet.to_dict()
        except Exception as e:
            api.abort(500, f"An error occurred while fetching the pet: {str(e)}")

    @pets_ns.doc('update_pet')
    @pets_ns.expect(pet_model)
    @pets_ns.marshal_with(pet_model)
    def put(self, pet_id):
        """Update a pet"""
        try:
            pet = SuperPet.query.get_or_404(pet_id)
            data = request.form.to_dict()
            
            if 'image' in request.files:
                file = request.files['image']
                if file and allowed_file(file.filename):
                    filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    if pet.image_url:
                        try:
                            os.remove(os.path.join(app.root_path, pet.image_url.lstrip('/')))
                        except OSError:
                            pass
                    pet.image_url = f"/static/images/pets/{filename}"
            
            for key, value in data.items():
                setattr(pet, key, value)
            
            db.session.commit()
            return pet.to_dict()
        except Exception as e:
            api.abort(500, f"An error occurred while updating the pet: {str(e)}")

    @pets_ns.doc('delete_pet')
    @pets_ns.response(204, 'Pet deleted')
    def delete(self, pet_id):
        """Delete a pet"""
        try:
            pet = SuperPet.query.get_or_404(pet_id)
            if pet.image_url:
                try:
                    os.remove(os.path.join(app.root_path, pet.image_url.lstrip('/')))
                except OSError:
                    pass
            db.session.delete(pet)
            db.session.commit()
            return '', 204
        except Exception as e:
            api.abort(500, f"An error occurred while deleting the pet: {str(e)}")

@inventory_ns.route('/')
class InventoryList(Resource):
    @inventory_ns.doc('list_inventory')
    @inventory_ns.marshal_list_with(inventory_model)
    def get(self):
        """List all inventory items"""
        try:
            inventory_items = Inventory.query.all()
            return [item.to_dict() for item in inventory_items]
        except Exception as e:
            api.abort(500, f"An error occurred while fetching inventory items: {str(e)}")

    @inventory_ns.doc('create_inventory_item')
    @inventory_ns.expect(inventory_model)
    @inventory_ns.marshal_with(inventory_model, code=201)
    def post(self):
        """Create a new inventory item"""
        try:
            data = request.json
            inventory_item = Inventory(**data)
            db.session.add(inventory_item)
            db.session.commit()
            return inventory_item.to_dict(), 201
        except Exception as e:
            api.abort(500, f"An error occurred while creating the inventory item: {str(e)}")

@inventory_ns.route('/<int:item_id>')
@inventory_ns.param('item_id', 'The inventory item identifier')
class InventoryItem(Resource):
    @inventory_ns.doc('get_inventory_item')
    @inventory_ns.marshal_with(inventory_model)
    def get(self, item_id):
        """Fetch an inventory item by ID"""
        try:
            item = Inventory.query.get_or_404(item_id)
            return item.to_dict()
        except Exception as e:
            api.abort(500, f"An error occurred while fetching the inventory item: {str(e)}")

    @inventory_ns.doc('update_inventory_item')
    @inventory_ns.expect(inventory_model)
    @inventory_ns.marshal_with(inventory_model)
    def put(self, item_id):
        """Update an inventory item"""
        try:
            inventory_item = Inventory.query.get_or_404(item_id)
            data = request.json
            for key, value in data.items():
                setattr(inventory_item, key, value)
            db.session.commit()
            return inventory_item.to_dict()
        except Exception as e:
            api.abort(500, f"An error occurred while updating the inventory item: {str(e)}")

    @inventory_ns.doc('delete_inventory_item')
    @inventory_ns.response(204, 'Inventory item deleted')
    def delete(self, item_id):
        """Delete an inventory item"""
        try:
            inventory_item = Inventory.query.get_or_404(item_id)
            db.session.delete(inventory_item)
            db.session.commit()
            return '', 204
        except Exception as e:
            api.abort(500, f"An error occurred while deleting the inventory item: {str(e)}")

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

if __name__ == '__main__':
    with app.app_context():
        try:
            app.logger.info(f"Attempting to connect to database: {app.config['SQLALCHEMY_DATABASE_URI']}")
            db.drop_all()  # Drop all existing tables
            db.create_all()  # Create all tables from scratch
            app.logger.info("Database tables dropped and recreated successfully")
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            app.logger.info("Upload folder created successfully")
        except Exception as e:
            app.logger.error(f"Error during setup: {str(e)}")
    app.run(host='0.0.0.0', port=5000, debug=True)
