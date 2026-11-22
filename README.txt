PROYECTO: SOFTWARE FJ
Sistema de gestión de clientes, servicios y reservas con Python y POO.

REQUISITOS
- Python 3.10 o superior.
- No requiere instalar librerías externas.
- No utiliza bases de datos.

CÓMO EJECUTAR
1. Descargue y descomprima Software_FJ_comentado.zip.
2. Abra la carpeta Software_FJ_comentado en Visual Studio Code.
3. Abra Terminal > Nueva terminal.
4. Ejecute: python main.py
   Si ese comando no funciona en Windows, pruebe: py main.py
5. Para ejecutar las 14 pruebas automáticas, seleccione la opción 10.

ARCHIVOS DEL PROYECTO
- main.py: menú principal y demostración de operaciones.
- entidades.py: clase abstracta Entidad.
- clientes.py: clase Cliente y validación de datos personales.
- servicios.py: clase abstracta Servicio y servicios especializados.
- reservas.py: creación, confirmación, cancelación y procesamiento.
- excepciones.py: errores personalizados.
- control_sistema.py: listas internas y registro de eventos.
- logs/registro_eventos.log: archivo de eventos y errores.

CONCEPTOS DE POO
- Abstracción: Entidad y Servicio son clases abstractas.
- Herencia: Cliente y los servicios especializados heredan de clases base.
- Polimorfismo: los servicios implementan su propio cálculo de costos y validación.
- Encapsulación: los datos de Cliente se controlan mediante propiedades.
- Sobrecarga simulada: se utilizan parámetros opcionales en calcular_costo.
  Python no ofrece sobrecarga tradicional de métodos por firma.
- Excepciones: hay excepciones personalizadas, try/except, try/except/else,
  try/except/finally y encadenamiento con raise ... from error.
- Archivos: el log registra eventos y errores; los datos operativos se mantienen
  en listas mientras la aplicación está abierta.

IMPORTANTE
Los clientes, servicios y reservas se almacenan en memoria y se pierden al cerrar
el programa. El archivo de logs permanece guardado en la carpeta logs.
