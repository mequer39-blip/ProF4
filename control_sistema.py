"""
control_sistema: Coordinar el funcionamiento general del sistema.
Mantiene clientes, servicios y reservas en listas internas.
También registra eventos y errores en un archivo de texto (log).
"""

import logging
from pathlib import Path

from clientes import Cliente
from reservas import Reserva
from excepciones import (
    ClienteNoEncontradoError,
    ServicioNoDisponibleError,
    ReservaNoValidaError,
)

# Crear la carpeta logs si todavía no existe.
RUTA_LOGS = Path(__file__).parent / "logs"
RUTA_LOGS.mkdir(parents=True, exist_ok=True)
ARCHIVO_LOG = RUTA_LOGS / "registro_eventos.log"

# Configurar el registro: fecha, nivel del mensaje y descripción.
logging.basicConfig(
    filename=ARCHIVO_LOG,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)
logger = logging.getLogger("SoftwareFJ")


class ControlSistema:
    def __init__(self):
        # Estas listas son la memoria temporal del programa.
        # No se utiliza ningún motor de base de datos.
        self.clientes = []
        self.servicios = []
        self.reservas = []

    # Registrar cliente y evitar identificadores repetidos.
    def registrar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise TypeError("El objeto proporcionado no es un Cliente.")
        if any(c.identificador == cliente.identificador for c in self.clientes):
            raise ValueError("Ya existe un cliente con ese identificador.")

        self.clientes.append(cliente)
        logger.info("Cliente registrado: %s", cliente.identificador)
        return cliente

    # Agregar servicio y evitar identificadores duplicados.
    def agregar_servicio(self, servicio):
        from servicios import Servicio

        if not isinstance(servicio, Servicio):
            raise TypeError("El objeto proporcionado no es un Servicio.")
        if any(s.identificador == servicio.identificador for s in self.servicios):
            raise ValueError("Ya existe un servicio con ese identificador.")

        self.servicios.append(servicio)
        logger.info("Servicio agregado: %s", servicio.identificador)
        return servicio

    # Buscar cliente por identificador.
    def buscar_cliente(self, identificador):
        for cliente in self.clientes:
            if cliente.identificador == str(identificador):
                return cliente
        raise ClienteNoEncontradoError(f"No existe el cliente {identificador}.")

    # Buscar servicio por identificador.
    def buscar_servicio(self, identificador):
        for servicio in self.servicios:
            if servicio.identificador == str(identificador):
                return servicio
        raise ServicioNoDisponibleError(f"No existe el servicio {identificador}.")

    # Crear una reserva: buscar objetos, validar servicio y calcular costo.
    def crear_reserva(self, id_reserva, id_cliente, id_servicio, duracion, **parametros):
        try:
            cliente = self.buscar_cliente(id_cliente)
            servicio = self.buscar_servicio(id_servicio)

            if not servicio.disponible:
                raise ServicioNoDisponibleError(
                    "El servicio está marcado como no disponible."
                )

            # Polimorfismo: se ejecuta el calcular_costo propio del servicio elegido.
            costo = servicio.calcular_costo(duracion, **parametros)

            # Crear el objeto Reserva y almacenarlo en la lista interna.
            reserva = Reserva(
                id_reserva, cliente, servicio, duracion, costo, parametros
            )
            self.reservas.append(reserva)
            logger.info("Reserva creada: %s", id_reserva)
            return reserva

        except Exception as error:
            # logger.exception guarda el error y su rastreo técnico en el archivo.
            logger.exception("Error al crear reserva %s", id_reserva)

            # Encadenamiento de excepciones: 'from error' conserva la causa original.
            raise ReservaNoValidaError(
                f"No fue posible crear la reserva {id_reserva}: {error}"
            ) from error

    # Convertir una lista de objetos en texto para mostrarla en consola.
    def listar(self, elementos):
        if not elementos:
            return "No hay registros."

        # Todos los elementos tienen describir(), lo que aprovecha el polimorfismo.
        return "\n".join(elemento.describir() for elemento in elementos)
