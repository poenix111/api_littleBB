from flask import Flask, request,make_response, jsonify
import mysql.connector
from libro import Libro
from material import Material
from usuario import Usuario
from flask_cors import CORS,cross_origin
from db import DB



app = Flask(__name__)
core = CORS(app)

host = 'poenix111.mysql.pythonanywhere-services.com'
user = 'poenix111'
password = '@ashe123'
database = 'poenix111$biblioteca'

""" conexion = mysql.connector.connect(user='brian',password='ashe123',database='biblioteca')
cursor = conexion.cursor() """




db = DB(host, user, password, database)
@app.before_request
def before_request_callback():  
    db.conectar()

@app.after_request
def after_request_callback(response):  
    db.desconectar()
    return response


@app.route('/registrar-usuario-api', methods = ['GET'])
@cross_origin()
def registrarUsuario():
    user = Usuario(db)
    nombre = request.args.get('nombre')
    usuario = request.args.get('usuario')
    contra = request.args.get('contra')
    tipo = request.args.get('tipo')
    email = request.args.get('email')
    telefono = request.args.get('telefono')
    area = request.args.get('area')
    user.crear(nombre,usuario,contra, tipo, email, telefono, area)
    respuesta = make_response("Hello World")
    respuesta.headers.add("Access-Control-Allow-Origin","*")
    return respuesta



@app.route("/registrar-libro", methods = ['GET'])
@cross_origin()
def registrarLibro():
    libro = Libro(db)
    nombre = request.args.get('nombre')
    autor = request.args.get('autor')
    genero = request.args.get('genero')
    edicion = request.args.get('edicion')
    editorial = request.args.get('editorial')
    idioma = request.args.get('idioma')
    isbn = request.args.get('isbn')
    descripcion = request.args.get('descripcion')
    libro.crear(nombre,autor,genero,edicion,editorial,idioma,isbn,descripcion)
    respuesta = make_response("Hello World")
    respuesta.headers.add("Access-Control-Allow-Origin","*")
    return respuesta

@app.route("/registrar-material", methods = ['GET'])
def registrarMaterial():
    material = Material(db)
    tipo = request.args.get('tipo')
    marca = request.args.get('marca')
    descripcion = request.args.get('descripcion')
    numSerie = request.args.get('numSerie')
    material.crear(tipo, marca, descripcion, numSerie)
    respuesta = make_response("Hello World")
    respuesta.headers.add("Access-Control-Allow-Origin","*")
    return respuesta


@app.route('/recuperar-libros/', methods = ['GET'])
def recuperarLibros():
    libro = Libro(db)
    result = libro.mostrarAll()
    print(result)
    return jsonify(result)

@app.route('/recuperar-material/', methods = ['GET'])
def recuperarMaterial():
    material = Material(db)
    result = material.mostrarAll()
    print(result)
    return jsonify(result)
@app.route('/recuperar-usuarios', methods = ['GET'])
def recuperarUsuarios():
    usuario = Usuario(db)
    result = usuario.mostrarAll()
    return jsonify(result)


@app.route('/editar-usuario', methods = ['POST'])
def editarUsuario():
    user = Usuario(db)
    data = request.get_json(force=True)
    print(data)
    user.actualizar(data)
    respuesta = make_response("Hello World")
    respuesta.headers.add("Access-Control-Allow-Origin","*")
    return respuesta

@app.route('/editar-libro', methods = ['POST'])
def editarLibro():
    libro = Libro(db)
    data = request.get_json(force = True)
    libro.actualizar(data)
    respuesta = make_response("Hello World")
    respuesta.headers.add("Access-Control-Allow-Origin","*")
    return respuesta
@app.route('/editar-material', methods = ['POST'])
def editarMaterial():
    material = Material(db)
    data = request.get_json(force = True)
    material.actualizar(data)
    respuesta = make_response("Hello World")
    respuesta.headers.add("Access-Control-Allow-Origin","*")
    return respuesta
app.run(debug=True)