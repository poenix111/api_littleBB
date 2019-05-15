from datetime import datetime
from libro import Libro
from usuario import Usuario
from material import Material
class Prestamo:
    def __init__(self, db):
        self.usuario = Usuario(db)
        self.libro = Libro(db)
        self.material = Material(db)
        self.conexion = db.conexion
        self.cursor = db.cursor

    def crear(self, data, libro = True):

        crearPrestamoNormal = ('INSERT INTO prestamo(id_user, fecha) VALUES (%s, %s)')
        if(libro):
            valuesPrestamoNormal = (data['usuario'], data['libros'][0]['date'])
        else:
            valuesPrestamoNormal = (data['usuario'], data['materiales'][0]['date'])

        crearPrestamoLibro = ('INSERT INTO prestamoLibro(folio, id_libro, fechaDevolucion, extension) VALUES (%s, %s, %s, %s)')


        crearPrestamoMaterial = ('INSERT INTO prestamoMaterial(folio, id_material, fechaDevolucion) VALUES (%s, %s, %s)')

        self.cursor.execute(crearPrestamoNormal, valuesPrestamoNormal)
        self.conexion.commit()

        query = ('SELECT LAST_INSERT_ID()')

        self.cursor.execute(query)
        prestamoId = self.cursor.fetchone()[0]
        if(libro):

            for libro in data['libros']:
                valuesPrestamoLibro = (prestamoId, libro['id_libro'], libro['dateEntrega'], libro['extension'])
                self.libro.removeCopy(libro['isbn'])
                self.usuario.aumentarContLibros(data['usuario'])
                self.cursor.execute(crearPrestamoLibro, valuesPrestamoLibro)
                self.conexion.commit()


        else:

            for material in data['materiales']:
                self.usuario.aumentarContMateriales(data['usuario'])
                valuesPrestamoMaterial = (prestamoId, material['id_material'], material['dateEntrega'])
                self.cursor.execute(crearPrestamoMaterial, valuesPrestamoMaterial)
                self.conexion.commit()



    def showLend(self, folio, libro = True):

        prestamoPrimary = ('SELECT * FROM prestamo WHERE folio = %s')

        self.cursor.execute(prestamoPrimary, (folio,))
        realLend = self.cursor.fetchall()
        if(realLend):
            realLend = realLend[0]
        if(libro):
            query = ('SELECT * FROM prestamoLibro WHERE folio = %s')

            self.cursor.execute(query, (folio, ))
            resultados = self.cursor.fetchall()
            libros = []
            if(resultados):
                for resultado in resultados:
                    print(resultado)
                    l = self.libro.searchById(resultado[1])
                    l['dateEntrega'] = str(resultado[2])
                    print(resultado[2])
                    #datetime.strptime(str(resultado[2]), '%Y-%m-%d %H:%M:%S')
                    l['date'] = str(realLend[2])
                    l['usuario'] = realLend[1]
                    l['extension'] = resultado[3]
                    libros.append(l)

                return libros
        else:
            query = ('SELECT * FROM prestamoMaterial WHERE folio = %s')

            self.cursor.execute(query, (folio,))

            resultados = self.cursor.fetchall()
            materiales = []

            if(resultados):
                for resultado in resultados:
                    m = self.material.searchById(resultado[1])
                    m['date'] = str(realLend[2])
                    m['dateEntrega'] = str(resultado[2])
                    m['usuario'] = realLend[1]
                    materiales.append(m)
                return materiales
            #hacer lo de los materiales


    def returnBook(self, data):
        today = datetime.now()
        fechaDevolucion = datetime.strptime(data['dateEntrega'], '%Y-%m-%d')
        print('hoy ' + str(today))
        print('fecha de devolucion ' + str(fechaDevolucion))
        if(today <= fechaDevolucion):
            self.libro.returnLibro(data['isbn'])
            self.borrarPrestamo(data['folio'], data['id_libro'])
            self.usuario.disminuirContLibros(data['usuario'])
            return True
        else:
            self.libro.returnLibro(data['isbn'])
            self.borrarPrestamo(data['folio'], data['id_libro'])
            self.usuario.penalizar(data['usuario'])
            diasAtraso = abs(today - fechaDevolucion).days
            self.cobroPrestamo(data['folio'],diasAtraso)
            return False
    def returnMaterial(self,data):
        self.borrarPrestamo(data['folio'],data['id_material'], False)

    def borrarPrestamo(self, folio, idPrestado, libro = True):
        if libro:
            delete = ('DELETE FROM prestamoLibro WHERE folio = %s AND id_libro = %s')
            self.cursor.execute(delete, (folio, idPrestado))
            self.conexion.commit()
            """
            query = ('SELECT * FROM prestamoLibro WHERE folio = %s')
            self.cursor.execute(query, (folio, ))
            resultado = self.cursor.fetchall()   """

        else:
            delete = ('DELETE FROM prestamoMaterial WHERE folio = %s AND id_material = %s')
            self.cursor.execute(delete, (folio, idPrestado))
            self.conexion.commit()

    #Falta hacer mostrar la informacion del prestamo, generar el ticket y retornar los prestamos

    def showPrestados(self, usuario, boolLibro = True):

        query = ('SELECT folio FROM prestamo WHERE id_user = %s')

        self.cursor.execute(query, (usuario,))
        resultados = self.cursor.fetchall()
        if(resultados):
            if(boolLibro):
                libros = []

                for resultado in resultados:
                    queryPrestamoLibro = ('SELECT id_libro FROM prestamoLibro WHERE folio = %s')
                    self.cursor.execute(queryPrestamoLibro, (resultado[0],))
                    resultadosLibros = self.cursor.fetchall()
                    if(resultadosLibros):
                        for libro in resultadosLibros:
                            libros.append(self.libro.searchById(libro[0])['isbn'])
                            #libros.append(libro[0])

                return libros
            else:
                materiales = []

                for resultado in resultados:
                    queryPrestamoMaterial = ('SELECT id_material FROM prestamoMaterial WHERE folio = %s')
                    self.cursor.execute(queryPrestamoMaterial, (resultado[0],))
                    resultadosMateriales = self.cursor.fetchall()
                    if(resultadosMateriales):
                        for material in resultadosMateriales:
                            materiales.append(self.material.searchById(material[0])['tipo'])
                            #libros.append(libro[0])
                return materiales

    def cobroPrestamo(self, folio, diasAtraso):
        today = datetime.now()
        query = ('SELECT montoActual FROM monto WHERE fecha = (SELECT max(fecha) FROM monto)')
        self.cursor.execute(query)
        monto = self.cursor.fetchone()
        monto = monto[0] * diasAtraso

        insert = ('INSERT INTO dinero(fecha, monto, id_prestamo) VALUES(%s, %s, %s)')

        self.cursor.execute(insert, (today, monto, folio))
        self.conexion.commit()
        return monto

    def tipo(self, folio):

        query = ('SELECT * FROM prestamo WHERE folio = %s')

        self.cursor.execute(query, (folio,))

        resultado = self.cursor.fetchone()

        if(resultado):
            queryLibro = ('SELECT * FROM prestamoLibro WHERE folio = %s')
            self.cursor.execute(queryLibro, (folio,))
            resultadoLibro = self.cursor.fetchall()

            if resultadoLibro:
                return True

            queryMaterial = ('SELECT * FROM prestamoMaterial WHERE folio = %s')
            self.cursor.execute(queryMaterial, (folio,))
            resultadoMaterial = self.cursor.fetchall()

            if resultadoMaterial:
                return False



            return None

    def mostrarFoliosActivos(self, usuario):

        queryPrestamo = ('SELECT folio FROM prestamo WHERE id_user = %s')
        self.cursor.execute(queryPrestamo, (usuario,))
        folios = self.cursor.fetchall()

        resultados = []
        
        if(folios):
            for folio in folios:
                folio = folio[0]
                queryLibro = ('SELECT DISTINCT folio FROM prestamoLibro WHERE folio = %s')
                self.cursor.execute(queryLibro, (folio, ))
                tmpLibro = self.cursor.fetchone()
                if(tmpLibro):
                    f = {

                        'folio': str(tmpLibro[0]),
                        'libro' : str(self.tipo(folio))
                    }
                    resultados.append(f)
                
                queryMaterial = ('SELECT DISTINCT folio FROM prestamoMaterial WHERE folio = %s')
                self.cursor.execute(queryMaterial, (folio, ))
                tmpMaterial = self.cursor.fetchone()
                if(tmpMaterial):
                    m = {
                        'folio': str(tmpMaterial[0]),
                        'libro' : str(self.tipo(folio))
                    }
                    resultados.append(m)
        
            return resultados

        else:
            return None

