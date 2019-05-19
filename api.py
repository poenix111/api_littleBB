
# A very simple Flask Hello World app for you to get started with...


from flask import Flask, request, make_response, jsonify
import mysql.connector
from libro import Libro
from material import Material
from usuario import Usuario
from flask_cors import CORS, cross_origin
from db import DB
from prestamo import Prestamo
app = Flask(__name__)

CORS(app)
host = 'poenix111.mysql.pythonanywhere-services.com'
user = 'poenix111'
password = '@ashe123'
database = 'poenix111$biblioteca'


""" host = 'localhost'
user = 'brian'
password = 'ashe123'
database = 'biblioteca' """
"""
@app.route('/')
def hello_world():
    return 'Hello from Flask!'
"""
@app.route('/HOME')
def p():
    return 'Hello from Flask!'
db = DB(host, user, password, database)

@app.before_request
def before_request_callback():
    db.conectar()


@app.after_request
def after_request_callback(response):
    db.desconectar()
    return response


@app.route('/registrar-usuario', methods=['POST'])
def registrarUsuario():
    user = Usuario(db)
    data = request.get_json(force=True)
    user.crear(data)
    respuesta = make_response("Registro exitoso")
    respuesta.headers.add("Access-Control-Allow-Origin", "*")
    return respuesta


@app.route("/registrar-libro", methods=['POST'])
def registrarLibro():
    libro = Libro(db)
    data = request.get_json(force=True)
    libro.crear(data)
    print(data)
    respuesta = make_response("Hello World")
    respuesta.headers.add("Access-Control-Allow-Origin", "*")
    return respuesta


@app.route("/registrar-material", methods=['POST'])
def registrarMaterial():
    material = Material(db)
    data = request.get_json(force=True)
    material.crear(data)
    respuesta = make_response("Hello World")
    respuesta.headers.add("Access-Control-Allow-Origin", "*")
    return respuesta


@app.route('/recuperar-libros/', methods=['GET'])
def recuperarLibros():
    libro = Libro(db)
    result = libro.mostrarAll()
    print(result)
    return jsonify(result)


@app.route('/recuperar-material/', methods=['GET'])
def recuperarMaterial():
    material = Material(db)
    result = material.mostrarAll()
    print(result)
    return jsonify(result)


@app.route('/recuperar-usuarios', methods=['GET'])
def recuperarUsuarios():
    usuario = Usuario(db)
    result = usuario.mostrarAll()
    return jsonify(result)


@app.route('/editar-usuario', methods=['POST'])
def editarUsuario():
    user = Usuario(db)
    data = request.get_json(force=True)
    print(data)
    user.actualizar(data)
    respuesta = make_response("Hello World")
    respuesta.headers.add("Access-Control-Allow-Origin", "*")
    return respuesta


@app.route('/editar-libro', methods=['POST'])
def editarLibro():
    libro = Libro(db)
    data = request.get_json(force=True)
    libro.actualizar(data)
    respuesta = make_response("Hello World")
    respuesta.headers.add("Access-Control-Allow-Origin", "*")
    return respuesta


@app.route('/editar-material', methods=['POST'])
def editarMaterial():
    material = Material(db)
    data = request.get_json(force=True)
    material.actualizar(data)
    respuesta = make_response("Hello World")
    respuesta.headers.add("Access-Control-Allow-Origin", "*")
    return respuesta


@app.route('/login', methods=['POST'])
def login():
    usuario = Usuario(db)
    data = request.get_json(force=True)
    return jsonify(usuario.login(data['usuario'], data['contra']))


@app.route('/exists', methods=['POST'])
def exists():
    usuario = Usuario(db)
    data = request.get_json(force=True)
    """   data = {}
    data['usuario'] = request.args.get('usuario') """
    if(usuario.exists(data['usuario'])):
        return 'True'
    else:
        return 'False'


