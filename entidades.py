""" 
Entidades: Crear la clase abstracta Entidad.
Una entidad es cualquier elemento del sistema que necesita identificador.
Se usa abstracción porque no se crearán objetos Entidad directamente:
las clases concretas deberán heredar de ella e implementar describir().
"""

from abc import ABC, abstractmethod
from datetime import datetime


class Entidad(ABC):
    # El constructor inicializa los datos comunes de todas las entidades.
    def __init__(self, identificador):
        # Validar que el identificador no esté vacío.
        if identificador is None or not str(identificador).strip():
            raise ValueError("El identificador es obligatorio.")

        # El guion bajo indica que el atributo se maneja como protegido.
        self._identificador = str(identificador).strip()

        # Registrar automáticamente la fecha y hora de creación.
        self._fecha_creacion = datetime.now()

    # @property permite consultar el identificador sin modificarlo directamente.
    @property
    def identificador(self):
        return self._identificador

    # Propiedad de solo lectura para conocer cuándo se creó la entidad.
    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    # Método abstracto: cada clase hija debe definir su propia descripción.
    @abstractmethod
    def describir(self):
        """Devuelve la información principal de la entidad."""
        pass
