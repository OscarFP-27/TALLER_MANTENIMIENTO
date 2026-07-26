"""
modelo/mdl_producto.py
=======================
El MODELO: aqui definimos QUE es un producto (Entidad) y CUALES son
las consultas SQL para guardarlo/leerlo en PostgreSQL (DAO).

Campos: id_producto (PK), nombre, id_marca (FK), id_categoria (FK),
        id_linea (FK), precio, stock, estado.

Las FK (id_marca, id_categoria, id_linea) son los ids de los otros
catalogos. Aqui solo guardamos el NUMERO; comprobar que ese id exista
lo hace la Vista antes de llamar al Controlador, y ademas PostgreSQL
lo protege de nuevo con sus FOREIGN KEY (si un id no existe, la base
de datos rechaza el INSERT/UPDATE).

Nota: ya NO existe siguiente_id(). Antes se calculaba a mano porque
los datos vivian en un .txt; ahora id_producto es SERIAL en
PostgreSQL, asi que la base de datos genera el id sola en cada INSERT.
"""

from config.conexion import Conexion


class Producto:
    """
    Entidad: representa un producto. Solo GUARDA datos, no sabe nada
    de SQL ni de PostgreSQL. Eso es trabajo del ProductoDAO.
    """

    def __init__(self, nombre, id_marca, id_categoria, id_linea, precio, stock,
                 estado=True, id=None):
        """
        Constructor: se ejecuta al hacer Producto(...). Solo GUARDA los datos.
        id=None cuando el producto todavia no existe en la base de datos.
        """
        self._id = int(id) if id is not None else None
        self._nombre = nombre
        self._id_marca = int(id_marca)
        self._id_categoria = int(id_categoria)
        self._id_linea = int(id_linea)
        self._precio = float(precio)
        self._stock = int(stock)
        self._estado = estado

    # -------------------------------------------------------------------
    # PROPERTIES: dan acceso controlado a los datos.
    # @property = para LEER (producto.precio) y @precio.setter = para
    # CAMBIAR (producto.precio = 59.99). Se usan SIN parentesis.
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
    def id_marca(self):
        return self._id_marca

    @id_marca.setter
    def id_marca(self, valor):
        self._id_marca = int(valor)

    @property
    def id_categoria(self):
        return self._id_categoria

    @id_categoria.setter
    def id_categoria(self, valor):
        self._id_categoria = int(valor)

    @property
    def id_linea(self):
        return self._id_linea

    @id_linea.setter
    def id_linea(self, valor):
        self._id_linea = int(valor)

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        self._precio = float(valor)

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, valor):
        self._stock = int(valor)

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, valor):
        self._estado = valor

    def __str__(self):
        return f"[{self._id}] {self._nombre} - Stock: {self._stock} - {'Activo' if self._estado else 'Inactivo'}"


class ProductoDAO:
    """
    DAO (Data Access Object): aqui SI vive el SQL de la tabla producto.
    La Entidad Producto de arriba nunca ejecuta una consulta; siempre
    se la delega al ProductoDAO.
    """

    @staticmethod
    def insertar(producto):
        """
        Guarda un Producto nuevo en PostgreSQL.
        No se envia el id: la columna id_producto es SERIAL, la propia
        base de datos lo genera sola (reemplaza a siguiente_id).
        Si alguna FK (id_marca, id_categoria, id_linea) no existe de
        verdad, PostgreSQL rechaza el INSERT solo, sin que este
        metodo tenga que comprobarlo a mano.
        """
        con = Conexion.obtener_conexion()
        try:
            cursor = con.cursor()
            cursor.execute(
                """INSERT INTO producto
                   (nombre, id_marca, id_categoria, id_linea, precio, stock, estado)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (producto.nombre, producto.id_marca, producto.id_categoria,
                 producto.id_linea, producto.precio, producto.stock, producto.estado)
            )
            con.commit()
            cursor.close()
            return True
        except Exception as ex:
            con.rollback()
            print(f"Error al insertar producto: {ex}")
            return False
        finally:
            con.close()

    @staticmethod
    def listar():
        """
        Trae solo los productos ACTIVOS (estado = TRUE) y los
        devuelve como una lista de objetos Producto.
        """
        con = Conexion.obtener_conexion()
        productos = []
        try:
            cursor = con.cursor()
            cursor.execute(
                """SELECT id_producto, nombre, id_marca, id_categoria, id_linea,
                          precio, stock, estado
                   FROM producto WHERE estado = TRUE ORDER BY id_producto"""
            )
            for fila in cursor.fetchall():
                productos.append(Producto(
                    id=fila[0], nombre=fila[1], id_marca=fila[2],
                    id_categoria=fila[3], id_linea=fila[4],
                    precio=fila[5], stock=fila[6], estado=fila[7]
                ))
            cursor.close()
        except Exception as ex:
            print(f"Error al listar productos: {ex}")
        finally:
            con.close()
        return productos

    @staticmethod
    def obtener_por_id(id_producto):
        """Trae UN solo producto segun su id. Devuelve None si no existe."""
        con = Conexion.obtener_conexion()
        producto = None
        try:
            cursor = con.cursor()
            cursor.execute(
                """SELECT id_producto, nombre, id_marca, id_categoria, id_linea,
                          precio, stock, estado
                   FROM producto WHERE id_producto = %s""",
                (id_producto,)
            )
            fila = cursor.fetchone()
            if fila:
                producto = Producto(
                    id=fila[0], nombre=fila[1], id_marca=fila[2],
                    id_categoria=fila[3], id_linea=fila[4],
                    precio=fila[5], stock=fila[6], estado=fila[7]
                )
            cursor.close()
        except Exception as ex:
            print(f"Error al obtener producto: {ex}")
        finally:
            con.close()
        return producto

    @staticmethod
    def actualizar(producto):
        """Actualiza todos los datos de un producto que YA existe (tiene id)."""
        con = Conexion.obtener_conexion()
        try:
            cursor = con.cursor()
            cursor.execute(
                """UPDATE producto
                   SET nombre = %s, id_marca = %s, id_categoria = %s, id_linea = %s,
                       precio = %s, stock = %s, estado = %s
                   WHERE id_producto = %s""",
                (producto.nombre, producto.id_marca, producto.id_categoria,
                 producto.id_linea, producto.precio, producto.stock,
                 producto.estado, producto.id)
            )
            con.commit()
            cursor.close()
            return True
        except Exception as ex:
            con.rollback()
            print(f"Error al actualizar producto: {ex}")
            return False
        finally:
            con.close()

    @staticmethod
    def cambiar_estado(id_producto, nuevo_estado):
        """'Borrado logico': en vez de eliminar la fila, la activa o desactiva."""
        con = Conexion.obtener_conexion()
        try:
            cursor = con.cursor()
            cursor.execute(
                "UPDATE producto SET estado = %s WHERE id_producto = %s",
                (nuevo_estado, id_producto)
            )
            con.commit()
            cursor.close()
            return True
        except Exception as ex:
            con.rollback()
            print(f"Error al cambiar estado de producto: {ex}")
            return False
        finally:
            con.close()