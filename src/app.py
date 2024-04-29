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
#-------------------CREATE USER-----------------------
@app.route('/users', methods=['POST'])  # Define un endpoint para agregar un nuevo personaje mediante una solicitud POST a la ruta '/users'
def create_new_user():  # Define la función que manejará la solicitud
    data = request.json  # Obtén los datos JSON enviados en la solicitud
    if not data:  # Verifica si no se proporcionaron datos JSON
        return jsonify({'error': 'No data provided'}), 400  # Devuelve un error con código de estado 400 si no se proporcionaron datos

    # Crear un nuevo objeto User y asignar los valores del JSON
    new_user = User()  # Crea una nueva instancia de la clase User
    for key, value in data.items():  #items() para iterar sobre cada par llave-valor en el JSON recibido
        if hasattr(new_user, key):  # Verifica si el campo existe en el modelo de User
            setattr(new_user, key, value)  # Asigna el valor del campo al objeto User utilizando setattr

    # Agregar el nuevo user a la base de datos
    db.session.add(new_user)  # Agrega el objeto User a la sesión de la base de datos
    db.session.commit()  # Confirma los cambios en la base de datos

    return jsonify({'message': 'New user created successfully', 'user_id': new_user.id}), 201  # Devuelve un mensaje de éxito con el ID del nuevo usuario y un código de estado 201


#-------------------CONSULTAR TODOS LOS USUARIOS-----------------------
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        if not users:
            return jsonify({'message': 'No users found'}), 404
        
        response_body = [user.serialize() for user in users]
        return jsonify(response_body), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

 #-------------------CONSULTAR TODOS LOS FAV -----------------------
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
    

#-------------------METODO POST USUARIO FAVORITO PLANET-----------------------

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])  # Define un endpoint para agregar un planeta favorito mediante una solicitud POST a la ruta '/favorite/planet/<planet_id>'
def add_favorite_planet(planet_id):  # Define la función que manejará la solicitud, tomando el ID del planeta como argumento
    try:  # Inicia un bloque try para manejar excepciones que puedan ocurrir durante la ejecución del código
        data = request.json  # Obtiene los datos JSON enviados en la solicitud
        if not data:  # Verifica si no se proporcionaron datos JSON
            return jsonify({'error': 'No data provided'}), 400  # Devuelve un error con código de estado 400 si no se proporcionaron datos

        user_id = data.get('user_id')  # Obtiene el ID del usuario de los datos JSON
        if not user_id:  # Verifica si no se proporcionó el ID del usuario
            return jsonify({'error': 'User ID is required'}), 400  # Devuelve un error con código de estado 400 si el ID del usuario no está presente

        user = User.query.get(user_id)  # Busca el usuario en la base de datos utilizando su ID
        if not user:  # Verifica si el usuario no fue encontrado en la base de datos
            return jsonify({'error': 'User not found'}), 404  # Devuelve un error con código de estado 404 si el usuario no fue encontrado

        planet = Planet.query.get(planet_id)  # Busca el planeta en la base de datos utilizando su ID
        if not planet:  # Verifica si el planeta no fue encontrado en la base de datos
            return jsonify({'error': 'Planet not found'}), 404  # Devuelve un error con código de estado 404 si el planeta no fue encontrado

        new_favorite = Favoritos(user_id = user_id, planet_id = planet_id)
        db.session.add(new_favorite)
        db.session.commit()  # Confirma los cambios en la base de datos

        return jsonify({'message': 'Planet added to favorites'}), 201  # Devuelve un mensaje de éxito con código de estado 201
    except Exception as e:  # Captura cualquier excepción que pueda ocurrir durante la ejecución del bloque try
        return jsonify({'error': str(e)}), 500  # Devuelve un error con código de estado 500 si ocurre una excepción, convirtiendo la excepción en una cadena de texto para la respuesta JSON


#-------------------METODO POST USUARIO FAVORITO CHARACTER-----------------------

