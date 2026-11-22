"""
ARCHIVO: reservas.py
PROPÓSITO:
    Representar una reserva que relaciona un cliente con un servicio.
    Controla la duración, el costo y los estados de la reserva.
"""

from datetime import datetime
from entidades import Entidad
from excepciones import (
    ReservaNoValidaError,
    OperacionNoPermitidaError,
    ServicioNoDisponibleError,
)


class Reserva(Entidad):
    # Estados posibles de una reserva.
    ESTADOS = ("PENDIENTE", "CONFIRMADA", "CANCELADA")

    def __init__(self, identificador, cliente, servicio, duracion, costo, parametros=None):
        super().__init__(identificador)

        # Verificar que se reciban objetos cliente y servicio.
        if cliente is None or servicio is None:
            raise ReservaNoValidaError("La reserva requiere un cliente y un servicio.")

        # No permitir reservas de servicios deshabilitados.
        if not servicio.disponible:
            raise ServicioNoDisponibleError("El servicio seleccionado no está disponible.")

        # Validar duración y costo antes de crear la reserva.
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ReservaNoValidaError("La duración debe ser mayor que cero.")
        if not isinstance(costo, (int, float)) or costo <= 0:
            raise ReservaNoValidaError("El costo calculado no es válido.")

        # Relacionar los objetos; no se guardan solamente sus identificadores.
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.costo = float(costo)
        self.parametros = parametros or {}

        # Toda reserva inicia pendiente.
        self.estado = "PENDIENTE"
        self.fecha = datetime.now()

    # Cambia de pendiente a confirmada.
    def confirmar(self):
        if self.estado != "PENDIENTE":
            raise OperacionNoPermitidaError(
                "Solo se pueden confirmar reservas pendientes."
            )
        self.estado = "CONFIRMADA"
        return self.estado

    # Cancela una reserva que todavía no esté cancelada.
    def cancelar(self):
        if self.estado == "CANCELADA":
            raise OperacionNoPermitidaError("La reserva ya está cancelada.")
        self.estado = "CANCELADA"
        return self.estado

    # Procesar requiere que la reserva esté confirmada.
    def procesar(self):
        if self.estado != "CONFIRMADA":
            raise OperacionNoPermitidaError(
                "La reserva debe estar confirmada para procesarse."
            )
        return f"Reserva {self.identificador} procesada correctamente."

    # Implementación de describir() exigida por la clase Entidad.
    def describir(self):
        return (
            f"Reserva {self.identificador} | Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | Duración: {self.duracion} | "
            f"Costo: ${self.costo:,.2f} | Estado: {self.estado}"
        )
