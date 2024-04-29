from flask_sqlalchemy import SQLAlchemy  # Importar la clase SQLAlchemy desde el módulo flask_sqlalchemy

# Definir la clase de personaje (tabla de personajes en la base de datos)
from datetime import datetime
import json

# Crear una instancia de SQLAlchemy que será utilizada para interactuar con la base de datos
db = SQLAlchemy()

#Definimos la relacion de usuario y favorito en la tabla usuario_favoritos antes de cada tabla
# usuario_favoritos = db.Table('usuario_favoritos', db.metadata, #.metadata en SQLAlchemy es un objeto que almacena metadatos sobre las tablas y sus columnas en una base de datos. Aquí te explico cómo funciona
#                         # Columna 'usuario_id' para almacenar el ID del usuario que tiene el favorito
#                         db.Column('usuario_id', db.Integer, db.ForeignKey('user.id'),primary_key=True),
#                         # Columna 'favorito_id' para almacenar el ID del favorito asociado al usuario
#                         db.Column('favorito_id', db.Integer, db.ForeignKey('favoritos.id'),primary_key=True)
# )

#------------------------------------------------------------------------USERS-------------------------------------------------------------

# Definir la clase de usuario (tabla de usuarios en la base de datos)
class User(db.Model):  # Definir una clase que hereda de la clase Model de SQLAlchemy
    # Definir las columnas de la tabla de usuarios
    id = db.Column(db.Integer, primary_key=True)  # Definir una columna de tipo entero como clave primaria
    #favorito_id = db.Column(db.Integer, db.ForeignKey('favoritos.id'))  # Corrección: db.Column en lugar de db.column
    email = db.Column(db.String(120), unique=True, nullable=False)  # Definir una columna de tipo string con restricciones de unicidad y no nulidad
    password = db.Column(db.String(80), unique=False, nullable=False)  # Definir una columna de tipo string con restricciones de no nulidad
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)  # Definir una columna de tipo booleano con restricciones de no nulidad
    username = db.Column(db.String(80), unique=True, nullable=False)  # Definir una columna de tipo string con restricciones de unicidad y no nulidad
    name = db.Column(db.String(80), unique=False, nullable=False)  # Definir una columna de tipo string con restricciones de no nulidad
    last_name = db.Column(db.String(80), unique=False, nullable=False)  # Definir una columna de tipo string con restricciones de no nulidad

    # favoritos = db.relationship("Favoritos", secondary=usuario_favoritos, back_populates="usuarios")
    favoritos = db.relationship("Favoritos", back_populates="usuarios")


    # Método para representar un objeto de usuario como una cadena
    def __repr__(self):  # Definir un método para representación de cadena
        return '<User %r>' % self.id  # Devolver una cadena que representa el objeto usuario

    # Método para serializar un objeto de usuario a un diccionario JSON
    def serialize(self):  # Definir un método para serializar el objeto usuario
        return {  # Devolver un diccionario con los atributos del usuario
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "name": self.name, 
            "last_name": self.last_name,
            "favoritos": [favorito.serialize() for favorito in self.favoritos]  # Serializar cada favorito en la lista

        }
    
#------------------------------------------------------------------------FAVORITOS-------------------------------------------------------------

class Favoritos(db.Model):
    # Definición de las columnas de la tabla de personajes
    id = db.Column(db.Integer, primary_key=True)  # Definir una columna de tipo entero como clave primaria
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Corrección: db.Column en lugar de db.column
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'))  # Definir una columna de clave foránea que referencia la tabla Film
    specie_id = db.Column(db.Integer, db.ForeignKey('species.id'))  # Definir una columna de clave foránea que referencia la tabla Film
    starship_id = db.Column(db.Integer, db.ForeignKey('starship.id'))  # Definir una columna de clave foránea que referencia la tabla Film
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))  # Definir una columna de clave foránea que referencia la tabla Film
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))  # Definir una columna de clave foránea que referencia la tabla Film
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))  # Definir una columna de clave foránea que referencia la tabla Film


        
    # Relaciones con las tablas de elementos favoritos
    film = db.relationship("Film", uselist=False, back_populates="favoritos")
    species = db.relationship("Species", uselist=False, back_populates="favoritos")
    starship = db.relationship("Starship", uselist=False, back_populates="favoritos")
    vehicle = db.relationship("Vehicle", uselist=False, back_populates="favoritos")
    character = db.relationship("Character", uselist=False, back_populates="favoritos")
    planet = db.relationship("Planet", uselist=False, back_populates="favoritos")


    # usuarios = db.relationship("User", secondary=usuario_favoritos, back_populates="favoritos")
    usuarios = db.relationship("User",  back_populates="favoritos")

    # Definir una relación con las tablas de usuario a través de la tabla de asociación


    def __repr__(self):  # Método para representar un objeto de personaje como una cadena
        return '<Favoritos %r>' % self.id  # Devolver una cadena que representa el objeto personaje

    def serialize(self):  # Método para serializar un objeto de personaje a un diccionario JSON
        # Obtener los nombres de los usuarios asociados al favorito
        # nombres_usuarios = [usuario.name for usuario in self.usuarios]
        # id_usuarios = [usuario.id for usuario in self.usuarios]

        return {  # Devolver un diccionario con los atributos del personaje
            "id": self.id,
            # "usuario": nombres_usuarios,
            "film": self.film.title if self.film else None,
            "species": self.species.name if self.species else None,
            "starship": self.starship.name if self.starship else None,
            "character": self.character.name if self.character else None,
            "planet": self.planet.name if self.planet else None

            # "homeworld": self.homeworld.name if self.film else None #serialize() if self.homeworld else None,  # Serializar el planeta asociado al personaje si existe

        }
    

