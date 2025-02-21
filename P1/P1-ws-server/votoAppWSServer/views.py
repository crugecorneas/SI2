from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Censo, Voto
from .serializers import CensoSerializer, VotoSerializer
from django.forms.models import model_to_dict


class CensoView(APIView):
    def post(self, request):
        """
        Valida si un votante está en el censo electoral.
        """
        numeroDNI = request.data.get('numeroDNI')
        nombre = request.data.get('nombre')
        fechaNacimiento = request.data.get('fechaNacimiento')
        anioCenso = request.data.get('anioCenso')
        codigoAutorizacion = request.data.get('codigoAutorizacion')

        censo_exists = Censo.objects.filter(
            numeroDNI=numeroDNI,
            nombre=nombre,
            fechaNacimiento=fechaNacimiento,
            anioCenso=anioCenso,
            codigoAutorizacion=codigoAutorizacion
        ).exists()

        if censo_exists:
            return Response({'message': 'Votante encontrado en el Censo.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Datos no encontrados en el Censo.'}, status=status.HTTP_404_NOT_FOUND)
    


class VotoView(APIView):
    def post(self, request):
        """
        Crea un voto si el votante existe en el censo electoral.
        """
        censo_id = request.data.get('censo_id')
        idCircunscripcion = request.data.get('idCircunscripcion')
        idMesaElectoral = request.data.get('idMesaElectoral')
        idProcesoElectoral = request.data.get('idProcesoElectoral')
        nombreCandidatoVotado = request.data.get('nombreCandidatoVotado')

        # Buscar el censo del votante
        try:
            censo = Censo.objects.get(numeroDNI=censo_id)
        except Censo.DoesNotExist:
            return Response({'message': 'Votante no encontrado en el Censo.'}, status=status.HTTP_404_NOT_FOUND)

        # Crear el voto
        voto = Voto.objects.create(
            idCircunscripcion=idCircunscripcion,
            idMesaElectoral=idMesaElectoral,
            idProcesoElectoral=idProcesoElectoral,
            nombreCandidatoVotado=nombreCandidatoVotado,
            censo=censo
        )
        voto_dict = model_to_dict(voto)
        return Response(voto_dict, status=status.HTTP_200_OK)
    
    def delete(self, request, id_voto):
        """
        Elimina un voto existente por su identificador.
        """
        try:
            voto = Voto.objects.get(id=id_voto)
        except Voto.DoesNotExist:
            return Response({'message': 'Voto no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        voto.delete()
        
        return Response({'message': 'Voto eliminado correctamente.'}, status=status.HTTP_200_OK)
    

class ProcesoElectoralView(APIView):
    def get(self, request, idProcesoElectoral):
        """
        Devuelve la lista de votos asociados a un proceso electoral específico.
        """
        votos = Voto.objects.filter(idProcesoElectoral=idProcesoElectoral)

        if not votos.exists():
            return Response({'message': 'No se encontraron votos para este proceso electoral.'}, 
                            status=status.HTTP_404_NOT_FOUND)
        
        # Serializar los votos encontrados
        votos_serializer = VotoSerializer(votos, many=True)
        
        return Response(votos_serializer.data, status=status.HTTP_200_OK)