@app.route('/favorite/character/<int:character_id>', methods=['POST'])  # Define un endpoint para agregar un character favorito mediante una solicitud POST a la ruta '/favorite/planet/<planet_id>'
def add_favorite_character(character_id):  # Define la función que manejará la solicitud, tomando el ID del character como argumento
    try:  # Inicia un bloque try para manejar excepciones que puedan ocurrir durante la ejecución del código
        data = request.json  # Obtiene los datos JSON enviados en la solicitud
        if not data:  # Verifica si no se proporcionaron datos JSON
            return jsonify({'error': 'No data provided'}), 400  # Devuelve un error con código de estado 400 si no se proporcionaron datos

        user_id = data.get('user_id')  # Obtiene el ID del usuario de los datos JSON
        if not user_id:  # Verifica si no se proporcionó el ID del usuario
            return jsonify({'error': 'User ID is required'}), 400  # Devuelve un error con código de estado 400 si el ID del usuario no está presente

        user = User.query.get(user_id)  # Busca el usuario en la base de datos utilizando su ID
        if not user:  # Verifica si el usuario no fue encontrado en la base de datos
            return jsonify({'error': 'User not found'}), 404  # Devuelve un error con código de estado 404 si el usuario no fue encontrado

        character = Character.query.get(character_id)  # Busca el planeta en la base de datos utilizando su ID
        if not character:  # Verifica si el planeta no fue encontrado en la base de datos
            return jsonify({'error': 'character not found'}), 404  # Devuelve un error con código de estado 404 si el character no fue encontrado

        new_favorite = Favoritos(user_id = user_id, character_id = character_id)
        db.session.add(new_favorite)
        db.session.commit()  # Confirma los cambios en la base de datos

        return jsonify({'message': 'character added to favorites'}), 201  # Devuelve un mensaje de éxito con código de estado 201
    except Exception as e:  # Captura cualquier excepción que pueda ocurrir durante la ejecución del bloque try
        return jsonify({'error': str(e)}), 500  # Devuelve un error con código de estado 500 si ocurre una excepción, convirtiendo la excepción en una cadena de texto para la respuesta JSON


#-------------------METODO DELETE PLANET DE UN USUARIO-----------------------

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(planet_id):
    try:
        # Obtiene los datos JSON enviados en la solicitud
        data = request.json
        # Verifica si no se proporcionaron datos JSON
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Obtiene el ID del usuario de los datos JSON
        user_id = data.get('user_id')
        # Verifica si no se proporcionó el ID del usuario
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400

        # Busca el usuario en la base de datos utilizando su ID
        user = User.query.get(user_id)
        # Verifica si el usuario no fue encontrado en la base de datos
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Busca el favorito correspondiente al usuario y al planeta específico en la base de datos
        favorite = Favoritos.query.filter_by(user_id=user_id, planet_id=planet_id).first()
        # Verifica si el favorito no fue encontrado en la base de datos
        if not favorite:
            return jsonify({'error': 'Favorite not found'}), 404

        # Elimina el favorito de la base de datos
        db.session.delete(favorite)
        # Confirma los cambios en la base de datos
        db.session.commit()

        # Devuelve un mensaje de éxito con código de estado 200
        return jsonify({'message': 'Favorite planet removed successfully'}), 200
    except Exception as e:
        # Devuelve un error con código de estado 500 si ocurre una excepción
        return jsonify({'error': str(e)}), 500


#-------------------METODO DELETE CHARACTERS DE UN USUARIO-----------------------

@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def remove_favorite_character(character_id):
    try:
        # Obtiene los datos JSON enviados en la solicitud
        data = request.json
        # Verifica si no se proporcionaron datos JSON
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Obtiene el ID del usuario de los datos JSON
        user_id = data.get('user_id')
        # Verifica si no se proporcionó el ID del usuario
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400

        # Busca el usuario en la base de datos utilizando su ID
        user = User.query.get(user_id)
        # Verifica si el usuario no fue encontrado en la base de datos
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Busca el favorito correspondiente al usuario y al planeta específico en la base de datos
        favorite = Favoritos.query.filter_by(user_id=user_id, character_id=character_id).first()
        # Verifica si el favorito no fue encontrado en la base de datos
        if not favorite:
            return jsonify({'error': 'Favorite not found'}), 404

        # Elimina el favorito de la base de datos
        db.session.delete(favorite)
        # Confirma los cambios en la base de datos
        db.session.commit()

        # Devuelve un mensaje de éxito con código de estado 200
        return jsonify({'message': 'Favorite character removed successfully'}), 200
    except Exception as e:
        # Devuelve un error con código de estado 500 si ocurre una excepción
        return jsonify({'error': str(e)}), 500


#-----------------------------------------------------------METODOS PARA CHARACTERS-------------------------------------------------------------

# Obtener todos los personajes ### OK ###
@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    serialized_characters = [character.serialize() for character in characters]
    return jsonify(serialized_characters)


