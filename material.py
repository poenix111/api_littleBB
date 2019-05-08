class Material:
    def __init__(self, db):
        self.conexion = db.conexion
        self.cursor = db.cursor

    def crear(self, data):
        insert = (
            'INSERT INTO material(tipo, marca, descripcion, numSerie) VALUES (%s,%s,%s,%s)')
        tipoReal = type(int)

        if(data['tipo'] == 'laptop' or data['tipo'] == ''):
            tipoReal = 1
        elif(data['tipo'] == 'bocina'):
            tipoReal = 2
        elif(data['tipo'] == 'proyector'):
            tipoReal = 3

        self.cursor.execute(insert, (tipoReal, data['marca'], data['descripcion'], data['numSerie']))
        self.conexion.commit()

    def mostrarAll(self):
        query = ('SELECT * FROM material')
        self.cursor.execute(query)
        consulta = self.cursor.fetchall()

        resultados = []

        for r in consulta:
            material = {
                "id_material": r[0],
                "tipo": r[1],
                "marca": r[2],
                "descripcion": r[3],
                "numSerie": r[4]
            }
            resultados.append(material)
        return resultados

    def actualizar(self, material):

        update = (
            'UPDATE material SET tipo = %s, marca = %s, descripcion = %s, numSerie = %s WHERE id_material = %s')
        tipoReal = type(int)
        tipo = material['tipo']
        """ if(tipo == 'laptop' or tipo == '' or tipo == 1):
            tipoReal = 1
        elif(tipo == 'bocina' or tipo == 2):
            tipoReal = 2
        elif(tipo == 'proyector' or tipo == 3):
            tipoReal = 3 """
        print(material)
        self.cursor.execute(update, (material['tipo'], material['marca'], material['descripcion'], material['numSerie'], material['id_material']))
        self.conexion.commit()

    def exists(self, numSerie):
        show = ('SELECT * FROM material WHERE numSerie = %s')

        self.cursor.execute(show, (numSerie,))

        r = self.cursor.fetchall()
        print(r)
        if (r):
            return True
        else:
            return False
    def deleteMaterial(self, numSerie):
        if(self.exists(numSerie)):
            delete = ('DELETE FROM material WHERE numSerie = %s')
            self.cursor.execute(delete, (numSerie,))
            self.conexion.commit()

    def searchById(self, id_material):
        show = ('SELECT * FROM material WHERE id_material = %s')

        self.cursor.execute(show, (id_material,))

        r = self.cursor.fetchone()
        if (r):
            return {
                    "id_material": r[0],
                    "tipo": r[1],
                    "marca": r[2],
                    "descripcion": r[3],
                    "numSerie": r[4]
            }
        else:
            return 'False'



    def jsonExists(self, numSerie):
        show = ('SELECT * FROM material WHERE numSerie = %s')

        self.cursor.execute(show, (numSerie,))

        r = self.cursor.fetchone()
        if (r):
            return {
                "id_material": r[0],
                "tipo": r[1],
                "marca": r[2],
                "descripcion": r[3],
                "numSerie": r[4]
            }
        else:
            return 'False'
        

    def isInLean(self, numSerie):
        query = ('SELECT * FROM prestamoMaterial WHERE numSerie = %s')

        self.cursor.execute(query, (numSerie,))

        resultado = self.cursor.fetchall()

        if(resultado):
            return True
        else:
            return False
