import os
import sys
import django
import pika

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'votoSite.settings')
django.setup()

from votoAppRPCServer.models import Censo, Voto

def main():
    if len(sys.argv) != 3:
        print("Debe indicar el host y el puerto")
        exit()
    
    hostname = sys.argv[1]
    port = sys.argv[2]
    
    # TODO: completar según las indicaciones

    credentials = pika.PlainCredentials('alumnomq', 'alumnomq')
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=hostname,port=port,credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='voto_cancelacion')
    
    def callback(ch, method, properties, body):
        idVoto = body.decode()
        print(f"Voto recibido: {idVoto}")
        try:
            voto = Voto.objects.get(id=idVoto)
            voto.codigoRespuesta='111'
            voto.save()
            print(f"Voto {idVoto} eliminado correctamente")
        except Voto.DoesNotExist:
            print(f"Voto {idVoto} no registrado")


    channel.basic_consume(queue='voto_cancelacion', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    main()
