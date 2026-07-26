
import psycopg2

HOST = "localhost"
PUERTO = "5432"
BASE_DATOS = "tecnored"
USUARIO = "postgres"
PASSWORD = "123"


class Conexion:

    @staticmethod
    def obtener_conexion():
        try:
            con = psycopg2.connect(
                host=HOST,
                port=PUERTO,
                dbname=BASE_DATOS,
                user=USUARIO,
                password=PASSWORD
            )
            return con
        except psycopg2.OperationalError as ex:
            raise ConnectionError(
                f"No se pudo conectar a PostgreSQL: {ex}"
            )