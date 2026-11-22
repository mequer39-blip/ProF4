"""
Servicios:Definir la clase abstracta Servicio y tres clases especializadas:
ReservaSala, AlquilerEquipo y Asesoria.
Cada servicio calcula el costo y valida sus parámetros de manera distinta.
Esto demuestra herencia y polimorfismo.
"""

from abc import abstractmethod
from entidades import Entidad
from excepciones import DatosInvalidosError


class Servicio(Entidad):
    # Constructor común para todos los servicios.
    def __init__(self, identificador, nombre, tarifa_base, disponible=True):
        super().__init__(identificador)

        # Validar el nombre del servicio.
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError("El nombre del servicio es obligatorio.")

        # Validar que la tarifa sea numérica y positiva.
        if isinstance(tarifa_base, bool) or not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise DatosInvalidosError("La tarifa base debe ser un número mayor que cero.")

        self.nombre = nombre.strip()
        self.tarifa_base = float(tarifa_base)
        self.disponible = bool(disponible)

    # Método abstracto: cada servicio debe calcular su costo.
    @abstractmethod
    def calcular_costo(self, *args, **kwargs):
        pass

    # Método abstracto: cada servicio valida sus parámetros específicos.
    @abstractmethod
    def validar_parametros(self, **kwargs):
        pass

    # Descripción general heredable por los servicios especializados.
    def describir(self):
        return (
            f"{self.nombre} (ID: {self.identificador}) - "
            f"Tarifa base: ${self.tarifa_base:,.0f}"
        )

    # Método auxiliar compartido para aplicar impuesto y descuento.
    def _aplicar_impuestos_descuento(self, subtotal, impuesto=0.19, descuento=0):
        # Los porcentajes se expresan como decimales: 0.19 equivale al 19 %.
        if not isinstance(impuesto, (int, float)) or not 0 <= impuesto <= 1:
            raise DatosInvalidosError("El impuesto debe estar entre 0 y 1.")
        if not isinstance(descuento, (int, float)) or not 0 <= descuento <= 1:
            raise DatosInvalidosError("El descuento debe estar entre 0 y 1.")

        # Primero se descuenta y luego se aplica el impuesto.
        total = subtotal * (1 - descuento) * (1 + impuesto)
        return round(total, 2)


# SERVICIO 1: reserva de salas por hora.
class ReservaSala(Servicio):
    def __init__(self, identificador, tarifa_hora, capacidad, disponible=True):
        super().__init__(identificador, "Reserva de sala", tarifa_hora, disponible)

        # La capacidad debe ser un número entero positivo.
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatosInvalidosError("La capacidad debe ser un entero positivo.")
        self.capacidad = capacidad

    def validar_parametros(self, **kwargs):
        # Se comprueba cuántas personas utilizarán la sala.
        personas = kwargs.get("personas")
        if not isinstance(personas, int) or personas <= 0:
            raise DatosInvalidosError("Indique una cantidad válida de personas.")
        if personas > self.capacidad:
            raise DatosInvalidosError(
                f"La sala admite máximo {self.capacidad} personas."
            )

    def calcular_costo(self, horas, impuesto=0.19, descuento=0, personas=1):
        self.validar_parametros(personas=personas)
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise DatosInvalidosError("Las horas deben ser mayores que cero.")
        subtotal = self.tarifa_base * horas
        return self._aplicar_impuestos_descuento(subtotal, impuesto, descuento)


# SERVICIO 2: alquiler de equipos por día y por unidad.
class AlquilerEquipo(Servicio):
    def __init__(self, identificador, tarifa_dia, unidades_disponibles, disponible=True):
        super().__init__(identificador, "Alquiler de equipos", tarifa_dia, disponible)

        if not isinstance(unidades_disponibles, int) or unidades_disponibles < 0:
            raise DatosInvalidosError("Las unidades disponibles no pueden ser negativas.")
        self.unidades_disponibles = unidades_disponibles

    def validar_parametros(self, **kwargs):
        unidades = kwargs.get("unidades")
        if not isinstance(unidades, int) or unidades <= 0:
            raise DatosInvalidosError("La cantidad de equipos debe ser un entero positivo.")
        if unidades > self.unidades_disponibles:
            raise DatosInvalidosError(
                f"Solo hay {self.unidades_disponibles} equipos disponibles."
            )

    def calcular_costo(self, dias, unidades=1, impuesto=0.19, descuento=0):
        self.validar_parametros(unidades=unidades)
        if not isinstance(dias, (int, float)) or dias <= 0:
            raise DatosInvalidosError("Los días deben ser mayores que cero.")
        subtotal = self.tarifa_base * dias * unidades
        return self._aplicar_impuestos_descuento(subtotal, impuesto, descuento)


# SERVICIO 3: asesorías especializadas por hora.
class Asesoria(Servicio):
    def __init__(self, identificador, tarifa_hora, especialidad, disponible=True):
        super().__init__(identificador, "Asesoría especializada", tarifa_hora, disponible)

        if not isinstance(especialidad, str) or not especialidad.strip():
            raise DatosInvalidosError("La especialidad es obligatoria.")
        self.especialidad = especialidad.strip()

    def validar_parametros(self, **kwargs):
        tema = kwargs.get("tema", self.especialidad)
        if not isinstance(tema, str) or not tema.strip():
            raise DatosInvalidosError("El tema de la asesoría es obligatorio.")

    def calcular_costo(self, horas, impuesto=0.19, descuento=0):
        self.validar_parametros()
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise DatosInvalidosError("Las horas deben ser mayores que cero.")
        subtotal = self.tarifa_base * horas
        return self._aplicar_impuestos_descuento(subtotal, impuesto, descuento)
