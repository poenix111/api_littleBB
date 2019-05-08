import mysql.connector
class DB(): 

    def __init__(self, host, user, password, database):
        self.conexion = None
        self.cursor = None

        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def conectar(self):
        try:
            self.conexion = mysql.connector.connect(
                host=self.host, 
                user=self.user, 
                password=self.password, 
                database=self.database
            )
            
            self.cursor = self.conexion.cursor()
        except:
            print('Error al intentar conectar con la base de datos')
            exit(-1)
    def desconectar(self):
        try:

            self.cursor.close()
            self.conexion.close()
            self.conexion = None
            self.cursor = None
        except:
            print('Error al intentar desconectar')
            exit(-1)