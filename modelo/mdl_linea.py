"""
modelo/mdl_linea.py
=====================
El MODELO: aqui definimos QUE es una linea (Entidad) y CUALES son
las consultas SQL para guardarla/leerla en PostgreSQL (DAO).

Campos: id_linea (PK), nombre, estado.
La Linea es un catalogo INDEPENDIENTE de la Categoria: no guarda
ninguna referencia a ella. Quien las relaciona es el Producto (con
sus FK id_categoria e id_linea, cada una por su lado).

Nota: ya NO existe siguiente_id(). Antes se calculaba a mano porque
los datos vivian en un .txt; ahora id_linea es SERIAL en PostgreSQL,
asi que la base de datos genera el id sola en cada INSERT.
"""

from config.conexion import Conexion


class Linea:
    """
    Entidad: representa una linea. Solo GUARDA datos, no sabe nada
    de SQL ni de PostgreSQL. Eso es trabajo del LineaDAO.
    """

    def __init__(self, nombre, estado=True, id=None):
        """
        Constructor: se ejecuta al hacer Linea(...). Solo GUARDA los datos.
        id=None cuando la linea todavia no existe en la base de datos.
        """
        self._id = int(id) if id is not None else None
        self._nombre = nombre
        self._estado = estado

    # -------------------------------------------------------------------
    # PROPERTIES: dan acceso controlado a los datos.
    # @property = para LEER (linea.nombre) y @nombre.setter = para
    # CAMBIAR (linea.nombre = "Deportiva"). Se usan SIN parentesis.
    # -------------------------------------------------------------------
    @property
    def id(self):
        # Solo LECTURA: no tiene setter, el id no se puede cambiar desde fuera.
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, valor):
        self._estado = valor

    def __str__(self):
        return f"[{self._id}] {self._nombre} - {'Activo' if self._estado else 'Inactivo'}"


class LineaDAO:
    """
    DAO (Data Access Object): aqui SI vive el SQL de la tabla linea.
    La Entidad Linea de arriba nunca ejecuta una consulta; siempre
    se la delega al LineaDAO.
    """

    @staticmethod
    def insertar(linea):
        """
        Guarda una Linea nueva en PostgreSQL.
        No se envia el id: la columna id_linea es SERIAL, la propia
        base de datos lo genera sola (reemplaza a siguiente_id).
        """
        con = Conexion.obtener_conexion()
        try:
            cursor = con.cursor()
            cursor.execute(
                "INSERT INTO linea (nombre, estado) VALUES (%s, %s)",
                (linea.nombre, linea.estado)
            )
            con.commit()
            cursor.close()
            return True
        except Exception as ex:
            con.rollback()
            print(f"Error al insertar linea: {ex}")
            return False
        finally:
            con.close()

    @staticmethod
    def listar():
        """
        Trae solo las lineas ACTIVAS (estado = TRUE) y las devuelve
        como una lista de objetos Linea.
        """
        con = Conexion.obtener_conexion()
        lineas = []
        try:
            cursor = con.cursor()
            cursor.execute("SELECT id_linea, nombre, estado FROM linea WHERE estado = TRUE ORDER BY id_linea")
            for fila in cursor.fetchall():
                lineas.append(Linea(id=fila[0], nombre=fila[1], estado=fila[2]))
            cursor.close()
        except Exception as ex:
            print(f"Error al listar lineas: {ex}")
        finally:
            con.close()
        return lineas

    @staticmethod
    def obtener_por_id(id_linea):
        """Trae UNA sola linea segun su id. Devuelve None si no existe."""
        con = Conexion.obtener_conexion()
        linea = None
        try:
            cursor = con.cursor()
            cursor.execute(
                "SELECT id_linea, nombre, estado FROM linea WHERE id_linea = %s",
                (id_linea,)
            )
            fila = cursor.fetchone()
            if fila:
                linea = Linea(id=fila[0], nombre=fila[1], estado=fila[2])
            cursor.close()
        except Exception as ex:
            print(f"Error al obtener linea: {ex}")
        finally:
            con.close()
        return linea

    @staticmethod
    def actualizar(linea):
        """Actualiza nombre y estado de una linea que YA existe (tiene id)."""
        con = Conexion.obtener_conexion()
        try:
            cursor = con.cursor()
            cursor.execute(
                "UPDATE linea SET nombre = %s, estado = %s WHERE id_linea = %s",
                (linea.nombre, linea.estado, linea.id)
            )
            con.commit()
            cursor.close()
            return True
        except Exception as ex:
            con.rollback()
            print(f"Error al actualizar linea: {ex}")
            return False
        finally:
            con.close()

    @staticmethod
    def cambiar_estado(id_linea, nuevo_estado):
        """
        'Borrado logico': en vez de eliminar la fila, la activa o
        desactiva. Evita romper productos que ya usan esta linea.
        """
        con = Conexion.obtener_conexion()
        try:
            cursor = con.cursor()
            cursor.execute(
                "UPDATE linea SET estado = %s WHERE id_linea = %s",
                (nuevo_estado, id_linea)
            )
            con.commit()
            cursor.close()
            return True
        except Exception as ex:
            con.rollback()
            print(f"Error al cambiar estado de linea: {ex}")
            return False
        finally:
            con.close()