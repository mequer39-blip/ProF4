"""
ARCHIVO: excepciones.py
PROPÓSITO:
    Definir errores propios del proyecto Software FJ.
    Estas excepciones permiten identificar qué tipo de problema ocurrió
    y mostrar mensajes claros sin cerrar inesperadamente la aplicación.
"""

# Excepción general: las excepciones específicas del proyecto heredan de esta.
class SoftwareFJError(Exception):
    """Clase base para los errores controlados de Software FJ."""
    pass


# Se utiliza cuando un nombre, correo, teléfono, tarifa u otro dato es incorrecto.
class DatosInvalidosError(SoftwareFJError):
    """Indica que un dato ingresado no cumple las reglas de validación."""
    pass


# Se utiliza cuando se consulta un cliente que no está registrado.
class ClienteNoEncontradoError(SoftwareFJError):
    """Indica que el cliente solicitado no existe en la lista interna."""
    pass


# Se utiliza cuando un servicio no existe o no puede utilizarse.
class ServicioNoDisponibleError(SoftwareFJError):
    """Indica que el servicio no está registrado o no está disponible."""
    pass


# Se utiliza cuando una reserva tiene datos incorrectos o no puede crearse.
class ReservaNoValidaError(SoftwareFJError):
    """Indica que la reserva no cumple las condiciones del sistema."""
    pass


# Se utiliza cuando se intenta confirmar, cancelar o procesar en un estado incorrecto.
class OperacionNoPermitidaError(SoftwareFJError):
    """Indica que la operación solicitada no está permitida."""
    pass
