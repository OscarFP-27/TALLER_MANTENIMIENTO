"""
controlador/ctr_linea.py
=========================
El CONTROLADOR: es el "intermediario" entre la Vista y el Modelo.
Ya NO lee ni escribe un archivo de texto: le pide todo al LineaDAO
(que es quien habla con PostgreSQL). Aqui viven las VALIDACIONES
de negocio (ej. no permitir nombres vacios).

La Linea sigue siendo un catalogo INDEPENDIENTE de la Categoria:
este Controlador no sabe nada de ctr_categoria ni lo necesita.
"""

from modelo.mdl_linea import Linea, LineaDAO


class Controlador:

    def listar(self):
        return LineaDAO.listar()

    def agregar(self, nombre):
        if nombre is None or nombre.strip() == "":
            raise ValueError("El nombre no puede estar vacio.")

        nueva = Linea(nombre=nombre, estado=True)
        exito = LineaDAO.insertar(nueva)
        if not exito:
            raise ValueError("No se pudo guardar la linea en la base de datos.")

    def editar(self, id, nombre):
        if nombre is None or nombre.strip() == "":
            raise ValueError("El nombre no puede estar vacio.")

        linea = LineaDAO.obtener_por_id(id)
        if linea is None:
            raise ValueError(f"No existe una linea con id {id}")

        linea.nombre = nombre
        exito = LineaDAO.actualizar(linea)
        if not exito:
            raise ValueError("No se pudo actualizar la linea.")

    def eliminar(self, id):
        # Ya NO se borra la fila fisicamente: se desactiva (estado=False).
        # Motivo: producto tiene FK a linea con ON DELETE RESTRICT.
        linea = LineaDAO.obtener_por_id(id)
        if linea is None:
            raise ValueError(f"No existe una linea con id {id}")

        exito = LineaDAO.cambiar_estado(id, False)
        if not exito:
            raise ValueError("No se pudo desactivar la linea.")