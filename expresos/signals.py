from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Estudiante

@receiver(post_save, sender=User)
def crear_estudiante(sender, instance, created, **kwargs):
    if created:
        Estudiante.objects.create(user=instance)

@receiver(post_save, sender=User)
def guardar_estudiante(sender, instance, **kwargs):
    instance.estudiante.save()
