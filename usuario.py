import hashlib
from datetime import datetime


class Usuario:
    def __init__(self, db):
        self.conexion = db.conexion
        self.cursor = db.cursor

    def crear(self, nombre, usuario, contra, tipo, email, telefono, area):
        insertar = ('INSERT INTO usuario(id_usuario, nombre, tipo, email, telefono, pass, estado, fechaRegistro, penalizaciones, area) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
        """   h = hashlib.new('sha256', bytes(contra, 'utf-8'))
        h = h.hexdigest() """
        date = datetime.now()
        estado = True
        penalizaciones = 0
        tipoReal = type(int)
        if(tipo == 'bibliotecario' or tipo == ''):
            tipoReal = 3
        elif(tipo == "maestro"):
            tipoReal = 2
        elif(tipo == "estudiante"):
            tipoReal = 1

        self.cursor.execute(insertar, (usuario, nombre, tipoReal, email,
                                       telefono, contra, estado, date, penalizaciones, area))
        self.conexion.commit()

    def login(self, usuario, contra):
        select = ('SELECT * FROM usuario id_usuario = %s AND pass = %s')
        h = hashlib.new('sha256', bytes(contra, 'utf-8'))
        h = h.hexdigest()
        self.cursor.execute(select, (usuario, h))
        resultado = self.cursor.fetchall()
        if resultado:
            return True
        else:
            return False

    def actualizar(self, usuario):

        update = ('UPDATE usuario SET nombre = %s, tipo = %s, email = %s, telefono = %s, pass = %s, penalizaciones = %s, area = %s, estado = %s WHERE id_usuario = %s')
        tipoReal = type(int)
        tipoAux = usuario['tipo']
        if(tipoAux == 'bibliotecario' or tipoAux == '' or tipoAux == 1):
            tipoReal = 3
        elif(tipoAux == "maestro" or tipoAux == 2):
            tipoReal = 2
        elif(tipoAux == "estudiante" or tipoAux == 3):
            tipoReal = 1
        print(usuario)
        self.cursor.execute(update, (usuario['nombre'], tipoReal, usuario['email'],
                                     usuario['telefono'], usuario['pass'], usuario['penalizaciones'], usuario['area'],usuario['estado'], usuario['id_usuario']))
        self.conexion.commit()
         

    def mostrarAll(self):
        query = ('SELECT * FROM usuario')
        self.cursor.execute(query)
        consulta = self.cursor.fetchall()

        resultados = []

        for u in consulta:
            usuario = {
                "id_usuario": u[0],
                "nombre": u[1],
                "tipo": u[2],
                "email": u[3],
                "telefono": u[4],
                "pass": u[5],
                "estado": u[6],
                "fechaRegistro": u[7],
                "penalizaciones": u[8],
                "area": u[9]
            }
            resultados.append(usuario)
        return resultados
