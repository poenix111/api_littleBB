class Libro:
    def __init__(self, db):
        self.conexion = db.conexion
        self.cursor = db.cursor

    def crear(self, data):

        insertar = (
            'INSERT INTO libro(nombre, autor, genero, edicion, editorial, idioma, isbn, descripcion, existencia, unicos, disponibles) VALUES (%s,%s,%s,%s,%s,%s,%s,%s, %s,%s,%s)')

        self.cursor.execute(insertar, (data['nombre'], data['autor'], data['genero'], data['edicion'], data['editorial'],
                                       data['idioma'], data['isbn'], data['descripcion'], data['existencia'], data['unicos'], data['disponibles']))
        self.conexion.commit()

    def mostrarAll(self):
        query = ('SELECT * FROM libro')
        self.cursor.execute(query)
        consulta = self.cursor.fetchall()

        resultados = []

        for r in consulta:
            libro = {
                "id_libro": r[0],
                "nombre": r[1],
                "autor": r[2],
                "genero": r[3],
                "edicion": r[4],
                "editorial": r[5],
                "idioma": r[6],
                "isbn": r[7],
                "descripcion": r[8],
                "existencia": r[9],
                "unicos": r[10],
                "disponibles": r[11]
            }

            resultados.append(libro)
        return resultados

    def actualizar(self, libro):
        update = ('UPDATE libro SET nombre = %s, autor = %s, genero = %s, edicion = %s, editorial = %s, idioma = %s, isbn = %s, descripcion = %s, existencia = %s, unicos = %s, disponibles = %s WHERE id_libro = %s')
        self.cursor.execute(update, (libro['nombre'], libro['autor'], libro['genero'], libro['edicion'], libro['editorial'], libro['idioma'],
                                     libro['isbn'], libro['descripcion'], libro['existencia'], libro['unicos'], libro['disponibles'], libro['id_libro']))
        self.conexion.commit()
    def exists(self, isbn):
        show = ('SELECT * FROM libro WHERE isbn = %s')

        self.cursor.execute(show, (isbn,))

        r = self.cursor.fetchall()
        print(r)
        if (r):
            return 'True'
        else:
            return 'False'
    def JsonExists(self, isbn):
        show = ('SELECT * FROM libro WHERE isbn = %s')

        self.cursor.execute(show, (isbn,))

        r = self.cursor.fetchall()
        if (r):
            r = r[0]
            return {
                "id_libro": r[0],
                "nombre": r[1],
                "autor": r[2],
                "genero": r[3],
                "edicion": r[4],
                "editorial": r[5],
                "idioma": r[6],
                "isbn": r[7],
                "descripcion": r[8],
                "existencia": r[9],
                "unicos": r[10],
                "disponibles": r[11]
            }
        else:
            return 'False'
    def searchById(self, id_libro):
        show = ('SELECT * FROM libro WHERE id_libro = %s')

        self.cursor.execute(show, (id_libro,))

        r = self.cursor.fetchall()
        if (r):
            r = r[0]
            return {
                    "id_libro": r[0],
                    "nombre": r[1],
                    "autor": r[2],
                    "genero": r[3],
                    "edicion": r[4],
                    "editorial": r[5],
                    "idioma": r[6],
                    "isbn": r[7],
                    "descripcion": r[8],
                    "existencia": r[9],
                    "unicos": r[10],
                    "disponibles": r[11]
                }
        else:
            return 'False'

    def hasCopys(self, isbn):
        query = ('SELECT disponibles FROM libro WHERE isbn = %s')

        self.cursor.execute(query, (isbn,))
        result = self.cursor.fetchall()
        
        if(result and self.exists(isbn)):
            result = result[0]
            print(result[0])
            if(result[0] > 0):
                return True
            else:
                return False
        else:
            return False

    def removeCopy(self, isbn):
        if(self.hasCopys(isbn)):
            disponibles = ('SELECT disponibles FROM libro WHERE isbn = %s')
            self.cursor.execute(disponibles, (isbn,))
            result = self.cursor.fetchall()
            copys = result[0][0]
            copys = copys - 1
            query = ('UPDATE libro SET disponibles = %s WHERE isbn = %s')
            self.cursor.execute(query, (copys,isbn))
            self.conexion.commit()
            return str(copys)
        else:
            return False

    def deleteCopy(self, isbn):
        if(self.exists(isbn)):
            delete = ('DELETE FROM libro WHERE isbn = %s')
            self.cursor.execute(delete, (isbn,))
            self.conexion.commit()
        else:
            return str(True)
    def turnIntoUnic(self,isbn):
        self.removeCopy(isbn)

        update = ('UPDATE libro SET unicos = %s WHERE isbn = %s')

        query = ('SELECT unicos FROM libro WHERE isbn = %s')
        self.cursor.execute(query, (isbn,))
        result = self.cursor.fetchall()
        unicos = result[0][0]
        unicos = unicos + 1
        self.cursor.execute(update, (unicos, isbn))
        self.conexion.commit()
        return str(unicos)

    def returnLibro(self,isbn):
        disponibles = ('SELECT disponibles FROM libro WHERE isbn = %s')
        self.cursor.execute(disponibles, (isbn,))
        result = self.cursor.fetchall()
        copys = result[0][0]
        copys = copys + 1
        query = ('UPDATE libro SET disponibles = %s WHERE isbn = %s')
        self.cursor.execute(query, (copys,isbn))
        self.conexion.commit()
        return str(copys)
    
    def borrarBook(self, isbn):
        delete = ('DELETE FROM libro WHERE isbn = %s')
        
        try:
            self.cursor.execute(delete, (isbn,))
            self.conexion.commit()
            return True
        except:
            return False

    def searchBookByIsbn(self, isbn):
        query = ('SELECT * FROM libro WHERE isbn LIKE %s')

        isbn = '%' + isbn + '%'

        self.cursor.execute(query, (isbn,))

        resultados = self.cursor.fetchall()

        lista = []
        if(resultados):
            for r in resultados:
                libro = {
                    "id_libro": r[0],
                    "nombre": r[1],
                    "autor": r[2],
                    "genero": r[3],
                    "edicion": r[4],
                    "editorial": r[5],
                    "idioma": r[6],
                    "isbn": r[7],
                    "descripcion": r[8],
                    "existencia": r[9],
                    "unicos": r[10],
                    "disponibles": r[11]
                }

                lista.append(libro)
            return lista

    def searchBookByName(self, name):
        query = ('SELECT * FROM libro WHERE nombre LIKE %s')

        name = '%' + name + '%'

        self.cursor.execute(query, (name,))

        resultados = self.cursor.fetchall()

        lista = []
        if(resultados):
            for r in resultados:
                libro = {
                    "id_libro": r[0],
                    "nombre": r[1],                        "autor": r[2],
                    "genero": r[3],
                    "edicion": r[4],
                    "editorial": r[5],
                    "idioma": r[6],
                    "isbn": r[7],
                    "descripcion": r[8],
                    "existencia": r[9],
                    "unicos": r[10],
                    "disponibles": r[11]
                }

                lista.append(libro)
            return lista