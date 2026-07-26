"""
modelo/mdl_categoria.py
========================
El MODELO: aqui definimos QUE es una categoria (Entidad) y CUALES son
las consultas SQL para guardarla/leerla en PostgreSQL (DAO).

Campos: id_categoria (PK), nombre, estado.

Nota: ya NO existe siguiente_id(). Antes se calculaba a mano porque
los datos vivian en un .txt; ahora id_categoria es SERIAL en
PostgreSQL, asi que la base de datos genera el id sola en cada INSERT.
"""

from config.conexion import Conexion


class Categoria:
    """
    Entidad: representa una categoria. Solo GUARDA datos, no sabe
    nada de SQL ni de PostgreSQL. Eso es trabajo del CategoriaDAO.
    """

    def __init__(self, nombre, estado=True, id=None):
        """
        Constructor: se ejecuta al hacer Categoria(...). Solo GUARDA los datos.
        id=None cuando la categoria todavia no existe en la base de datos.
        """
        self._id = int(id) if id is not None else None
        self._nombre = nombre
        self._estado = estado

    # -------------------------------------------------------------------
    # PROPERTIES: dan acceso controlado a los datos.
    # @property = para LEER (categoria.nombre) y @nombre.setter = para
    # CAMBIAR (categoria.nombre = "Calzado"). Se usan SIN parentesis.
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


class CategoriaDAO:
    """
    DAO (Data Access Object): aqui SI vive el SQL de la tabla categoria.
    La Entidad Categoria de arriba nunca ejecuta una consulta; siempre
    se la delega al CategoriaDAO.
    """

    @staticmethod
    def insertar(categoria):
        """
        Guarda una Categoria nueva en PostgreSQL.
        No se envia el id: la columna id_categoria es SERIAL, la propia
        base de datos lo genera sola (reemplaza a siguiente_id).
        """
        con = Conexion.obtener_conexion()
        try:
            cursor = con.cursor()
            cursor.execute(
                "INSERT INTO categoria (nombre, estado) VALUES (%s, %s)",
                (categoria.nombre, categoria.estado)
            )
            con.commit()
            cursor.close()
            return True
        except Exception as ex:
            con.rollback()
            print(f"Error al insertar categoria: {ex}")
            return False
        finally:
            con.close()

    @staticmethod
    def listar():
        """
        Trae solo las categorias ACTIVAS (estado = TRUE) y las
        devuelve como una lista de objetos Categoria.
        """
        con = Conexion.obtener_conexion()
        categorias = []
        try:
            cursor = con.cursor()
            cursor.execute("SELECT id_categoria, nombre, estado FROM categoria WHERE estado = TRUE ORDER BY id_categoria")
            for fila in cursor.fetchall():
                categorias.append(Categoria(id=fila[0], nombre=fila[1], estado=fila[2]))
            cursor.close()
        except Exception as ex:
            print(f"Error al listar categorias: {ex}")
        finally:
            con.close()
        return categorias

    @staticmethod
    def obtener_por_id(id_categoria):
        """Trae UNA sola categoria segun su id. Devuelve None si no existe."""
        con = Conexion.obtener_conexion()
        categoria = None
        try:
            cursor = con.cursor()
            cursor.execute(
                "SELECT id_categoria, nombre, estado FROM categoria WHERE id_categoria = %s",
                (id_categoria,)
            )
            fila = cursor.fetchone()
            if fila:
                categoria = Categoria(id=fila[0], nombre=fila[1], estado=fila[2])
            cursor.close()
        except Exception as ex:
            print(f"Error al obtener categoria: {ex}")
        finally:
            con.close()
        return categoria

    @staticmethod
    def actualizar(categoria):
        """Actualiza nombre y estado de una categoria que YA existe (tiene id)."""
        con = Conexion.obtener_conexion()
        try:
            cursor = con.cursor()
            cursor.execute(
                "UPDATE categoria SET nombre = %s, estado = %s WHERE id_categoria = %s",
                (categoria.nombre, categoria.estado, categoria.id)
            )
            con.commit()
            cursor.close()
            return True
        except Exception as ex:
            con.rollback()
            print(f"Error al actualizar categoria: {ex}")
            return False
        finally:
            con.close()

    @staticmethod
    def cambiar_estado(id_categoria, nuevo_estado):
        """
        'Borrado logico': en vez de eliminar la fila, la activa o
        desactiva. Evita romper productos que ya usan esta categoria.
        """
        con = Conexion.obtener_conexion()
        try:
            cursor = con.cursor()
            cursor.execute(
                "UPDATE categoria SET estado = %s WHERE id_categoria = %s",
                (nuevo_estado, id_categoria)
            )
            con.commit()
            cursor.close()
            return True
        except Exception as ex:
            con.rollback()
            print(f"Error al cambiar estado de categoria: {ex}")
            return False
        finally:
            con.close()