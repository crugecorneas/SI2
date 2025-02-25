from django.conf import settings
from xmlrpc.client import ServerProxy

def verificar_censo(censo_data):
    """ 
    Verifica si el votante está registrado en el censo.
    
    :param censo_data: Diccionario con los datos del votante, que son proporcionados 
                       por el formulario CensoForm. Ejemplo: {'numeroDNI': '12345678A', 'nombre': 'Juan'}
                       
    :return: True si el votante está registrado en el censo, False si no está registrado o si censo_data 
             no es válido (vacío o no coincide con ningún registro).
    
    La función invoca el procedimiento remoto 'verificar_censo' en el servidor RPC y devuelve el resultado.
    Si hay algún error al realizar la llamada remota, se captura la excepción y se devuelve False.
    """
    try:
        with ServerProxy(settings.RPCAPIBASEURL) as proxy:
            # Invocar el procedimiento remoto para verificar el censo
            return proxy.verificar_censo(censo_data)
    except Exception as e:
        print("Error: Verificando censo: ", e)
        return False


def registrar_voto(voto_dict):
    """ 
    Registra un voto en la base de datos.

    :param voto_dict: Diccionario con los datos del voto, proporcionados por el formulario VotoForm.
                       Debe incluir información como: {'censo_id': '12345678A', 'idProcesoElectoral': 1, 'voto': 'A'}
    
    :return: Información del voto registrado si la operación es exitosa, None si falla.

    La función invoca el procedimiento remoto 'registrar_voto' en el servidor RPC. Si el registro es exitoso, 
    devuelve la información del voto registrado. Si ocurre un error, la excepción se captura y se devuelve None.
    """
    try:
        with ServerProxy(settings.RPCAPIBASEURL) as proxy:
            # Invocar el procedimiento remoto para registrar el voto
            return proxy.registrar_voto(voto_dict)
    except Exception as e:
        print("Error: Registrando voto: ", e)
        return None


def eliminar_voto(idVoto):
    """ 
    Elimina un voto de la base de datos.

    :param idVoto: ID del voto que se desea eliminar. Es un valor único que identifica un voto específico.
                    Ejemplo: 12345
    
    :return: True si la eliminación fue exitosa, False si hubo algún error (como no encontrar el voto).

    La función invoca el procedimiento remoto 'eliminar_voto' en el servidor RPC. Si el voto se elimina correctamente,
    devuelve True. Si ocurre un error (por ejemplo, si el voto no existe), captura la excepción y devuelve False.
    """
    try:
        with ServerProxy(settings.RPCAPIBASEURL) as proxy:
            # Invocar el procedimiento remoto para eliminar el voto
            return proxy.eliminar_voto(idVoto)
    except Exception as e:
        print("Error: Eliminando voto: ", e)
        return False


def get_votos_from_db(idProcesoElectoral):
    """ 
    Obtiene los votos de un proceso electoral desde la base de datos.

    :param idProcesoElectoral: ID del proceso electoral. Es un identificador único para el proceso electoral 
                               (por ejemplo, un número que representa las elecciones de un año y región específica).
    
    :return: Lista de votos encontrados en el proceso electoral especificado. Cada voto puede ser un diccionario 
             o un objeto que contiene la información relevante, como el ID del voto, el censo_id, el resultado del voto, etc.

    La función invoca el procedimiento remoto 'get_votos_from_db' en el servidor RPC para obtener los votos 
    asociados a un proceso electoral. Si la llamada remota es exitosa, devuelve los votos. En caso de error, 
    captura la excepción y devuelve una lista vacía.
    """
    try:
        with ServerProxy(settings.RPCAPIBASEURL) as proxy:
            # Invocar el procedimiento remoto para obtener los votos
            return proxy.get_votos_from_db(idProcesoElectoral)
    except Exception as e:
        print("Error: Obteniendo votos: ", e)
        return []