@app.route('/book-exists', methods=['POST'])
def bookExists():
    libro = Libro(db)
    data = request.get_json(force=True)
    if(libro.exists(data['isbn']) != 'False'):
        return jsonify(libro.JsonExists(data['isbn']))
    else:
        return 'False'


@app.route('/material-exists', methods=['POST'])
def materialExists():
    material = Material(db)
    data = request.get_json(force=True)
    numSerie = data['numSerie']
    if(material.exists(numSerie)):
        return jsonify(material.jsonExists(numSerie))
    else:
        return str(False)


@app.route('/book', methods=['POST'])
def book():
    libro = Libro(db)
    data = request.get_json(force=True)
    return libro.exists(data['isbn'])


@app.route('/material', methods=['POST'])
def material():
    material = Material(db)
    data = request.get_json(force=True)
    numSerie = data['numSerie']
    return str(material.exists(numSerie))


@app.route('/user-info', methods=['POST'])
def userInfo():
    usuario = Usuario(db)
    user = request.get_json(force=True)
    if(usuario.exists(user['usuario'])):
        return jsonify(usuario.showInfo(user['usuario']))

    return str(False)


@app.route('/next-value')
def nextValue():
    prestamo = Prestamo(db)
    return str(prestamo.nextValue())


@app.route('/prestamo-libro', methods=['POST'])
def prestamoLibro():
    prestamo = Prestamo(db)
    data = request.get_json(force=True)
    prestamo.crear(data)
    respuesta = make_response("Prestamo Creado")
    respuesta.headers.add("Access-Control-Allow-Origin", "*")
    return respuesta


@app.route('/prestamo-material', methods=['POST'])
def prestamoMaterial():
    prestamo = Prestamo(db)
    data = request.get_json(force=True)
    prestamo.crear(data, False)
    respuesta = make_response("Prestamo creado")
    respuesta.headers.add("Access-Control-Allow-Origin", '*')
    return respuesta


@app.route('/has-copy', methods=['POST'])
def hasCopy():
    libro = Libro(db)
    data = request.get_json(force=True)
    isbn = data['isbn']
    return str(libro.hasCopys(isbn))


@app.route('/remove-copy', methods=['POST'])
def removeCopy():
    libro = Libro(db)
    data = request.get_json(force=True)
    isbn = data['isbn']
    return str(libro.removeCopy(isbn))


@app.route('/turn-unic', methods=['POST'])
def turnUnic():
    libro = Libro(db)
    data = request.get_json(force=True)
    isbn = data['isbn']
    return str(libro.turnIntoUnic(isbn))


@app.route('/penalizar', methods=['POST'])
def penalizar():
    usuario = Usuario(db)
    data = request.get_json(force=True)
    id_user = data['usuario']
    return usuario.penalizar(id_user)


@app.route('/delete-user', methods=['POST'])
def deleteUser():
    user = Usuario(db)
    data = request.get_json(force=True)
    id_user = data['id_usuario']
    if(user.borrarUser(id_user)):
        respuesta = make_response("Borrado exitoso")
        respuesta.headers.add("Access-Control-Allow-Origin", "*")
        return respuesta
    else:
        respuesta = make_response("Error")
        respuesta.headers.add("Access-Control-Allow-Origin", "*")
        return respuesta

@app.route('/delete-book', methods=['POST'])
def deleteBook():
    book = Libro(db)
    data = request.get_json(force=True)
    isbn = data['isbn']
    if(book.borrarBook(isbn)):
        respuesta = make_response("Borrado exitoso")
        respuesta.headers.add("Access-Control-Allow-Origin", "*")
        return respuesta
    else:
        respuesta = make_response("Error")
        respuesta.headers.add("Access-Control-Allow-Origin", "*")
        return respuesta

