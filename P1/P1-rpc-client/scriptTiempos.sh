#!/bin/bash

# Función para ejecutar el script Python y extraer el tiempo de ejecución
get_execution_time() {
    local script="$1"  # El script que se debe ejecutar
    # Ejecutar el script y capturar la salida
    output=$(python3 "$script")
    
    # Extraer el tiempo de la salida utilizando 'grep' y 'awk'
    time_taken=$(echo "$output" | grep -oP 'Tiempo invertido en buscar las 1000 entradas una a una: \K[0-9.]+')
    
    # Retornar el tiempo extraído
    echo "$time_taken"
}

# Repeticiones
repetitions=7
vm1_times_1=()
vm1_times_2=()

# Función para calcular el promedio y desviación estándar
calculate_mean_and_stddev() {
    local times=("$@")
    local sum=0
    local count=${#times[@]}
    
    # Calcular la suma de los tiempos
    for time in "${times[@]}"; do
        sum=$(echo "$sum + $time" | bc)
    done
    
    # Calcular el promedio
    mean=$(echo "$sum / $count" | bc -l)
    
    # Calcular la desviación estándar
    sum_sq_diff=0
    for time in "${times[@]}"; do
        diff=$(echo "$time - $mean" | bc -l)
        sq_diff=$(echo "$diff * $diff" | bc -l)
        sum_sq_diff=$(echo "$sum_sq_diff + $sq_diff" | bc -l)
    done
    
    variance=$(echo "$sum_sq_diff / $count" | bc -l)
    stddev=$(echo "scale=6; sqrt($variance)" | bc -l)
    
    # Retornar el promedio y la desviación estándar
    echo "Media: $mean segundos"
    echo "Desviación estándar: $stddev segundos"
}

echo "Ejecutando pruebas..."

# 1. La base de datos está en la máquina virtual VM1 con read_1000_entries_from_db.py
echo -e "\n1. Base de datos en VM1 con read_1000_entries_from_db.py"
for i in $(seq 1 $repetitions); do
    time_taken=$(get_execution_time "read_1000_entries_from_db.py")
    vm1_times_1+=($time_taken)
    echo "Tiempo de ejecución $i: $time_taken segundos"
done
calculate_mean_and_stddev "${vm1_times_1[@]}"


# 3. La base de datos está en VM1 con read_1000_entries_from_db_modified.py
echo -e "\n3. Base de datos en VM1 con read_1000_entries_from_db_modified.py"
for i in $(seq 1 $repetitions); do
    time_taken=$(get_execution_time "read_1000_entries_from_db_modified.py")
    vm1_times_2+=($time_taken)
    echo "Tiempo de ejecución $i: $time_taken segundos"
done
calculate_mean_and_stddev "${vm1_times_2[@]}"


echo -e "\nPruebas completadas."
