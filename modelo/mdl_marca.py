"""
modelo/mdl_marca.py
====================
El MODELO: aqui definimos QUE es una marca (Entidad) y CUALES son
las consultas SQL para guardarla/leerla en PostgreSQL (DAO).

El modelo NO pide datos por teclado ni muestra menus (eso es trabajo
de la Vista) y NO valida reglas de negocio (eso es del Controlador).

Campos: id_marca (PK), nombre, estado.

Nota: ya NO existe siguiente_id(). Antes se calculaba a mano porque
los datos vivian en un .txt; ahora id_marca es SERIAL en PostgreSQL,
asi que la base de datos genera el id sola en cada INSERT.
"""

from config.conexion import Conexion


class Marca:
    """
    Entidad: representa una marca. Solo GUARDA datos, no sabe nada
    de SQL ni de PostgreSQL. Eso es trabajo del MarcaDAO de mas abajo.
    """

    def __init__(self, nombre, estado=True, id=None):
        """
        Constructor: se ejecuta al hacer Marca(...). Solo GUARDA los datos.
        id=None cuando la marca todavia no existe en la base de datos
        (caso de una marca nueva, antes de insertarla).
        """
        self._id = int(id) if id is not None else None
        self._nombre = nombre
        self._estado = estado

    # -------------------------------------------------------------------
    # PROPERTIES: dan acceso controlado a los datos.
    # @property = para LEER (marca.nombre) y @nombre.setter = para
    # CAMBIAR (marca.nombre = "Nike"). Se usan SIN parentesis.
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


class MarcaDAO:
    """
    DAO (Data Access Object): aqui SI vive el SQL de la tabla marca.
    La Entidad Marca de arriba nunca ejecuta una consulta; siempre
    se la delega al MarcaDAO. Esto es lo que pide el enunciado:
    "Clases de entidad y DAOs (Consultas SQL)".
    """

    @staticmethod
    def insertar(marca):
        """
        Guarda una Marca nueva en PostgreSQL.
        No se envia el id: la columna id_marca es SERIAL, la propia
        base de datos lo genera sola (reemplaza a siguiente_id).
        """
        con = Conexion.obtener_conexion()
        try:
            cursor = con.cursor()
            cursor.execute(
                "INSERT INTO marca (nombre, estado) VALUES (%s, %s)",
                (marca.nombre, marca.estado)
            )
            con.commit()
            cursor.close()
            return True
        except Exception as ex:
            con.rollback()
            print(f"Error al insertar marca: {ex}")
            return False
        finally:
            con.close()

    @staticmethod
    def listar():
        """
        Trae solo las marcas ACTIVAS (estado = TRUE) y las devuelve
        como una lista de objetos Marca. Las marcas desactivadas
        (borrado logico) ya no aparecen aqui.
        """
        con = Conexion.obtener_conexion()
        marcas = []
        try:
            cursor = con.cursor()
            cursor.execute("SELECT id_marca, nombre, estado FROM marca WHERE estado = TRUE ORDER BY id_marca")
            for fila in cursor.fetchall():
                marcas.append(Marca(id=fila[0], nombre=fila[1], estado=fila[2]))
            cursor.close()
        except Exception as ex:
            print(f"Error al listar marcas: {ex}")
        finally:
            con.close()
        return marcas

    @staticmethod
    def obtener_por_id(id_marca):
        """Trae UNA sola marca segun su id. Devuelve None si no existe."""
        con = Conexion.obtener_conexion()
        marca = None
        try:
            cursor = con.cursor()
            cursor.execute(
                "SELECT id_marca, nombre, estado FROM marca WHERE id_marca = %s",
                (id_marca,)
            )
            fila = cursor.fetchone()
            if fila:
                marca = Marca(id=fila[0], nombre=fila[1], estado=fila[2])
            cursor.close()
        except Exception as ex:
            print(f"Error al obtener marca: {ex}")
        finally:
            con.close()
        return marca

    @staticmethod
    def actualizar(marca):
        """Actualiza nombre y estado de una marca que YA existe (tiene id)."""
        con = Conexion.obtener_conexion()
        try:
            cursor = con.cursor()
            cursor.execute(
                "UPDATE marca SET nombre = %s, estado = %s WHERE id_marca = %s",
                (marca.nombre, marca.estado, marca.id)
            )
            con.commit()
            cursor.close()
            return True
        except Exception as ex:
            con.rollback()
            print(f"Error al actualizar marca: {ex}")
            return False
        finally:
            con.close()

    @staticmethod
    def cambiar_estado(id_marca, nuevo_estado):
        """
        'Borrado logico': en vez de eliminar la fila, la activa o
        desactiva. Evita romper productos que ya usan esta marca.
        """
        con = Conexion.obtener_conexion()
        try:
            cursor = con.cursor()
            cursor.execute(
                "UPDATE marca SET estado = %s WHERE id_marca = %s",
                (nuevo_estado, id_marca)
            )
            con.commit()
            cursor.close()
            return True
        except Exception as ex:
            con.rollback()
            print(f"Error al cambiar estado de marca: {ex}")
            return False
        finally:
            con.close()