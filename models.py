from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SuperPet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    color = db.Column(db.String(50))
    hero_name = db.Column(db.String(100))
    superpower = db.Column(db.String(100))
    hero_type = db.Column(db.String(50))
    hero_appearance = db.Column(db.String(200))
    image_url = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'species': self.species,
            'breed': self.breed,
            'age': self.age,
            'gender': self.gender,
            'color': self.color,
            'hero_name': self.hero_name,
            'superpower': self.superpower,
            'hero_type': self.hero_type,
            'hero_appearance': self.hero_appearance,
            'image_url': self.image_url
        }

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('super_pet.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    is_premade = db.Column(db.Boolean, nullable=False, default=False)

    pet = db.relationship('SuperPet', backref=db.backref('inventory_items', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'pet_id': self.pet_id,
            'quantity': self.quantity,
            'is_premade': self.is_premade
        }
