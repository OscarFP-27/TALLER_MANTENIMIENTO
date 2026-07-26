"""
controlador/ctr_producto.py
============================
El CONTROLADOR: es el "intermediario" entre la Vista y el Modelo.
Ya NO lee ni escribe un archivo de texto: le pide todo al
ProductoDAO (que es quien habla con PostgreSQL). Aqui viven las
VALIDACIONES de negocio (nombre, precio y stock validos).

Las FK (id_marca, id_categoria, id_linea) la Vista ya las valida
contra los catalogos antes de llegar aqui; si aun asi alguna fuera
invalida, PostgreSQL la rechaza solo por la FOREIGN KEY.
"""

from modelo.mdl_producto import Producto, ProductoDAO


class Controlador:

    def listar(self):
        return ProductoDAO.listar()

    def _validar_datos(self, nombre, precio, stock):
        if nombre is None or nombre.strip() == "":
            raise ValueError("El nombre no puede estar vacio.")
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")

    def agregar(self, nombre, id_marca, id_categoria, id_linea, precio, stock):
        self._validar_datos(nombre, precio, stock)

        nuevo = Producto(nombre=nombre, id_marca=id_marca, id_categoria=id_categoria,
                          id_linea=id_linea, precio=precio, stock=stock, estado=True)
        exito = ProductoDAO.insertar(nuevo)
        if not exito:
            raise ValueError("No se pudo guardar el producto en la base de datos.")

    def editar(self, id, nombre, id_marca, id_categoria, id_linea, precio, stock):
        self._validar_datos(nombre, precio, stock)

        producto = ProductoDAO.obtener_por_id(id)
        if producto is None:
            raise ValueError(f"No existe un producto con id {id}")

        producto.nombre = nombre
        producto.id_marca = id_marca
        producto.id_categoria = id_categoria
        producto.id_linea = id_linea
        producto.precio = precio
        producto.stock = stock

        exito = ProductoDAO.actualizar(producto)
        if not exito:
            raise ValueError("No se pudo actualizar el producto.")

    def eliminar(self, id):
        # Ya NO se borra la fila fisicamente: se desactiva (estado=False).
        producto = ProductoDAO.obtener_por_id(id)
        if producto is None:
            raise ValueError(f"No existe un producto con id {id}")

        exito = ProductoDAO.cambiar_estado(id, False)
        if not exito:
            raise ValueError("No se pudo desactivar el producto.")