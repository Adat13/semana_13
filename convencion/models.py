from django.db import models

class Iglesia(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Iglesia")
    distrito = models.CharField(max_length=100, verbose_name="Distrito")

    def __str__(self):
        return f"{self.nombre} ({self.distrito})"


class Participante(models.Model):
    STATUS_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('pendiente', 'Pendiente'),
    ]

    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    celular = models.CharField(max_length=20, blank=True, verbose_name="Celular")
    iglesia = models.ForeignKey(Iglesia, on_delete=models.CASCADE, related_name="participantes", verbose_name="Iglesia")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='activo', verbose_name="Estado")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    def __str__(self):
        return f"{self.apellidos}, {self.nombres}"
