from rest_framework import serializers
from .models import Iglesia, Participante

class IglesiaSerializer(serializers.ModelSerializer):
    # SerializerMethodField to compute the number of participants registered
    participantes_count = serializers.SerializerMethodField()

    class Meta:
        model = Iglesia
        fields = ['id', 'nombre', 'distrito', 'participantes_count']

    def get_participantes_count(self, obj):
        return obj.participantes.count()


class ParticipanteSerializer(serializers.HyperlinkedModelSerializer):
    # Read-only field
    created = serializers.ReadOnlyField()

    # SerializerMethodField to return a calculated full name
    nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = Participante
        fields = [
            'url',
            'id',
            'nombres',
            'apellidos',
            'nombre_completo',
            'email',
            'celular',
            'iglesia',
            'status',
            'created'
        ]

    def get_nombre_completo(self, obj):
        return f"{obj.nombres} {obj.apellidos}"

    def validate_nombres(self, value):
        if not value.strip():
            raise serializers.ValidationError("Los nombres no pueden estar vacíos.")
        return value

    def validate_apellidos(self, value):
        if not value.strip():
            raise serializers.ValidationError("Los apellidos no pueden estar vacíos.")
        return value

    # Nested / Cross-field validation
    def validate(self, data):
        nombres = data.get('nombres', '')
        apellidos = data.get('apellidos', '')

        # Validating that names do not contain numeric characters
        if any(char.isdigit() for char in nombres):
            raise serializers.ValidationError({"nombres": "Los nombres no pueden contener caracteres numéricos."})
        if any(char.isdigit() for char in apellidos):
            raise serializers.ValidationError({"apellidos": "Los apellidos no pueden contener caracteres numéricos."})

        return data
