from django.db import models
from django.contrib.auth.models import User


# Estados del bus
ESTADOS = [
    ('verde', 'Disponible (Vacío)'),
    ('amarillo', 'Medio'),
    ('rojo', 'Lleno'),
]

DESTINOS = [
    ('norte', 'Norte'),
    ('sur', 'Sur'),
    ('este', 'Este'),
    ('oeste', 'Oeste'),
]


class Expreso(models.Model):
    nombre = models.CharField(max_length=50)
    capacidad = models.IntegerField(default=18)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='verde')
    destino = models.CharField(max_length=10, choices=DESTINOS)
    hora_salida = models.TimeField()

    def __str__(self):
        return self.nombre

    # --- FUNCIONES AUTOMÁTICAS ---
    @property
    def ocupados(self):
        return Estudiante.objects.filter(expreso_asignado=self).count()

    @property
    def disponible(self):
        return self.ocupados < self.capacidad

    def actualizar_estado(self):
        if self.capacidad == 0:
            self.estado = "rojo"
            self.save()
            return

        porcentaje = (self.ocupados / self.capacidad) * 100

        if porcentaje <= 30:
            self.estado = "verde"
        elif porcentaje <= 60:
            self.estado = "amarillo"
        else:
            self.estado = "rojo"

        self.save()


class Estudiante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    expreso_asignado = models.ForeignKey(
        Expreso, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.username


class Sugerencia(models.Model):
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sugerencia de {self.estudiante.username}"


class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)

    def __str__(self):
        return f"Notificación para {self.usuario.username}"
    
    
    from django.contrib.auth.models import User

class Conductor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    expreso = models.ForeignKey(Expreso, on_delete=models.CASCADE)
    activo = models.BooleanField(default=False)

    def __str__(self):
        return f"Conductor: {self.user.username}"
