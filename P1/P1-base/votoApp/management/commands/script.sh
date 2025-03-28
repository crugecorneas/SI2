#!/bin/bash

# Configuración de rutas y archivos
JMETER_DIR="/ruta/a/jmeter/bin"
RESULTS_DIR="output_users"
OUTPUT_CSV="throughput_results.csv"
OUTPUT_PLOT="throughput_plot.png"

# Comando para conectar a PostgreSQL
PSQL_CMD="psql -h localhost -p 15432 -U alumnodb -d voto"

# Crear archivo CSV para los resultados con cabecera
echo "Usuarios,Throughput" > "$OUTPUT_CSV"

# Lista de usuarios de forma exponencial controlada
USUARIOS_LIST=(1 2 3 4 5 6 7 8 9 10 12 15 20 26 35 40)


# Iterar sobre los valores de la lista
for USUARIOS in "${USUARIOS_LIST[@]}"; do
  echo -e "\n=== Ejecutando prueba con ${USUARIOS} usuarios ==="

  # Limpiar la base de datos antes de cada prueba
  echo "Limpiando datos de la tabla 'voto'..."
  if ! $PSQL_CMD -c "DELETE FROM voto;"; then
    echo "Error al limpiar la base de datos. Continuando de todos modos..."
  fi

  # Ejecutar JMeter
  echo "Iniciando JMeter con ${USUARIOS} usuarios..."
  if ! ./jmeter.sh -n -t P2-projects.jmx -Jusers=${USUARIOS} -l "results_${USUARIOS}.jtl" -Jsummariser.name=summary -e -o "${RESULTS_DIR}_${USUARIOS}"; then
    echo "Error en la ejecución de JMeter para ${USUARIOS} usuarios. Saltando..."
    continue
  fi

  # Procesar resultados
  JSON_FILE="${RESULTS_DIR}_${USUARIOS}/statistics.json"
  if [ -f "$JSON_FILE" ]; then
    echo "Procesando resultados desde $JSON_FILE..."
    
    # Extraer el throughput total usando jq
    THROUGHPUT=$(jq -r '.Total.throughput' "$JSON_FILE")
    
    if [ -n "$THROUGHPUT" ] && [ "$THROUGHPUT" != "null" ]; then
      echo "Throughput para ${USUARIOS} usuarios: ${THROUGHPUT} transacciones/segundo"
      echo "${USUARIOS},${THROUGHPUT}" >> "$OUTPUT_CSV"
    else
      echo "Advertencia: No se pudo extraer el throughput del archivo JSON."
    fi
  else
    echo "Error: No se encontró el archivo statistics.json en ${RESULTS_DIR}_${USUARIOS}"
  fi
done

echo -e "\n=== Proceso completado ==="
echo "Resultados detallados en: $OUTPUT_CSV"

