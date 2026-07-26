"""
controlador/ctr_categoria.py
=============================
El CONTROLADOR: es el "intermediario" entre la Vista y el Modelo.
Ya NO lee ni escribe un archivo de texto: le pide todo al
CategoriaDAO (que es quien habla con PostgreSQL). Aqui viven las
VALIDACIONES de negocio (ej. no permitir nombres vacios).
"""

from modelo.mdl_categoria import Categoria, CategoriaDAO


class Controlador:

    def listar(self):
        return CategoriaDAO.listar()

    def agregar(self, nombre):
        if nombre is None or nombre.strip() == "":
            raise ValueError("El nombre no puede estar vacio.")

        nueva = Categoria(nombre=nombre, estado=True)
        exito = CategoriaDAO.insertar(nueva)
        if not exito:
            raise ValueError("No se pudo guardar la categoria en la base de datos.")

    def editar(self, id, nombre):
        if nombre is None or nombre.strip() == "":
            raise ValueError("El nombre no puede estar vacio.")

        categoria = CategoriaDAO.obtener_por_id(id)
        if categoria is None:
            raise ValueError(f"No existe una categoria con id {id}")

        categoria.nombre = nombre
        exito = CategoriaDAO.actualizar(categoria)
        if not exito:
            raise ValueError("No se pudo actualizar la categoria.")

    def eliminar(self, id):
        # Ya NO se borra la fila fisicamente: se desactiva (estado=False).
        # Motivo: producto tiene FK a categoria con ON DELETE RESTRICT.
        categoria = CategoriaDAO.obtener_por_id(id)
        if categoria is None:
            raise ValueError(f"No existe una categoria con id {id}")

        exito = CategoriaDAO.cambiar_estado(id, False)
        if not exito:
            raise ValueError("No se pudo desactivar la categoria.")