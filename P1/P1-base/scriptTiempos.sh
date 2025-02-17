#!/bin/bash

# Función para ejecutar el script Python y extraer el tiempo de ejecución
get_execution_time() {
    # Ejecutar el script y capturar la salida
    output=$(python3 read_1000_entries_from_db_modified.py)
    
    # Extraer el tiempo de la salida utilizando 'grep' y 'awk'
    time_taken=$(echo "$output" | grep -oP 'Tiempo invertido en buscar las 1000 entradas una a una: \K[0-9.]+')
    
    # Retornar el tiempo extraído
    echo "$time_taken"
}

# Repeticiones
repetitions=7
vm1_times=()
neon_times=()
django_times=()

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

# 1. La base de datos está en la máquina virtual VM1
#echo -e "\n1. Base de datos en VM1"
#for i in $(seq 1 $repetitions); do
#    time_taken=$(get_execution_time)
#    vm1_times+=($time_taken)
#    echo "Tiempo de ejecución $i: $time_taken segundos"
#done
#calculate_mean_and_stddev "${vm1_times[@]}"

# 2. La base de datos no está en la red local (neon.tech)
#echo -e "\n2. Base de datos en neon.tech"
#for i in $(seq 1 $repetitions); do
#    time_taken=$(get_execution_time)
#    neon_times+=($time_taken)
#    echo "Tiempo de ejecución $i: $time_taken segundos"
#done
#calculate_mean_and_stddev "${neon_times[@]}"

# 3. Acceso a la base de datos mediante el ORM de Django
echo -e "\n3. Acceso mediante el ORM de Django"
for i in $(seq 1 $repetitions); do
    time_taken=$(get_execution_time)
    django_times+=($time_taken)
    echo "Tiempo de ejecución $i: $time_taken segundos"
done
calculate_mean_and_stddev "${django_times[@]}"

echo -e "\nPruebas completadas."
