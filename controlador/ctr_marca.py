"""
controlador/ctr_marca.py
=========================
El CONTROLADOR: es el "intermediario" entre la Vista y el Modelo.
Ya NO lee ni escribe un archivo de texto: le pide todo al MarcaDAO
(que es quien habla con PostgreSQL). Aqui es donde viven las
VALIDACIONES de negocio (ej. no permitir nombres vacios), y desde
aqui se decide QUE metodo del DAO llamar segun la operacion.
"""

from modelo.mdl_marca import Marca, MarcaDAO


class Controlador:

    def listar(self):
        # Le pedimos la lista completa al DAO; el Controlador no sabe SQL.
        return MarcaDAO.listar()

    def agregar(self, nombre):
        # Validacion de negocio: aqui es donde va, no en el Modelo ni en la Vista.
        if nombre is None or nombre.strip() == "":
            raise ValueError("El nombre no puede estar vacio.")

        nueva = Marca(nombre=nombre, estado=True)
        exito = MarcaDAO.insertar(nueva)
        if not exito:
            raise ValueError("No se pudo guardar la marca en la base de datos.")

    def editar(self, id, nombre):
        if nombre is None or nombre.strip() == "":
            raise ValueError("El nombre no puede estar vacio.")

        # Primero confirmamos que exista antes de intentar actualizarla.
        marca = MarcaDAO.obtener_por_id(id)
        if marca is None:
            raise ValueError(f"No existe una marca con id {id}")

        marca.nombre = nombre
        exito = MarcaDAO.actualizar(marca)
        if not exito:
            raise ValueError("No se pudo actualizar la marca.")

    def eliminar(self, id):
        # Ya NO se borra la fila fisicamente: se desactiva (estado=False).
        # Motivo: producto tiene FK a marca con ON DELETE RESTRICT, asi
        # que borrar de verdad una marca en uso rompe la base de datos.
        marca = MarcaDAO.obtener_por_id(id)
        if marca is None:
            raise ValueError(f"No existe una marca con id {id}")

        exito = MarcaDAO.cambiar_estado(id, False)
        if not exito:
            raise ValueError("No se pudo desactivar la marca.")