#------------------------------------------------------------------------RELACION DE TABLAS-------------------------------------------------------------



# Definición de las tablas de relaciones many-to-many entre películas y otras entidades
starships_films = db.Table('starships_films',  # Nombre de la tabla de relación entre naves espaciales y películas
                           db.Column('starship_id', db.Integer, db.ForeignKey('starship.id'), primary_key=True),  # Columna de clave foránea para la nave espacial
                           db.Column('film_id', db.Integer, db.ForeignKey('film.id'), primary_key=True)  # Columna de clave foránea para la película
                           )

vehicles_films = db.Table('vehicles_films',  # Nombre de la tabla de relación entre vehículos y películas
                          db.Column('vehicle_id', db.Integer, db.ForeignKey('vehicle.id'), primary_key=True),  # Columna de clave foránea para el vehículo
                          db.Column('film_id', db.Integer, db.ForeignKey('film.id'), primary_key=True)  # Columna de clave foránea para la película
                          )

species_films = db.Table('species_films',  # Nombre de la tabla de relación entre especies y películas
                         db.Column('species_id', db.Integer, db.ForeignKey('species.id'), primary_key=True),  # Columna de clave foránea para la especie
                         db.Column('film_id', db.Integer, db.ForeignKey('film.id'), primary_key=True)  # Columna de clave foránea para la película
                         )

# Definición de la tabla de relación entre películas y planetas antes de la clase Planet
films_planets = db.Table('films_planets',  # Nombre de la tabla de relación entre películas y planetas
                         db.Column('film_id', db.Integer, db.ForeignKey('film.id'), primary_key=True),  # Columna de clave foránea para la película
                         db.Column('planet_id', db.Integer, db.ForeignKey('planet.id'), primary_key=True)  # Columna de clave foránea para el planeta
                         )


#------------------------------------------------------------------------FILM-------------------------------------------------------------


