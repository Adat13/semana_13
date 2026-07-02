import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'convencion_project.settings')
django.setup()

from convencion.models import Iglesia, Participante

# Clear existing data
print("Clearing database...")
Participante.objects.all().delete()
Iglesia.objects.all().delete()

# Create Iglesias
sr = Iglesia.objects.create(nombre="Santa Rosa", distrito="Huancayo")
hs = Iglesia.objects.create(nombre="Huancayo Sur", distrito="Chilca")
et = Iglesia.objects.create(nombre="El Tambo", distrito="El Tambo")

print("Created Iglesias:")
for i in Iglesia.objects.all():
    print(f" - {i}")

# Create 12 Participantes to test page size limits (set to 5)
participantes_data = [
    ("David Angel", "Toribio Anselmo", "david@gmail.com", "987654321", sr, "activo"),
    ("Maria Elena", "Quispe Gomez", "maria@gmail.com", "912345678", sr, "activo"),
    ("Juan Carlos", "Perez Vega", "juan@gmail.com", "923456789", sr, "pendiente"),
    ("Ana Lucia", "Sosa Rojas", "ana@gmail.com", "934567890", sr, "activo"),
    ("Luis Alberto", "Flores Diaz", "luis@gmail.com", "945678901", sr, "inactivo"),
    
    ("Pedro Jose", "Castillo Ramos", "pedro@gmail.com", "956789012", hs, "activo"),
    ("Sofia Valentina", "Mendoza Soto", "sofia@gmail.com", "967890123", hs, "activo"),
    ("Carlos Andres", "Linares Ruiz", "carlos@gmail.com", "978901234", hs, "pendiente"),
    ("Gabriela Ines", "Torres Luna", "gabriela@gmail.com", "989012345", hs, "activo"),
    ("Jorge Luis", "Morales Gil", "jorge@gmail.com", "990123456", hs, "inactivo"),
    
    ("Esteban Raul", "Vargas Ortiz", "esteban@gmail.com", "901234567", et, "activo"),
    ("Lucia Belen", "Palacios Rios", "lucia@gmail.com", "911223344", et, "activo"),
]

for nombres, apellidos, email, celular, iglesia, status in participantes_data:
    Participante.objects.create(
        nombres=nombres,
        apellidos=apellidos,
        email=email,
        celular=celular,
        iglesia=iglesia,
        status=status
    )

print(f"Successfully seeded {Participante.objects.count()} participants.")
