from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Censo
from .serializers import CensoSerializer


class CensoView(APIView):
    def post(self, request):
        """
        Valida si un votante está en el censo electoral.
        """
        serializer = CensoSerializer(data=request.data)
        
        if serializer.is_valid():
            censo_data = serializer.validated_data
            
            if Censo.objects.filter(**censo_data).exists():
                return Response({'message': 'Votante encontrado en el Censo.'}, status=status.HTTP_200_OK)
            
            return Response({'message': 'Datos no encontrados en Censo.'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

