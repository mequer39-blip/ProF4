"""
ARCHIVO: main.py
PROPÓSITO:
    Punto de entrada del programa.
    Presenta el menú, recibe información del usuario y llama a las clases
    encargadas de realizar cada operación.
"""

import logging

from clientes import Cliente
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from control_sistema import ControlSistema

# Crear una única instancia que administra las listas del sistema.
sistema = ControlSistema()


def ejecutar_demo():
    """
    Ejecuta 14 pruebas automáticas.
    Incluye operaciones correctas e incorrectas para comprobar que el sistema
    captura los errores y continúa con las pruebas siguientes.
    """
    print("\n========== DEMOSTRACIÓN AUTOMÁTICA ==========")
    operaciones = 0

    # Función auxiliar para ejecutar cada prueba sin detener toda la demostración.
    def probar(titulo, accion):
        nonlocal operaciones
        operaciones += 1
        print(f"\n{operaciones}. {titulo}")

        try:
            # Ejecutar la operación que se recibe como parámetro.
            resultado = accion()
        except Exception as error:
            # Si ocurre un error, se registra y se muestra un mensaje controlado.
            logging.exception("Operación de demostración fallida: %s", titulo)
            print(f"   ERROR CONTROLADO: {error}")
        else:
            # El bloque else se ejecuta únicamente si el try terminó sin errores.
            if resultado is not None:
                print("   OK:", resultado)
        finally:
            # finally se ejecuta siempre, haya ocurrido un error o no.
            print("   Prueba finalizada.")

    # 1. Registro válido de cliente.
    probar("Registrar cliente válido", lambda: sistema.registrar_cliente(
        Cliente("C001", "Laura Gómez", "laura@example.com", "3001234567")))

    # 2. Intento de registro con correo inválido.
    probar("Intentar registrar cliente con correo inválido", lambda:
        Cliente("C002", "Carlos Pérez", "correo-invalido", "3007654321"))

    # 3. Registro de un segundo cliente.
    probar("Registrar segundo cliente", lambda: sistema.registrar_cliente(
        Cliente("C003", "Andrés Ruiz", "andres@example.com", "3105557788")))

    # 4. Creación de servicio de salas.
    probar("Crear servicio de reserva de sala", lambda: sistema.agregar_servicio(
        ReservaSala("S001", 50000, 20)))

    # 5. Creación de servicio de alquiler.
    probar("Crear servicio de alquiler de equipos", lambda: sistema.agregar_servicio(
        AlquilerEquipo("S002", 30000, 5)))

    # 6. Creación de servicio de asesoría.
    probar("Crear servicio de asesoría", lambda: sistema.agregar_servicio(
        Asesoria("S003", 80000, "Ciberseguridad")))

    # 7. Intento de crear una sala con capacidad incorrecta.
    probar("Intentar crear sala con capacidad inválida", lambda:
        ReservaSala("S004", 40000, 0))

    # 8. Crear una reserva correcta de sala.
    probar("Crear reserva de sala", lambda: sistema.crear_reserva(
        "R001", "C001", "S001", 2, impuesto=0.19, descuento=0.10, personas=8))

    # 9. Intentar alquilar más equipos que los disponibles.
    probar("Intentar alquilar más equipos de los disponibles", lambda:
        sistema.crear_reserva("R002", "C001", "S002", 2, unidades=10))

    # 10. Crear reserva correcta de asesoría.
    probar("Crear reserva de asesoría", lambda: sistema.crear_reserva(
        "R003", "C003", "S003", 1, impuesto=0.19))

    # 11. Confirmar la primera reserva.
    probar("Confirmar reserva R001", lambda: sistema.reservas[0].confirmar())

    # 12. Procesar una reserva confirmada.
    probar("Procesar reserva confirmada", lambda: sistema.reservas[0].procesar())

    # 13. Cancelar la segunda reserva creada (R003).
    probar("Cancelar reserva R003", lambda: sistema.reservas[1].cancelar())

    # 14. Intentar procesar una reserva cancelada.
    probar("Intentar procesar reserva cancelada", lambda:
        sistema.reservas[1].procesar())

    print(f"\nDemostración terminada: {operaciones} operaciones ejecutadas.")
    print("Revise logs/registro_eventos.log para consultar los eventos y errores.")


def pedir_numero(mensaje):
    """
    Solicita un número positivo.
    Incluye try/except/else para separar la validación de la conversión correcta.
    """
    valor = input(mensaje).strip()

    try:
        numero = float(valor)
        if numero <= 0:
            raise ValueError("El valor debe ser mayor que cero.")
    except ValueError as error:
        # Capturar entradas no numéricas o valores que no sean positivos.
        logging.exception("Entrada numérica inválida")
        raise ValueError(f"Entrada no válida: {error}") from error
    else:
        # Se llega aquí cuando la conversión y validación fueron exitosas.
        return numero
    finally:
        # Este bloque se ejecuta incluso cuando la entrada es incorrecta.
        # Se deja disponible como evidencia del uso de finally.
        pass


