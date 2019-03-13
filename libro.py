class Libro:
    def __init__(self, db):
        self.conexion = db.conexion
        self.cursor = db.cursor

    def crear(self, nombre, autor, genero, edicion, editorial, idioma, isbn, descripcion):

        insertar = (
            'INSERT INTO libro(nombre, autor, genero, edicion, editorial, idioma, isbn, descripcion, existencia, unicos, disponibles) VALUES (%s,%s,%s,%s,%s,%s,%s,%s, %s,%s,%s)')

        query = (
            'SELECT * FROM libro WHERE nombre = %s AND autor = %s AND edicion = %s')
        # Para validar que no tenga que solo actualizar la existecia del libro
        self.cursor.execute(query, (nombre, autor, edicion))
        result = self.cursor.fetchall()
        if(result):
            existencia = int(result[0][9])
            existencia = existencia + 1
            disponibles = int(result[0][11])
            disponibles = disponibles + 1
            print(result)
            updateExistencia = (
                'UPDATE libro SET existencia = %s, disponibles = %s WHERE id_libro = %s')
            # Esta raro no se actualiza, verificar porque
            self.cursor.execute(
                updateExistencia, (existencia, disponibles, result[0][0]))
            self.conexion.commit()
        else:
            self.cursor.execute(
                insertar, (nombre, autor, genero, edicion, editorial, idioma, isbn, descripcion, '1', '1', '1'))
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
