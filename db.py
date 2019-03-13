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
        self.conexion = mysql.connector.connect(
            host=self.host, 
            user=self.user, 
            password=self.password, 
            database=self.database
        )
        self.cursor = self.conexion.cursor()
    def desconectar(self):
        self.cursor.close()
        self.conexion.close()
        self.conexion = None
        self.cursor = None