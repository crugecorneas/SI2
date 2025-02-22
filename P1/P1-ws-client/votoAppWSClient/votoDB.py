import requests
from django.conf import settings

RESTAPIBASEURL = settings.RESTAPIBASEURL


def verificar_censo(censo_data):
    """ Verifica si el votante está registrado en el Censo """
    if not censo_data:
        return False
    
    url = f"{RESTAPIBASEURL}verificar_censo/"
    print(url)
    response = requests.get(url, json=censo_data)
    
    return response.status_code == 200 and response.json().get("valid", False)


def registrar_voto(voto_dict):
    """ Registra un voto en el sistema a través del API REST """
    url = f"{RESTAPIBASEURL}registrar_voto/"
    response = requests.post(url, json=voto_dict)
    
    if response.status_code == 201:
        return response.json()
    else:
        print("Error: Registrando voto:", response.text)
        return None


def eliminar_voto(idVoto):
    """ Elimina un voto en el sistema a través del API REST """
    url = f"{RESTAPIBASEURL}eliminar_voto/{idVoto}/"
    response = requests.delete(url)
    
    return response.status_code == 204


def get_votos_from_db(idProcesoElectoral):
    """ Obtiene los votos asociados a un proceso electoral """
    url = f"{RESTAPIBASEURL}get_votos/{idProcesoElectoral}/"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Error: Obteniendo votos:", response.text)
        return []