# Definición de la clase Film que representa una película
class Film(db.Model):
    # Definición de las columnas de la tabla de películas
    id = db.Column(db.Integer, primary_key=True)  # Definir una columna de tipo entero como clave primaria
    title = db.Column(db.String(255), nullable=False)  # Definir una columna de tipo string con restricciones de no nulidad
    episode_id = db.Column(db.Integer, nullable=False)  # Definir una columna de tipo entero con restricciones de no nulidad
    director = db.Column(db.String(255), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    opening_crawl = db.Column(db.Text, nullable=True)  # Definir una columna de tipo texto con restricciones de no nulidad
    producer = db.Column(db.String(255), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    release_date = db.Column(db.Date, nullable=True)  # Definir una columna de tipo fecha con restricciones de no nulidad
    created = db.Column(db.DateTime, nullable=True)  # Definir una columna de tipo fecha y hora con restricciones de no nulidad
    edited = db.Column(db.DateTime, nullable=True)  # Definir una columna de tipo fecha y hora con restricciones de no nulidad
    url = db.Column(db.String(255), unique=True, nullable=False)  # Definir una columna de tipo string con restricciones de unicidad y no nulidad

    favoritos = db.relationship("Favoritos", back_populates="film") # Relación uno a uno con la tabla Favoritos


    # Método para representar un objeto de película como una cadena
    def __repr__(self):  # Definir un método para representación de cadena
        return '<Film %r>' % self.id  # Devolver una cadena que representa el objeto película

    # Método para serializar un objeto de película a un diccionario JSON
    def serialize(self):  # Definir un método para serializar el objeto película
        return {  # Devolver un diccionario con los atributos de la película
            "id": self.id,
            "title": self.title,
            "episode_id": self.episode_id,
            "director": self.director,
            "opening_crawl": self.opening_crawl,
            "producer": self.producer,
            "release_date": self.release_date.strftime('%Y-%m-%d'),
            "created": self.created.strftime('%Y-%m-%d'),
            "edited": self.edited.strftime('%Y-%m-%d'),
            "url": self.url
        }


#------------------------------------------------------------------------STARSHIP-------------------------------------------------------------


# Definición de la clase Starship que representa una nave espacial
class Starship(db.Model):
    # Definición de las columnas de la tabla de naves espaciales
    id = db.Column(db.Integer, primary_key=True)  # Definir una columna de tipo entero como clave primaria
    name = db.Column(db.String(255), nullable=False)  # Definir una columna de tipo string con restricciones de no nulidad
    model = db.Column(db.String(255), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    starship_class = db.Column(db.String(255), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    manufacturer = db.Column(db.String(255), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    cost_in_credits = db.Column(db.String(50), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    length = db.Column(db.String(50), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    crew = db.Column(db.String(50), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    passengers = db.Column(db.String(50), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    max_atmosphering_speed = db.Column(db.String(50), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    hyperdrive_rating = db.Column(db.String(50), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    MGLT = db.Column(db.String(50), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    cargo_capacity = db.Column(db.String(50), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    consumables = db.Column(db.String(50), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    created = db.Column(db.DateTime, nullable=True)  # Definir una columna de tipo fecha y hora con restricciones de no nulidad
    edited = db.Column(db.DateTime, nullable=True)  # Definir una columna de tipo fecha y hora con restricciones de no nulidad
    url = db.Column(db.String(255), unique=True, nullable=True)  # Definir una columna de tipo string con restricciones de unicidad y no nulidad

    films = db.relationship('Film', secondary=starships_films, backref=db.backref('starships', lazy=True))  # Definir una relación many-to-many con películas
    favoritos = db.relationship("Favoritos", back_populates="starship") # Relación uno a uno con la tabla Favoritos


    # Método para representar un objeto de nave espacial como una cadena
    def __repr__(self):  # Definir un método para representación de cadena
        return '<Starship %r>' % self.id  # Devolver una cadena que representa el objeto nave espacial

    # Método para serializar un objeto de nave espacial a un diccionario JSON
    def serialize(self):  # Definir un método para serializar el objeto nave espacial
        return {  # Devolver un diccionario con los atributos de la nave espacial
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "starship_class": self.starship_class,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "hyperdrive_rating": self.hyperdrive_rating,
            "MGLT": self.MGLT,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "created": self.created.strftime('%Y-%m-%d'),
            "edited": self.edited.strftime('%Y-%m-%d'),
            "url": self.url
        }

#------------------------------------------------------------------------VEHICLE-------------------------------------------------------------


# Definición de la clase Vehicle que representa un vehículo
class Vehicle(db.Model):
    # Definición de las columnas de la tabla de vehículos
    id = db.Column(db.Integer, primary_key=True)  # Definir una columna de tipo entero como clave primaria
    name = db.Column(db.String(255), nullable=False)  # Definir una columna de tipo string con restricciones de no nulidad
    model = db.Column(db.String(255), nullable=False)  # Definir una columna de tipo string con restricciones de no nulidad
    vehicle_class = db.Column(db.String(255), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    manufacturer = db.Column(db.String(255), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    cost_in_credits = db.Column(db.String(50), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    length = db.Column(db.String(50), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    crew = db.Column(db.String(50), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    passengers = db.Column(db.String(50), nullable=False)  # Definir una columna de tipo string con restricciones de no nulidad
    max_atmosphering_speed = db.Column(db.String(50), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    cargo_capacity = db.Column(db.String(50), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    consumables = db.Column(db.String(50), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    created = db.Column(db.DateTime, nullable=True)  # Definir una columna de tipo fecha y hora con restricciones de no nulidad
    edited = db.Column(db.DateTime, nullable=True)  # Definir una columna de tipo fecha y hora con restricciones de no nulidad
    url = db.Column(db.String(255), unique=True, nullable=True)  # Definir una columna de tipo string con restricciones de unicidad y no nulidad

    films = db.relationship('Film', secondary=vehicles_films, backref=db.backref('vehicles', lazy=True))  # Definir una relación many-to-many con películas
    favoritos = db.relationship("Favoritos", back_populates="vehicle") # Relación uno a uno con la tabla Favoritos

    # Método para representar un objeto de vehículo como una cadena
    def __repr__(self):  # Definir un método para representación de cadena
        return '<Vehicle %r>' % self.id  # Devolver una cadena que representa el objeto vehículo

    # Método para serializar un objeto de vehículo a un diccionario JSON
    def serialize(self):  # Definir un método para serializar el objeto vehículo
        return {  # Devolver un diccionario con los atributos del vehículo
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "created": self.created.strftime('%Y-%m-%d'),
            "edited": self.edited.strftime('%Y-%m-%d'),
            "url": self.url
        }


#------------------------------------------------------------------------SPECIES-------------------------------------------------------------


# Definición de la clase Species que representa una especie
class Species(db.Model):
    # Definición de las columnas de la tabla de especies
    id = db.Column(db.Integer, primary_key=True)  # Definir una columna de tipo entero como clave primaria
    name = db.Column(db.String(255), nullable=False)  # Definir una columna de tipo string con restricciones de no nulidad
    classification = db.Column(db.String(255), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    designation = db.Column(db.String(255), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    average_height = db.Column(db.String(50), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    average_lifespan = db.Column(db.String(50), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    eye_colors = db.Column(db.String(255), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    hair_colors = db.Column(db.String(255), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    skin_colors = db.Column(db.String(255), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    language = db.Column(db.String(255), nullable=False)  # Definir una columna de tipo string con restricciones de no nulidad
    # homeworld = db.Column(db.String(255), nullable=False)  # Definir una columna de tipo string con restricciones de no nulidad
    created = db.Column(db.DateTime, nullable=True)  # Definir una columna de tipo fecha y hora con restricciones de no nulidad
    edited = db.Column(db.DateTime, nullable=True)  # Definir una columna de tipo fecha y hora con restricciones de no nulidad
    homeworld_id = db.Column(db.Integer, db.ForeignKey('planet.id'))  # Definir una columna de clave externa que referencia la tabla de planetas
    url = db.Column(db.String(255), unique=True, nullable=True)  # Definir una columna de tipo string con restricciones de unicidad y no nulidad

    homeworld = db.relationship('Planet', backref='species_homeworld', lazy=True)  # Definir una relación many-to-one con planetas
    films = db.relationship('Film', secondary=species_films, backref=db.backref('species', lazy=True))  # Definir una relación many-to-many con películas
    favoritos = db.relationship("Favoritos", back_populates="species") # Relación uno a uno con la tabla Favoritos

    # Método para representar un objeto de especie como una cadena
    def __repr__(self):  # Definir un método para representación de cadena
        return '<Species %r>' % self.id  # Devolver una cadena que representa el objeto especie

    # Método para serializar un objeto de especie a un diccionario JSON
    def serialize(self):  # Definir un método para serializar el objeto especie
        return {  # Devolver un diccionario con los atributos de la especie
            "id": self.id,
            "name": self.name,
            "classification": self.classification,
            "designation": self.designation,
            "average_height": self.average_height,
            "average_lifespan": self.average_lifespan,
            "eye_colors": self.eye_colors,
            "hair_colors": self.hair_colors,
            "skin_colors": self.skin_colors,
            "language": self.language,
            "homeworld": self.homeworld.name if self.homeworld else None, #serialize() if self.homeworld else None,  # Serializar el planeta asociado al personaje si existe
            "created": self.created.strftime('%Y-%m-%d'),
            "edited": self.edited.strftime('%Y-%m-%d'),
            "url": self.url
        }

#------------------------------------------------------------------------PLANET-------------------------------------------------------------


# Definición de la clase Planet que representa un planeta
class Planet(db.Model):
    # Definición de las columnas de la tabla de planetas
    id = db.Column(db.Integer, primary_key=True)  # Definir una columna de tipo entero como clave primaria
    name = db.Column(db.String(255), nullable=False)  # Definir una columna de tipo string con restricciones de no nulidad
    diameter = db.Column(db.String(50), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    rotation_period = db.Column(db.String(50), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    orbital_period = db.Column(db.String(50), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    gravity = db.Column(db.String(50), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    population = db.Column(db.String(50), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    climate = db.Column(db.String(255), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    terrain = db.Column(db.String(255), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    surface_water = db.Column(db.String(50), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    created = db.Column(db.DateTime, nullable=True)  # Definir una columna de tipo fecha y hora con restricciones de no nulidad
    edited = db.Column(db.DateTime, nullable=True)  # Definir una columna de tipo fecha y hora con restricciones de no nulidad
    url = db.Column(db.String(255), unique=True, nullable=True)  # Definir una columna de tipo string con restricciones de unicidad y no nulidad

    # residents = db.relationship('Character', backref='residents_homeworld', lazy=True)  # Definir una relación one-to-many con personajes (residents)

    films = db.relationship('Film', secondary=films_planets, backref=db.backref('planets', lazy=True))  # Definir una relación many-to-many con películas
    favoritos = db.relationship("Favoritos", back_populates="planet") # Relación uno a uno con la tabla Favoritos

    def __repr__(self):  # Método para representar un objeto de planeta como una cadena
        return '<Planet %r>' % self.id  # Devolver una cadena que representa el objeto planeta

    def serialize(self):  # Método para serializar un objeto de planeta a un diccionario JSON
        return {  # Devolver un diccionario con los atributos del planeta
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "created": self.created.strftime('%Y-%m-%d') if self.created else None,
            "edited": self.edited.strftime('%Y-%m-%d') if self.edited else None,
            "url": self.url
        }


#------------------------------------------------------------------------CHARACTER-------------------------------------------------------------

# Definición de la clase Character que representa un personaje
class Character(db.Model):
    # Definición de las columnas de la tabla de personajes
    id = db.Column(db.Integer, primary_key=True)  # Definir una columna de tipo entero como clave primaria
    name = db.Column(db.String(80), nullable=False)  # Definir una columna de tipo string con restricciones de no nulidad
    eye_color = db.Column(db.String(80), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    skin_color = db.Column(db.String(80), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    gender = db.Column(db.String(10), nullable=True)  # Definir una columna de tipo string con restricciones de no nulidad
    height = db.Column(db.String(10), nullable=True)  # Definir una columna de tipo string (opcional)
    mass = db.Column(db.String(10), nullable=True)  # Definir una columna de tipo string (opcional)
    hair_color = db.Column(db.String(80), nullable=True)  # Definir una columna de tipo string (opcional)
    birth_year = db.Column(db.String(10), nullable=True)  # Definir una columna de tipo string (opcional)
    homeworld_id = db.Column(db.Integer, db.ForeignKey('planet.id'))  # Definir una columna de clave externa que referencia la tabla de planetas
    url = db.Column(db.String(120), nullable=True)  # Definir una columna de tipo string (opcional)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)  # Definir una columna de tipo fecha y hora con valor predeterminado
    edited = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)  # Definir una columna de tipo fecha y hora con valor predeterminado y actualización automática
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'))  # Definir una columna de clave externa que referencia la tabla de películas

    homeworld = db.relationship('Planet', backref='characters_homeworld', lazy=True)  # Definir una relación many-to-one con planetas
    film = db.relationship('Film', backref=db.backref('characters', lazy=True))  # Definir una relación one-to-many con películas
    favoritos = db.relationship("Favoritos", back_populates="character") # Relación uno a uno con la tabla Favoritos

    def __repr__(self):  # Método para representar un objeto de personaje como una cadena
        return '<Character %r>' % self.id  # Devolver una cadena que representa el objeto personaje

    def serialize(self):  # Método para serializar un objeto de personaje a un diccionario JSON
        return {  # Devolver un diccionario con los atributos del personaje
            "id": self.id,
            "name": self.name,
            "eye_color": self.eye_color,
            "skin_color": self.skin_color,
            "gender": self.gender,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "birth_year": self.birth_year,
            "homeworld": self.homeworld.name if self.homeworld else None, #serialize() if self.homeworld else None,  # Serializar el planeta asociado al personaje si existe
            "url": self.url,
            "created": self.created.strftime('%Y-%m-%d'),  # Formatear la fecha de creación '%Y-%m-%dT%H:%M:%S.%fZ'
            "edited": self.edited.strftime('%Y-%m-%d'),  # Formatear la fecha de edición
            "film": self.film.title if self.film else None #serialize() if self.film else None  # Serializar la película asociada al personaje si existe
        }

# este código define las clases que representan las tablas de la base de datos en un modelo de objetos, 
# utilizando SQLAlchemy en Flask para la interacción con la base de datos. Cada clase define sus atributos 
# como columnas de la tabla correspondiente y métodos para representar y serializar los objetos.      


