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
from models import db, User, Film, Starship, Vehicle, Species, Planet, Character, Favoritos
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

#------------------------------------------------------------------------USERS-------------------------------------------------------------

#-------------------CONSULTAR TODOS LOS USUARIOS-----------------------
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        if not users:
            return jsonify({'message': 'No users found'}), 404
        
        response_body = [{'id': user.id, 'name': user.name} for user in users]
        return jsonify(response_body), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


@app.route('/favoritos', methods=['GET'])
def get_favorites():
    try:
        # Obtener todos los favoritos de la base de datos
        favoritos = Favoritos.query.all()
        
        # Serializar los favoritos
        serialized_favoritos = [favorito.serialize() for favorito in favoritos]
        
        # Responder con los favoritos en formato JSON
        return jsonify(serialized_favoritos), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



 #-------------------CONSULTAR FAV DEL UN USUARIO-----------------------
 #https://fantastic-umbrella-695qvg7q9qvh5v9-3000.app.github.dev/users/favoritos?user_id=1
@app.route('/users/favoritos', methods=['GET'])
def get_user_favorites():
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'message': 'User ID is required'}), 400

        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        favoritos = user.favoritos
        serialized_favoritos = [favorito.serialize() for favorito in favoritos]
        return jsonify(serialized_favoritos), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

#-------------------METODO POST DE UN USUARIO-----------------------

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    try:
        user_id = request.json.get('user_id')
        if not user_id:
            return jsonify({'message': 'User ID is required'}), 400
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        planet = Planet.query.get(planet_id)
        if not planet:
            return jsonify({'message': 'Planet not found'}), 404
        
        user.favoritos.append(planet)
        db.session.commit()
        
        return jsonify({'message': 'Planet added to favorites'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/favorite/characters/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):
    try:
        user_id = request.json.get('user_id')
        if not user_id:
            return jsonify({'message': 'User ID is required'}), 400
        
        # Buscar el usuario en la base de datos
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        # Buscar el personaje en la base de datos
        character = Character.query.get(character_id)
        if not character:
            return jsonify({'message': 'Character not found'}), 404
        
        # Agregar el personaje a los favoritos del usuario
        user.favoritos.append(character)
        db.session.commit()
        
        return jsonify({'message': 'Character added to favorites'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


#-------------------METODO DELETE DE UN USUARIO-----------------------

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    try:
        user_id = request.json.get('user_id')
        if not user_id:
            return jsonify({'message': 'User ID is required'}), 400
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        planet = Planet.query.get(planet_id)
        if not planet:
            return jsonify({'message': 'Planet not found'}), 404
        
        if planet in user.favoritos:
            user.favoritos.remove(planet)
            db.session.commit()
            return jsonify({'message': 'Planet removed from favorites'}), 200
        else:
            return jsonify({'message': 'Planet is not in favorites'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/favorite/characters/<int:people_id>', methods=['DELETE'])
def delete_favorite_character(people_id):
    try:
        user_id = request.json.get('user_id')
        if not user_id:
            return jsonify({'message': 'User ID is required'}), 400
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        character = Character.query.get(people_id)
        if not character:
            return jsonify({'message': 'Character not found'}), 404
        
        if character in user.favoritos:
            user.favoritos.remove(character)
            db.session.commit()
            return jsonify({'message': 'Character removed from favorites'}), 200
        else:
            return jsonify({'message': 'Character is not in favorites'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        

#------------------------------------------------------------------------CHARACTERS-------------------------------------------------------------


# Obtener todos los personajes
@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    serialized_characters = [character.serialize() for character in characters]
    return jsonify(serialized_characters)

# Obtener un personaje por su ID
@app.route('/character/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({'error': 'Character not found'}), 404
    return jsonify(character.serialize())

# Agregar un nuevo personaje
@app.route('/characters', methods=['POST'])
def add_character():
    data = request.json
    name = data.get('name')
    planet_id = data.get('homeworld_id')

    if not name or not planet_id:
        return jsonify({'error': 'Name and homeworld_id are required'}), 400

    character = Character(name=name, homeworld_id=planet_id)
    db.session.add(character)
    db.session.commit()
    return jsonify({'message': 'Character added successfully', 'id': character.id}), 201

# Actualizar un personaje existente
@app.route('/character/<int:character_id>', methods=['PUT'])
def update_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({'error': 'Character not found'}), 404

    data = request.json
    name = data.get('name')
    planet_id = data.get('homeworld_id')

    if name:
        character.name = name
    if planet_id:
        character.homeworld_id = planet_id

    db.session.commit()
    return jsonify({'message': 'Character updated successfully'})

# Eliminar un personaje existente
@app.route('/character/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({'error': 'Character not found'}), 404

    db.session.delete(character)
    db.session.commit()
    return jsonify({'message': 'Character deleted successfully'})

#------------------------------------------------------------------------PLANETS-------------------------------------------------------------

# Obtener todos los planetas
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    serialized_planets = [planet.serialize() for planet in planets]
    return jsonify(serialized_planets)


# Obtener un planeta por su ID
@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({'error': 'Planet not found'}), 404
    return jsonify(planet.serialize())

# Agregar un nuevo planeta
@app.route('/planets', methods=['POST'])
def add_planet():
    data = request.json
    name = data.get('name')
    diameter = data.get('diameter')
    rotation_period = data.get('rotation_period')
    orbital_period = data.get('orbital_period')
    gravity = data.get('gravity')
    population = data.get('population')
    climate = data.get('climate')
    terrain = data.get('terrain')
    surface_water = data.get('surface_water')
    created = datetime.utcnow()
    edited = datetime.utcnow()
    url = data.get('url')

    if not all([name, diameter, rotation_period, orbital_period, gravity, population, climate, terrain, surface_water, url]):
        return jsonify({'error': 'All fields are required'}), 400

    planet = Planet(name=name, diameter=diameter, rotation_period=rotation_period, orbital_period=orbital_period, gravity=gravity,
                    population=population, climate=climate, terrain=terrain, surface_water=surface_water, created=created, edited=edited, url=url)
    db.session.add(planet)
    db.session.commit()
    return jsonify({'message': 'Planet added successfully', 'id': planet.id}), 201

# Actualizar un planeta existente
@app.route('/planet/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({'error': 'Planet not found'}), 404

    data = request.json
    planet.name = data.get('name', planet.name)
    planet.diameter = data.get('diameter', planet.diameter)
    planet.rotation_period = data.get('rotation_period', planet.rotation_period)
    planet.orbital_period = data.get('orbital_period', planet.orbital_period)
    planet.gravity = data.get('gravity', planet.gravity)
    planet.population = data.get('population', planet.population)
    planet.climate = data.get('climate', planet.climate)
    planet.terrain = data.get('terrain', planet.terrain)
    planet.surface_water = data.get('surface_water', planet.surface_water)
    planet.edited = datetime.utcnow()
    planet.url = data.get('url', planet.url)

    db.session.commit()
    return jsonify({'message': 'Planet updated successfully'})

# Eliminar un planeta existente
@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({'error': 'Planet not found'}), 404

    db.session.delete(planet)
    db.session.commit()
    return jsonify({'message': 'Planet deleted successfully'})



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
