"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, People, Vehicle
from sqlalchemy.exc import IntegrityError
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_all():

    users= User.query.all()
    return jsonify([user.serialize() for user in users]),200

   #response_body = {
        #"msg": "Hello, this is your GET /user response "
   # }

   #eturn jsonify(response_body), 200
@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Faltan campos obligatorios"}), 400
    
    try:
        new_user = User(
            email=data["email"],
            password=data["password"],
            is_active=data.get("is_active", True),
            firts_name=data["firts_name"],
            second_name=data["second_name"]
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.serialize()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/user/<int:user_id>',methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "usuario no encontrado"}), 404
    
    return jsonify(user.serialize()), 200

@app.route('/people', methods=['GET'])
def get_all_people():
    people = People.query.all()
    result = [person.serialize() for person in people]
    return jsonify(result), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    if not person:
        return jsonify({"error": "Personaje no encontrado"}), 404
    return jsonify(person.serialize()), 200

@app.route('/planet', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    result = [planet.serialize() for planet in planets]
    return jsonify(result), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planeta no encontrado"}), 404
    return jsonify(planet.serialize()), 200

@app.route('/people', methods=['POST'])
def create_person():
    data = request.get_json()

    if not data.get("name") or not data.get("planet_id"):
        return jsonify({"error": "Faltan campos requeridos"}), 400
    
    new_person = People(
        name=data["name"],
        gender=data.get("gender"),
        height=data.get("height"),
        mass=data.get("mass"),
        birth_year=data.get("birth_year"),
        planet_id=data["planet_id"]
    )
    db.session.add(new_person)
    db.session.commit()
    return jsonify(new_person.serialize()), 201

@app.route('/people/<int:person_id>', methods=['PUT'])
def update_person(person_id):
    person = People.query.get(person_id)
    if not person:
        return jsonify({"error": "Personaje no encontrado"}), 404
    
    data = request.get_json()
    person.name = data.get("name", person.name)
    person.gender = data.get("gender", person.gender)
    person.height = data.get("height", person.height)
    person.mass = data.get("mass",person.mass)
    person.planet_id = data.get("planet_id", person.planet_id)

    db.session.commit()
    return jsonify(person.serialize()), 200

@app.route('/people/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    person = People.query.get(person_id)
    if not person:
        return jsonify({"error": "Personaje no encontrada"}), 404
    
    db.session.delete(person)
    db.session.commit()
    return jsonify({"msg": "Personaje eliminado"}),200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
