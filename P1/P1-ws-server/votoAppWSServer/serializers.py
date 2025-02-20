from rest_framework import serializers
from .models import Censo, Voto

class CensoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Censo
        fields = ['numeroDNI', 'nombre', 'fechaNacimiento', 'anioCenso', 'codigoAutorizacion']

    def create(self, validated_data):
        # No hacer nada, solo validar los datos
        return validated_data
    

class VotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voto
        fields = ['idCircunscripcion', 'idMesaElectoral', 'idProcesoElectoral', 'nombreCandidatoVotado', 'censo']