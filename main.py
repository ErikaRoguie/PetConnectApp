import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import uuid
import logging
from models import db, SuperPet, Inventory

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images/pets'
db.init_app(app)

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

@app.route('/api/pets', methods=['GET'])
def get_pets():
    try:
        search = request.args.get('search', '')
        pets = SuperPet.query.filter(SuperPet.name.ilike(f'%{search}%')).all()
        return jsonify([pet.to_dict() for pet in pets])
    except Exception as e:
        app.logger.error(f"Error in get_pets route: {str(e)}")
        return jsonify({"error": f"An error occurred while fetching pets: {str(e)}"}), 500

@app.route('/api/pets', methods=['POST'])
def create_pet():
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
        return jsonify(pet.to_dict()), 201
    except Exception as e:
        app.logger.error(f"Error in create_pet route: {str(e)}")
        return jsonify({"error": f"An error occurred while creating the pet: {str(e)}"}), 500

@app.route('/api/pets/<int:pet_id>', methods=['PUT'])
def update_pet(pet_id):
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
        return jsonify(pet.to_dict())
    except Exception as e:
        app.logger.error(f"Error in update_pet route: {str(e)}")
        return jsonify({"error": f"An error occurred while updating the pet: {str(e)}"}), 500

@app.route('/api/pets/<int:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
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
        app.logger.error(f"Error in delete_pet route: {str(e)}")
        return jsonify({"error": f"An error occurred while deleting the pet: {str(e)}"}), 500

@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    try:
        inventory_items = Inventory.query.all()
        return jsonify([item.to_dict() for item in inventory_items])
    except Exception as e:
        app.logger.error(f"Error in get_inventory route: {str(e)}")
        return jsonify({"error": f"An error occurred while fetching inventory items: {str(e)}"}), 500

@app.route('/api/inventory', methods=['POST'])
def create_inventory_item():
    try:
        data = request.json
        inventory_item = Inventory(**data)
        db.session.add(inventory_item)
        db.session.commit()
        return jsonify(inventory_item.to_dict()), 201
    except Exception as e:
        app.logger.error(f"Error in create_inventory_item route: {str(e)}")
        return jsonify({"error": f"An error occurred while creating the inventory item: {str(e)}"}), 500

@app.route('/api/inventory/<int:item_id>', methods=['PUT'])
def update_inventory_item(item_id):
    try:
        inventory_item = Inventory.query.get_or_404(item_id)
        data = request.json
        for key, value in data.items():
            setattr(inventory_item, key, value)
        db.session.commit()
        return jsonify(inventory_item.to_dict())
    except Exception as e:
        app.logger.error(f"Error in update_inventory_item route: {str(e)}")
        return jsonify({"error": f"An error occurred while updating the inventory item: {str(e)}"}), 500

@app.route('/api/inventory/<int:item_id>', methods=['DELETE'])
def delete_inventory_item(item_id):
    try:
        inventory_item = Inventory.query.get_or_404(item_id)
        db.session.delete(inventory_item)
        db.session.commit()
        return '', 204
    except Exception as e:
        app.logger.error(f"Error in delete_inventory_item route: {str(e)}")
        return jsonify({"error": f"An error occurred while deleting the inventory item: {str(e)}"}), 500

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
