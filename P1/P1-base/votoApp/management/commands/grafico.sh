#!/bin/bash

INPUT_CSV="throughput_results.csv"
OUTPUT_PLOT="throughput_enhanced.png"

# Configuración de estilo mejorada
gnuplot << EOF
set terminal pngcairo enhanced font "Arial,12" size 1600,1200
set output '$OUTPUT_PLOT'
set title "Throughput Detallado" font "Arial-Bold,16"
set xlabel "Número de Usuarios" font "Arial-Bold,14"
set ylabel "Throughput (transacciones/segundo)" font "Arial-Bold,14"
set grid xtics ytics lt 0 lw 1 lc rgb "#dddddd"
set key top right box

# Estilo mejorado para líneas y puntos
set style line 1 lc rgb '#0060ad' lt 1 lw 2 pt 7 ps 1.2   # Línea principal + puntos
set style line 2 lc rgb '#dd181f' lt 1 lw 1 pt 5 ps 0.8   # Puntos alternativos
set pointintervalbox 2                                   # Espaciado de puntos

# Ajuste automático de ejes con márgenes
set autoscale xy
set offsets graph 0.1, 0.1, 0.1, 0.1

# Configurar separador CSV y saltar encabezado
set datafile separator ","
plot '$INPUT_CSV' every ::1 using 1:2 with linespoints ls 1 title "Throughput", \
     '' every 2::1 using 1:2 with points ls 2 notitle    # Puntos adicionales para mejor visualización
EOF

echo "Gr�fico mejorado generado: $OUTPUT_PLOT"