def menu():
    """Mantiene activa la aplicación hasta que el usuario elija salir."""
    while True:
        print("""
========== SOFTWARE FJ ==========
1. Registrar cliente
2. Crear servicio
3. Crear reserva
4. Confirmar reserva
5. Cancelar reserva
6. Procesar reserva
7. Listar clientes
8. Listar servicios
9. Listar reservas
10. Ejecutar demostración de 14 operaciones
0. Salir
""")

        opcion = input("Seleccione una opción: ").strip()

        try:
            # OPCIÓN 1: pedir los datos y registrar un cliente.
            if opcion == "1":
                cliente = Cliente(
                    input("ID: "),
                    input("Nombre: "),
                    input("Correo: "),
                    input("Teléfono: "),
                )
                sistema.registrar_cliente(cliente)
                print("Cliente registrado correctamente.")

            # OPCIÓN 2: crear uno de los tres tipos de servicio.
            elif opcion == "2":
                print("1. Sala  2. Alquiler de equipos  3. Asesoría")
                tipo = input("Tipo: ").strip()
                identificador = input("ID del servicio: ").strip()
                tarifa = pedir_numero("Tarifa base: $")

                if tipo == "1":
                    capacidad = int(pedir_numero("Capacidad de la sala: "))
                    servicio = ReservaSala(identificador, tarifa, capacidad)
                elif tipo == "2":
                    unidades = int(pedir_numero("Unidades disponibles: "))
                    servicio = AlquilerEquipo(identificador, tarifa, unidades)
                elif tipo == "3":
                    especialidad = input("Especialidad: ")
                    servicio = Asesoria(identificador, tarifa, especialidad)
                else:
                    raise ValueError("Tipo de servicio inexistente.")

                sistema.agregar_servicio(servicio)
                print("Servicio creado correctamente.")

            # OPCIÓN 3: buscar cliente y servicio, calcular costo y crear reserva.
            elif opcion == "3":
                id_reserva = input("ID de reserva: ").strip()
                id_cliente = input("ID del cliente: ").strip()
                id_servicio = input("ID del servicio: ").strip()
                duracion = pedir_numero("Duración (horas o días): ")

                servicio = sistema.buscar_servicio(id_servicio)
                extras = {}

                # Solicitar parámetros adicionales según el tipo de servicio.
                if isinstance(servicio, AlquilerEquipo):
                    extras["unidades"] = int(pedir_numero("Cantidad de equipos: "))
                elif isinstance(servicio, ReservaSala):
                    extras["personas"] = int(pedir_numero("Cantidad de personas: "))

                reserva = sistema.crear_reserva(
                    id_reserva, id_cliente, id_servicio, duracion, **extras
                )
                print(reserva.describir())

            # OPCIONES 4, 5 y 6: localizar reserva y cambiar su estado.
            elif opcion in ("4", "5", "6"):
                id_reserva = input("ID de reserva: ").strip()
                reserva = next(
                    (r for r in sistema.reservas if r.identificador == id_reserva),
                    None,
                )

                if reserva is None:
                    raise ValueError("No se encontró la reserva.")

                if opcion == "4":
                    reserva.confirmar()
                    print("Reserva confirmada.")
                elif opcion == "5":
                    reserva.cancelar()
                    print("Reserva cancelada.")
                else:
                    print(reserva.procesar())

            # OPCIONES 7, 8 y 9: mostrar las listas en memoria.
            elif opcion == "7":
                print(sistema.listar(sistema.clientes))
            elif opcion == "8":
                print(sistema.listar(sistema.servicios))
            elif opcion == "9":
                print(sistema.listar(sistema.reservas))

            # OPCIÓN 10: ejecutar pruebas automáticas.
            elif opcion == "10":
                ejecutar_demo()

            # OPCIÓN 0: terminar el ciclo y cerrar la aplicación.
            elif opcion == "0":
                print("Aplicación finalizada.")
                break

            # Cualquier otra entrada se considera una opción inválida.
            else:
                raise ValueError("Seleccione una opción válida del menú.")

        except Exception as error:
            # Capturar el error para que no cierre el programa.
            logging.exception("Error controlado en el menú principal")
            print(f"\nNo se pudo completar la operación: {error}")
            print("El sistema continúa activo.")
        finally:
            # Se ejecuta al terminar cada vuelta del menú, incluso ante errores.
            # No se cierra el programa aquí; el ciclo while mantiene la aplicación.
            pass


# Este condicional evita que el menú se ejecute al importar main.py desde otro módulo.
if __name__ == "__main__":
    print("Software FJ - Sistema de gestión sin base de datos")
    print("Los datos operativos se mantienen en memoria durante la ejecución.")
    menu()
