from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny

from .models import Iglesia, Participante
from .serializers import IglesiaSerializer, ParticipanteSerializer

class IglesiaViewSet(viewsets.ModelViewSet):
    queryset = Iglesia.objects.all()
    serializer_class = IglesiaSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['distrito']
    search_fields = ['nombre']
    ordering_fields = ['nombre']
    ordering = ['nombre']

    # Custom endpoint: GET /api/iglesias/{id}/participantes/
    @action(detail=True, methods=['get'], url_path='participantes')
    def participantes(self, request, pk=None):
        iglesia = self.get_object()
        participantes = iglesia.participantes.all()
        # Pass request context for HyperlinkedModelSerializer
        serializer = ParticipanteSerializer(participantes, many=True, context={'request': request})
        return Response(serializer.data)


class ParticipanteViewSet(viewsets.ModelViewSet):
    queryset = Participante.objects.all()
    serializer_class = ParticipanteSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'iglesia']
    search_fields = ['nombres', 'apellidos', 'email']
    ordering_fields = ['created', 'apellidos']
    ordering = ['-created']

    # Custom endpoint: POST /api/participantes/{id}/cambiar-estado/
    @action(detail=True, methods=['post'], url_path='cambiar-estado')
    def cambiar_estado(self, request, pk=None):
        participante = self.get_object()
        nuevo_estado = request.data.get('status')
        if nuevo_estado not in dict(Participante.STATUS_CHOICES):
            return Response(
                {"error": f"Estado '{nuevo_estado}' no es válido. Opciones: {[c[0] for c in Participante.STATUS_CHOICES]}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        participante.status = nuevo_estado
        participante.save()
        serializer = self.get_serializer(participante)
        return Response(serializer.data)

    # Custom endpoint: GET /api/participantes/resumen/
    @action(detail=False, methods=['get'], url_path='resumen')
    def resumen(self, request):
        total = Participante.objects.count()
        activos = Participante.objects.filter(status='activo').count()
        inactivos = Participante.objects.filter(status='inactivo').count()
        pendientes = Participante.objects.filter(status='pendiente').count()
        return Response({
            "total_inscritos": total,
            "activos": activos,
            "inactivos": inactivos,
            "pendientes": pendientes
        })
