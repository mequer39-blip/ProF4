"""
ARCHIVO: clientes.py
PROPÓSITO:
    Definir la clase Cliente.
    Esta clase hereda de Entidad y protege los datos personales mediante
    propiedades. Cada propiedad valida la información antes de guardarla.
"""

import re
from entidades import Entidad
from excepciones import DatosInvalidosError


class Cliente(Entidad):
    # El constructor recibe los datos y los asigna mediante propiedades.
    # Así se ejecutan las validaciones desde el primer momento.
    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)  # Inicializa los atributos heredados.
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    # ----- Validación y encapsulación del nombre -----
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        # El nombre debe ser texto y contener al menos dos caracteres.
        if not isinstance(valor, str) or len(valor.strip()) < 2:
            raise DatosInvalidosError("El nombre debe tener al menos 2 caracteres.")
        self._nombre = valor.strip()

    # ----- Validación y encapsulación del correo -----
    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        # Expresión regular sencilla para comprobar el formato del correo.
        if not isinstance(valor, str) or not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+", valor.strip()
        ):
            raise DatosInvalidosError("El correo electrónico no tiene un formato válido.")

        # Guardar el correo en minúsculas para mantener uniformidad.
        self._correo = valor.strip().lower()

    # ----- Validación y encapsulación del teléfono -----
    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        # Quitar espacios, guiones y otros caracteres que no sean dígitos.
        numero = re.sub(r"\D", "", str(valor))

        # Aceptar teléfonos de 7 a 15 dígitos.
        if not 7 <= len(numero) <= 15:
            raise DatosInvalidosError("El teléfono debe contener entre 7 y 15 dígitos.")
        self._telefono = numero

    # Implementación del método abstracto heredado de Entidad.
    def describir(self):
        return (
            f"Cliente {self.identificador}: {self.nombre} | "
            f"{self.correo} | {self.telefono}"
        )

    # Permite que print(cliente) muestre información legible.
    def __str__(self):
        return self.describir()
