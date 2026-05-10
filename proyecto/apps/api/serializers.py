from rest_framework import serializers

class InfoSistemaSerializer(serializers.Serializer):
    mensaje = serializers.CharField()
    version = serializers.CharField()
    ambiente = serializers.CharField()
    estado = serializers.CharField()