@app.route('/delete-material', methods=['POST'])
def deleteMaterial():
    material = Material(db)
    data = request.get_json(force=True)
    numSerie = data['numSerie']
    if(material.borrarMaterial(numSerie)):
        respuesta = make_response("Borrado exitoso")
        respuesta.headers.add("Access-Control-Allow-Origin", "*")
        return respuesta
    else:
        respuesta = make_response("Error")
        respuesta.headers.add("Access-Control-Allow-Origin", "*")
        return respuesta

@app.route('/return-book', methods=['POST'])
def returnBook():
    prestamo = Prestamo(db)
    data = request.get_json(force=True)
    if(prestamo.returnBook(data)):
        respuesta = make_response("Retorno exitoso")
        respuesta.headers.add("Access-Control-Allow-Origin", "*")
        return respuesta
    else:
        respuesta = make_response("Usuario penalizado")
        respuesta.headers.add("Access-Control-Allow-Origin", "*")
        return respuesta


@app.route('/return-material', methods=['POST'])
def returnMaterial():
    prestamo = Prestamo(db)
    data = request.get_json(force=True)
    if(prestamo.returnMaterial(data)):
        respuesta = make_response("Retorno exitoso")
        respuesta.headers.add("Access-Control-Allow-Origin", "*")
        return respuesta
    else:
        respuesta = make_response("Usuario penalizado")
        respuesta.headers.add("Access-Control-Allow-Origin", "*")
        return respuesta


@app.route('/show-lend', methods=['POST'])
def showLend():
    prestamo = Prestamo(db)
    data = request.get_json(force=True)
    folio = data['folio']
    return jsonify(prestamo.showLend(folio))


@app.route('/show-lend-material', methods=['POST'])
def showLendMaterial():
    prestamo = Prestamo(db)
    data = request.get_json(force=True)
    folio = data['folio']
    return jsonify(prestamo.showLend(folio, False))


@app.route('/libros-en-posesion', methods=['POST'])
def librosEnPosesion():
    prestamo = Prestamo(db)
    data = request.get_json(force=True)
    usuario = data['usuario']
    return jsonify(prestamo.showPrestados(usuario))


@app.route('/materiales-en-posesion', methods=['POST'])
def materialesEnPosesion():
    prestamo = Prestamo(db)
    data = request.get_json(force=True)
    usuario = data['usuario']
    return jsonify(prestamo.showPrestados(usuario, False))


@app.route('/cont-books', methods=['POST'])
def contBooks():
    usuario = Usuario(db)
    data = request.get_json(force=True)
    user = data['usuario']
    return usuario.searchContBooks(user)


@app.route('/cont-materials', methods=['POST'])
def contMaterials():
    usuario = Usuario(db)
    data = request.get_json(force=True)
    user = data['usuario']
    return usuario.searchContMaterials(user)


@app.route('/tipo', methods=['POST'])
def tipo():
    prestamo = Prestamo(db)
    data = request.get_json(force=True)
    folio = data['folio']
    return str(prestamo.tipo(folio))


@app.route('/exists-maestro', methods=['POST'])
def existsMaestro():
    usuario = Usuario(db)
    data = request.get_json(force=True)
    user = data['usuario']
    return str(usuario.existsMaestro(user))

@app.route('/folios-activos', methods=['POST'])
def foliosActivos():
    prestamo = Prestamo(db)
    data = request.get_json(force=True)
    user = data['id_usuario']
    return jsonify(prestamo.mostrarFoliosActivos(user))

@app.route('/mostrar-dinero', methods = ['GET'])
def mostrarDinero():
    prestamo = Prestamo(db)

    return jsonify(prestamo.returnMoney())




@app.route('/cobro-daños', methods = ['POST'])
def cobroDeDaño():
    prestamo = Prestamo(db)
    data = request.get_json(force = True)
    money = data['dinero']
    folio = data['folio']
    prestamo.cobroDaño(money, folio)

    respuesta = make_response("Cobro realizado")
    respuesta.headers.add("Access-Control-Allow-Origin", "*")
    return respuesta

#app.run(debug=True)
