# connect to the database, read the first 1000 entries
# then perform 1000 queries retrieving each one of the entries
# one by one. Measure the time requiered for the 1000 queries

import psycopg2
import time
# Do not expose your Neon credentials to the browser

# Configuracion de la base de datos
db_config = {
    'dbname': 'voto',  # Nombre de la base de datos
    'user': 'alumnodb',  # Reemplaza con tu usuario de PostgreSQL
    'password': 'npg_QfNYwtd4ERn7',  # Reemplaza con tu contrasegna
    'host': 'ep-steep-pine-a8gb1b6g-pooler.eastus2.azure.neon.tech',  # Cambia si el host es diferente
    'port': 5432,  # Cambia si tu puerto es diferente
}
 
try:
    # Conexion a la base de datos
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    # Leer las primeras 1000 entradas de la tabla censo
    query_fetch_1000 = "SELECT * FROM censo LIMIT 1000"
    cursor.execute(query_fetch_1000)
    rows = cursor.fetchall()

    # Preparar para las busquedas individuales
    search_query = 'SELECT * FROM censo WHERE "numeroDNI" = %s'  # Asumiendo que hay una columna 'id' para identificar las filas

    # Medir el tiempo de inicio
    start_time = time.time()

    # Realizar busquedas una a una
    for row in rows:
        id_value = row[0]  # Suponiendo que la primera columna es el ID
        cursor.execute(search_query, (id_value,))
        cursor.fetchone()  # Obtener la fila encontrada

    # Medir el tiempo de finalizacion
    end_time = time.time()

    # Mostrar los resultados
    print(f"Tiempo invertido en buscar las 1000 entradas una a una: {end_time - start_time:.6f} segundos")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Cerrar el cursor y la conexion
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
