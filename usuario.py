import hashlib
from datetime import datetime


class Usuario:
    def __init__(self, db):
        self.conexion = db.conexion
        self.cursor = db.cursor

    def crear(self, data):
        insertar = ('INSERT INTO usuario(id_usuario, nombre, tipo, email, telefono, pass, estado, fechaRegistro, penalizaciones, area) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
        h = hashlib.new('sha256', bytes(data['contra'], 'utf-8'))
        h = h.hexdigest()
        date = datetime.now()
        estado = True
        penalizaciones = 0
        """  if(data["tipo"] == 'bibliotecario'):
            tipoReal = 3
        elif(data["tipo"] == "maestro"):
            tipoReal = 2
        elif(data["tipo"] == "estudiante" or data["tipo"] == ''):
            tipoReal = 1 """

        self.cursor.execute(insertar, (data["usuario"], data["nombre"], data['tipo'], data["email"],
                                       data["telefono"], h, estado, date, penalizaciones, data["area"]))
        self.conexion.commit()

    def login(self, usuario, contra):
        select = ('SELECT * FROM usuario WHERE id_usuario = %s AND pass = %s')
        h = hashlib.new('sha256', bytes(contra, 'utf-8'))
        h = h.hexdigest()
        self.cursor.execute(select, (usuario, h))
        resultado = self.cursor.fetchall()
        print(resultado)
        if(resultado):
            return {
                'id_usuario': resultado[0][0],
                'nombre': resultado[0][1],
                'tipo': resultado[0][2],
                'email': resultado[0][3],
                'telefono': resultado[0][4],
                'estado': resultado[0][6],
                'fecha': str(resultado[0][7]),
                'penalizaciones': resultado[0][8],
                'area': resultado[0][9]

            }
        

    def actualizar(self, usuario):
        if(usuario['pass'] != ''):
            update = ('UPDATE usuario SET nombre = %s, tipo = %s, email = %s, telefono = %s, pass = %s, penalizaciones = %s, area = %s, estado = %s WHERE id_usuario = %s')
        else:
            update = ('UPDATE usuario SET nombre = %s, tipo = %s, email = %s, telefono = %s, penalizaciones = %s, area = %s, estado = %s WHERE id_usuario = %s')
        h = hashlib.new('sha256', bytes(usuario['pass'], 'utf-8'))
        h = h.hexdigest()
        """  tipoAux = usuario['tipo']
        if(tipoAux == 'bibliotecario' or tipoAux == 1):
            tipoReal = 3
        elif(tipoAux == "maestro" or tipoAux == 2):
            tipoReal = 2
        elif(tipoAux == "estudiante" or tipoAux == 3 or tipoAux == ''):
            tipoReal = 1 """
        if(usuario['pass'] != ''):
            self.cursor.execute(update, (usuario['nombre'], usuario['tipo'], usuario['email'],
                                         usuario['telefono'], h, usuario['penalizaciones'], usuario['area'], usuario['estado'], usuario['id_usuario']))
        else:
            self.cursor.execute(update, (usuario['nombre'], usuario['tipo'], usuario['email'],
                                         usuario['telefono'], usuario['penalizaciones'], usuario['area'], usuario['estado'], usuario['id_usuario']))
        self.conexion.commit()

    def mostrarAll(self, name=None, matricula=None):
        query = ('SELECT * FROM usuario ')

        if(name or matricula):
            if(name):
                query += ('WHERE nombre LIKE %s')
                name = '%' + name + '%'
                self.cursor.execute(query, (name, ))
            if(matricula):
                query += ('WHERE CAST(id_usuario as CHAR) LIKE %s')
                matricula = '%' + matricula + '%'
                self.cursor.execute(query, (matricula, ))
        else:
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

    def exists(self, usuario):
        select = ('SELECT * FROM usuario WHERE id_usuario = %s')
        self.cursor.execute(select, (usuario,))
        resultado = self.cursor.fetchall()
        print(resultado)
        if resultado:
            return True
        else:
            return False

    def showInfo(self, usuario):

        select = ('SELECT * FROM usuario WHERE id_usuario = %s')
        self.cursor.execute(select, (usuario,))
        u = self.cursor.fetchall()
        if(u):
            u = u[0]
            return {
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

    def penalizar(self, usuario):

        if(self.exists(usuario)):
            penalizaciones = self.showInfo(usuario)['penalizaciones'] + 1
            update = (
                'UPDATE usuario SET penalizaciones = %s WHERE id_usuario = %s')
            self.cursor.execute(update, (penalizaciones, usuario))
            self.conexion.commit()
            return str(penalizaciones)
        else:
            return str(False)

    def borrarUser(self, usuario):
        delete = ('DELETE FROM usuario WHERE id_usuario = %s')
        
        try:
            self.cursor.execute(delete, (usuario,))
            self.conexion.commit()
            return True
        except:
            return False
            
       
    def changeStatus(self, usuario):
       user = self.showInfo(usuario)

       update = ('UPDATE usuario SET estado = %s WHERE id_usuario = %s')

       if(user['penalizaciones'] == 5):
           self.cursor.execute(update, (False, usuario))
           self.conexion.commit()
       
    def aumentarContLibros(self, usuario):
        query = ('SELECT contLibros FROM libroUsuarios WHERE id_user = %s')

        self.cursor.execute(query, (usuario,))

        resultado = self.cursor.fetchall()

        if(resultado):

            contLibros = resultado[0][0] + 1
            

            actualizar = ('UPDATE libroUsuarios SET contLibros = %s WHERE id_user = %s')
            self.cursor.execute(actualizar, (contLibros,usuario))
            self.conexion.commit()
        
        else:
            insert = ('INSERT INTO libroUsuarios(id_user, contLibros) VALUES(%s, %s)')

            self.cursor.execute(insert, (usuario, 1))
            self.conexion.commit()

    def disminuirContLibros(self, usuario):
        query = ('SELECT contLibros FROM libroUsuarios WHERE id_user = %s')            
        self.cursor.execute(query, (usuario,))
        resultado = self.cursor.fetchall()
        if(resultado):
            contLibros = resultado[0][0] - 1
            actualizar = ('UPDATE libroUsuarios SET contLibros = %s WHERE id_user = %s')
            self.cursor.execute(actualizar, (contLibros,usuario))
            self.conexion.commit()
        
    def aumentarContMateriales(self, usuario):
        query = ('SELECT contMateriales FROM materialesUsuarios WHERE id_user = %s')

        self.cursor.execute(query, (usuario,))

        resultado = self.cursor.fetchall()

        if(resultado):

            contMaterial = resultado[0][0] + 1
            

            actualizar = ('UPDATE materialesUsuarios SET contMateriales = %s WHERE id_user = %s')
            self.cursor.execute(actualizar, (contMaterial,usuario))
            self.conexion.commit()
        
        else:
            insert = ('INSERT INTO libroUsuarios(id_user, contLibros) VALUES(%s, %s)')

            self.cursor.execute(insert, (usuario, 1))
            self.conexion.commit()


    def disminuirContMateriales(self, usuario):
        query = ('SELECT contMateriales FROM materialesUsuarios WHERE id_user = %s')            
        self.cursor.execute(query, (usuario,))
        resultado = self.cursor.fetchall()
        if(resultado):
            contLibros = resultado[0][0] - 1
            actualizar = ('UPDATE materialesUsuarios SET contMateriales = %s WHERE id_user = %s')
            self.cursor.execute(actualizar, (contLibros,usuario))
            self.conexion.commit()
    def searchContBooks(self, usuario):
        query = ('SELECT contLibros FROM libroUsuarios WHERE id_user = %s')

        self.cursor.execute(query, (usuario,))

        resultado = self.cursor.fetchall()

        if(resultado):
            return str(resultado[0][0])
        else:
            return str(0)
    def searchContMaterials(self, usuario):
        query = ('SELECT contMateriales FROM materialesUsuarios WHERE id_user = %s')

        self.cursor.execute(query, (usuario,))

        resultado = self.cursor.fetchall()

        if(resultado):
            return str(resultado[0][0])
        else:
            return str(0)
    def existsMaestro(self, usuario):

        select = ('SELECT * FROM usuario WHERE id_usuario = %s')
        self.cursor.execute(select, (usuario,))
        resultado = self.cursor.fetchone()
        print(resultado)
        if resultado:
            print('El resultado es: ' + str(resultado[2]))
            if(resultado[2] > 1):
                return True

            return False
        else:
            return False
