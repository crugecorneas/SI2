
import time
import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'votoSite.settings')
django.setup()

from votoApp.models import Censo


def realizar_busquedas():
    # Medir el tiempo de inicio
    start_time = time.time()

    # Obtener las primeras 1000 entradas de la tabla 'censo'
    censos = Censo.objects.all()[:1000]  # O usando `.filter()` si necesitas aplicar algún filtro

    # Realizar búsquedas una por una
    for censo in censos:
        # Obtener el censo usando el 'numeroDNI'
        try:
            censo_encontrado = Censo.objects.get(numeroDNI=censo.numeroDNI)
            # Realiza cualquier procesamiento con censo_encontrado si es necesario
        except Censo.DoesNotExist:
            # Si no se encuentra un censo, manejar el caso de error
            print(f"Censo con numeroDNI {censo.numeroDNI} no encontrado.")
    
    # Medir el tiempo de finalización
    end_time = time.time()

    # Mostrar los resultados
    print(f"Tiempo invertido en buscar las 1000 entradas una a una: {end_time - start_time:.6f} segundos")
realizar_busquedas()