# Obtener un personaje por su ID ### OK ###
@app.route('/character/<int:character_id>', methods=['GET'])  # Define un endpoint para obtener un personaje mediante una solicitud GET a la ruta '/character/<character_id>'
def get_character(character_id):  # Define la función que manejará la solicitud, tomando el ID del personaje como argumento
    character = Character.query.get(character_id)  # Busca el personaje en la base de datos utilizando su ID
    if not character:  # Verifica si el personaje no fue encontrado en la base de datos
        return jsonify({'error': 'Character not found'}), 404  # Devuelve un error con código de estado 404 si el personaje no fue encontrado
    return jsonify(character.serialize())  # Devuelve una representación JSON del personaje utilizando su método serialize()



# Agregar un nuevo personaje ### OK ###
@app.route('/characters', methods=['POST'])  # Define un endpoint para agregar un nuevo personaje mediante una solicitud POST a la ruta '/characters'
def add_character():  # Define la función que manejará la solicitud
    data = request.json  # Obtén los datos JSON enviados en la solicitud
    if not data:  # Verifica si no se proporcionaron datos JSON
        return jsonify({'error': 'No data provided'}), 400  # Devuelve un error con código de estado 400 si no se proporcionaron datos

    # Crear un nuevo objeto Character y asignar los valores del JSON
    character = Character()  # Crea una nueva instancia de la clase Character
    for key, value in data.items():  #items() para iterar sobre cada par llave-valor en el JSON recibido
        if hasattr(character, key):  # Verifica si el campo existe en el modelo de Character
            setattr(character, key, value)  # Asigna el valor del campo al objeto Character utilizando setattr

    # Agregar el nuevo personaje a la base de datos
    db.session.add(character)  # Agrega el objeto Character a la sesión de la base de datos
    db.session.commit()  # Confirma los cambios en la base de datos

    return jsonify({'message': 'Character created successfully', 'character_id': character.id}), 201  # Devuelve un mensaje de éxito con el ID del nuevo personaje y un código de estado 201


# Actualizar un personaje existente ### OK ###
@app.route('/character/<int:character_id>', methods=['PUT'])  # Define un endpoint para actualizar un personaje mediante una solicitud PUT a la ruta '/character/<character_id>'
def update_character(character_id):  # Define la función que manejará la solicitud, tomando el ID del personaje como argumento
    character = Character.query.get(character_id)  # Busca el personaje en la base de datos utilizando su ID
    if not character:  # Verifica si el personaje no fue encontrado en la base de datos
        return jsonify({'error': 'Character not found'}), 404  # Devuelve un error con código de estado 404 si el personaje no fue encontrado

    data = request.json  # Obtén los datos JSON enviados en la solicitud
    if not data:  # Verifica si no se proporcionaron datos JSON
        return jsonify({'error': 'No data provided'}), 400  # Devuelve un error con código de estado 400 si no se proporcionaron datos

    # Iterar sobre cada campo en el JSON y actualizar el personaje si corresponde
    for key, value in data.items():  #items() para iterar sobre cada par llave-valor en el JSON recibido
        # Verificar si el campo existe en la clase Character
        if hasattr(character, key):  # Verifica si el personaje tiene un atributo con el nombre de la llave
            setattr(character, key, value)  # Asigna el valor del campo al atributo correspondiente del personaje utilizando setattr()

    db.session.commit()  # Confirma los cambios en la base de datos
    return jsonify({'message': 'Character updated successfully'})  # Devuelve un mensaje de éxito indicando que el personaje se actualizó correctamente


# Eliminar un personaje existente ### OK ###
@app.route('/character/<int:character_id>', methods=['DELETE'])  # Define un endpoint para eliminar un personaje mediante una solicitud DELETE a la ruta '/character/<character_id>'
def delete_character(character_id):  # Define la función que manejará la solicitud, tomando el ID del personaje como argumento
    character = Character.query.get(character_id)  # Busca el personaje en la base de datos utilizando su ID
    if not character:  # Verifica si el personaje no fue encontrado en la base de datos
        return jsonify({'error': 'Character not found'}), 404  # Devuelve un error con código de estado 404 si el personaje no fue encontrado

    db.session.delete(character)  # Elimina el personaje de la base de datos
    db.session.commit()  # Confirma los cambios en la base de datos
    return jsonify({'message': 'Character deleted successfully'})  # Devuelve un mensaje de éxito indicando que el personaje se eliminó correctamente


#-----------------------------------------------------------METODOS PARA PLANETS-------------------------------------------------------------

