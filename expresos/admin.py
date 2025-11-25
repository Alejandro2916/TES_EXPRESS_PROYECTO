from django.contrib import admin
from .models import Expreso, Sugerencia

@admin.register(Expreso)
class ExpresoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'capacidad', 'destino', 'estado', 'hora_salida')
    list_filter = ('destino', 'estado')


@admin.register(Sugerencia)
class SugerenciaAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'mensaje', 'fecha')
    list_filter = ('fecha',)
    
    from .models import Conductor
    admin.site.register(Conductor)