# Obtener todos los planetas ### OK ###
@app.route('/planets', methods=['GET'])  # Define un endpoint para obtener todos los planetas mediante una solicitud GET a la ruta '/planets'
def get_planets():  # Define la función que manejará la solicitud
    planets = Planet.query.all()  # Obtén todos los planetas de la base de datos
    serialized_planets = [planet.serialize() for planet in planets]  # Serializa cada planeta en una lista de diccionarios JSON
    return jsonify(serialized_planets)  # Devuelve la lista de planetas serializados como JSON


# Obtener un planeta por su ID ### OK ###
@app.route('/planet/<int:planet_id>', methods=['GET'])  # Define un endpoint para obtener un planeta por su ID mediante una solicitud GET a la ruta '/planet/<planet_id>'
def get_planet(planet_id):  # Define la función que manejará la solicitud, tomando el ID del planeta como argumento
    planet = Planet.query.get(planet_id)  # Busca el planeta en la base de datos utilizando su ID
    if not planet:  # Verifica si el planeta no fue encontrado en la base de datos
        return jsonify({'error': 'Planet not found'}), 404  # Devuelve un error con código de estado 404 si el planeta no fue encontrado
    return jsonify(planet.serialize())  # Devuelve una representación JSON del planeta utilizando su método serialize()



# Agregar un nuevo planeta ### OK ###
@app.route('/planets', methods=['POST'])  # Define un endpoint para agregar un nuevo planeta mediante una solicitud POST a la ruta '/planets'
def add_planet():  # Define la función que manejará la solicitud
    data = request.json  # Obtén los datos JSON enviados en la solicitud
    if not data:  # Verifica si no se proporcionaron datos JSON
        return jsonify({'error': 'No data provided'}), 400  # Devuelve un error con código de estado 400 si no se proporcionaron datos

    # Crear un nuevo objeto Planet y asignar los valores del JSON
    planet = Planet()  # Crea una nueva instancia de la clase Planet
    for key, value in data.items():  # Itera sobre cada par clave-valor en los datos JSON
        if hasattr(planet, key):  # Verifica si el campo existe en el modelo de Planet
            setattr(planet, key, value)  # Asigna el valor del campo al objeto Planet utilizando setattr

    # Agregar el nuevo planeta a la base de datos
    db.session.add(planet)  # Agrega el objeto Planet a la sesión de la base de datos
    db.session.commit()  # Confirma los cambios en la base de datos

    return jsonify({'message': 'Planet created successfully', 'planet_id': planet.id}), 201  # Devuelve un mensaje de éxito con el ID del nuevo planeta y un código de estado 201


# Actualizar un planeta existente ### OK ###
@app.route('/planet/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    planet = Planet.query.get(planet_id)  # Busca el planeta en la base de datos utilizando su ID
    if not planet:  # Verifica si el planeta no fue encontrado en la base de datos
        return jsonify({'error': 'Planet not found'}), 404  # Devuelve un error con código de estado 404 si el planeta no fue encontrado

    data = request.json  # Obtén los datos JSON enviados en la solicitud
    if not data:  # Verifica si no se proporcionaron datos JSON
        return jsonify({'error': 'No data provided'}), 400  # Devuelve un error con código de estado 400 si no se proporcionaron datos

    # Iterar sobre cada campo en el JSON y actualizar el personaje si corresponde
    for key, value in data.items(): #items() para iterar sobre cada par llave-valor en el JSON recibido
        # Verificar si el campo existe en la clase Character
        if hasattr(planet, key): #hasattr(). Si el campo existe
            setattr(planet, key, value)#lo actualizamos utilizando setattr()

    db.session.commit()  # Confirma los cambios en la base de datos
    return jsonify({'message': 'Planet updated successfully'})  # Devuelve un mensaje de éxito indicando que el planeta se actualizó correctamente


# Eliminar un planeta existente ### OK ###
@app.route('/planet/<int:planet_id>', methods=['DELETE'])  # Define un endpoint para eliminar un planeta existente mediante una solicitud DELETE a la ruta '/planet/<planet_id>'
def delete_planet(planet_id):  # Define la función que manejará la solicitud, tomando el ID del planeta como argumento
    planet = Planet.query.get(planet_id)  # Busca el planeta en la base de datos utilizando su ID
    if not planet:  # Verifica si el planeta no fue encontrado en la base de datos
        return jsonify({'error': 'Planet not found'}), 404  # Devuelve un error con código de estado 404 si el planeta no fue encontrado

    db.session.delete(planet)  # Elimina el planeta de la base de datos
    db.session.commit()  # Confirma los cambios en la base de datos
    return jsonify({'message': 'Planet deleted successfully'})  # Devuelve un mensaje de éxito indicando que el planeta se eliminó correctamente




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
