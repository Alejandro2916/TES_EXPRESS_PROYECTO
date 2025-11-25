from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Expreso, Estudiante, Notificacion
from django.http import JsonResponse
from django.http import JsonResponse
from expresos.gps_rutas import RUTAS




# ==========================================
#               HOME
# ==========================================
@login_required
def home(request):
    estudiante = request.user.estudiante
    expresos = Expreso.objects.all().order_by('nombre')

    # Obtener notificaciones del estudiante
    notificaciones = Notificacion.objects.filter(usuario=request.user, leida=False)

    return render(request, 'expresos/home.html', {
        'expresos': expresos,
        'estudiante': estudiante,
        'notificaciones_count': notificaciones.count(),
    })


# ==========================================
#               DETALLE EXPRESO
# ==========================================
from datetime import datetime, time, timedelta
from django.utils import timezone

@login_required
def detalle_expreso(request, expreso_id):
    expreso = get_object_or_404(Expreso, id=expreso_id)

    # === Cálculo del tiempo restante ===
    ahora = timezone.localtime().time()  # Hora actual local
    salida = expreso.hora_salida

    # Convertir a datetime real del día
    ahora_dt = datetime.combine(datetime.today(), ahora)
    salida_dt = datetime.combine(datetime.today(), salida)

    # Si la hora de salida ya pasó hoy → asumir salida mañana
    if salida_dt < ahora_dt:
        salida_dt += timedelta(days=1)

    diferencia = salida_dt - ahora_dt
    segundos_restantes = int(diferencia.total_seconds())

    return render(request, 'expresos/detalle.html', {
        'expreso': expreso,
        'segundos_restantes': segundos_restantes,
    })



# ==========================================
#           TOMAR EXPRESO  (FIX)
# ==========================================
@login_required
def tomar_expreso(request, expreso_id):
    expreso = get_object_or_404(Expreso, id=expreso_id)
    estudiante = request.user.estudiante

    if not expreso.disponible:
        messages.error(request, "Este expreso está lleno.")
        return redirect('detalle_expreso', expreso_id=expreso.id)

    if estudiante.expreso_asignado and estudiante.expreso_asignado != expreso:
        messages.error(request, "Ya estás asignado a otro expreso.")
        return redirect('detalle_expreso', expreso_id=expreso.id)

    estudiante.expreso_asignado = expreso
    estudiante.save()

    Notificacion.objects.create(
        usuario=request.user,
        mensaje=f"Te has asignado al expreso {expreso.nombre}."
    )

    messages.success(request, "Has tomado este expreso correctamente.")
    return redirect('detalle_expreso', expreso_id=expreso.id)


# ==========================================
#              DEJAR EXPRESO
# ==========================================
@login_required
def dejar_expreso(request, expreso_id):
    expreso = get_object_or_404(Expreso, id=expreso_id)
    estudiante = request.user.estudiante

    if estudiante.expreso_asignado != expreso:
        messages.error(request, "No estás asignado a este expreso.")
        return redirect('home')

    estudiante.expreso_asignado = None
    estudiante.save()

    Notificacion.objects.create(
        usuario=request.user,
        mensaje=f"Has dejado el expreso {expreso.nombre}."
    )

    messages.success(request, "Has dejado este expreso.")
    return redirect('home')



# ==========================================
#         ENVIAR SUGERENCIA
# ==========================================
@login_required
def enviar_sugerencia(request, expreso_id):
    expreso = get_object_or_404(Expreso, id=expreso_id)

    if request.method == "POST":
        texto = request.POST.get("sugerencia")

        Notificacion.objects.create(
            usuario=request.user,
            mensaje=f"Sugerencia enviada para el expreso {expreso.nombre}: {texto}"
        )

        messages.success(request, "Sugerencia enviada correctamente.")
        return redirect('detalle_expreso', expreso_id=expreso.id)

    return render(request, 'expresos/sugerencia.html', {'expreso': expreso})


# ==========================================
#        VER NOTIFICACIONES
# ==========================================
@login_required
def ver_notificaciones(request):
    notificaciones = Notificacion.objects.filter(usuario=request.user).order_by('-fecha')

    # Marcar como leídas
    Notificacion.objects.filter(usuario=request.user, leida=False).update(leida=True)

    return render(request, 'expresos/notificaciones.html', {
        'notificaciones': notificaciones
    })
    
    
# ==========================================
#             GPS SIMULADO 
# ==========================================
from django.http import JsonResponse
import json, os

@login_required
def gps_expreso(request, expreso_id):
    expreso = get_object_or_404(Expreso, id=expreso_id)
    return render(request, "expresos/gps.html", {"expreso": expreso})


# API SIMULADA PARA POSICIÓN DEL BUS
posicion_simulada = 0

@login_required
def api_posicion_expreso(request, expreso_id):
    global posicion_simulada

    # Ruta simulada (lat, lon)
    ruta = [
        (-2.14850, -79.96400),
        (-2.14870, -79.96350),
        (-2.14920, -79.96290),
        (-2.14980, -79.96220),
        (-2.15030, -79.96170),
        (-2.15090, -79.96110),
        (-2.15140, -79.96060),
        (-2.15200, -79.96010),
    ]

    # Mover al siguiente punto
    posicion_simulada = (posicion_simulada + 1) % len(ruta)

    return JsonResponse({
        "lat": ruta[posicion_simulada][0],
        "lng": ruta[posicion_simulada][1]
    })


@login_required
def gps_ruta(request, expreso_id):
    expreso = get_object_or_404(Expreso, id=expreso_id)

    ruta = expreso.destino  # ejemplo: "norte"

    if ruta in RUTAS:
        return JsonResponse({
            "ruta": RUTAS[ruta]
        })

    return JsonResponse({
        "error": "Ruta no definida"
    })
    
  
#NUEVA FUNCIÓN   
# ==========================================
#        VISTA GPS EN VIVO (SIMULADO)
# ==========================================
@login_required
def gps_en_vivo(request, expreso_id):
    expreso = get_object_or_404(Expreso, id=expreso_id)

    return render(request, 'expresos/gps.html', {
        'expreso': expreso
    })
 
 
 
 #nuevo
@login_required
def mi_panel(request):
    estudiante = request.user.estudiante
    expreso = estudiante.expreso_asignado

    # Si el estudiante NO tiene expreso
    if not expreso:
        return render(request, 'expresos/panel.html', {
            'estudiante': estudiante,
            'expreso': None,
            'segundos_restantes': 0,
        })

    # Cálculo de tiempo restante
    from datetime import datetime
    ahora = datetime.now()
    hora_salida = datetime.combine(ahora.date(), expreso.hora_salida)

    segundos_restantes = max(0, int((hora_salida - ahora).total_seconds()))

    # Notificaciones del usuario
    notificaciones = Notificacion.objects.filter(
        usuario=request.user
    ).order_by('-fecha')[:5]

    return render(request, 'expresos/panel.html', {
        'estudiante': estudiante,
        'expreso': expreso,
        'notificaciones': notificaciones,
        'segundos_restantes': segundos_restantes,
    })
    
    
    # ============================
#    MAPA GLOBAL (FASE 2)
# ============================

from django.http import JsonResponse

@login_required
def mapa_global(request):
    expresos = Expreso.objects.all()
    return render(request, 'expresos/mapa_global.html', {'expresos': expresos})


@login_required
def gps_todos(request):
    """
    Retorna la posición actual y la ruta de TODOS los buses.
    """
    from .gps_rutas import RUTAS

    data = []

    for expreso in Expreso.objects.all():

        sector = expreso.destino.lower()

        # Ruta definida en gps_rutas.py
        ruta = RUTAS.get(sector, [])

        # Indice que simula movimiento
        indice = expreso.id % len(ruta) if ruta else 0

        data.append({
            'id': expreso.id,
            'nombre': expreso.nombre,
            'sector': expreso.destino,
            'ruta': ruta,
            'posicion': ruta[indice] if ruta else None
        })

    return JsonResponse({'buses': data})





@login_required
def panel_conductor(request):
    from .models import Conductor

    try:
        conductor = Conductor.objects.get(user=request.user)
    except Conductor.DoesNotExist:
        return render(request, "expresos/no_conductor.html")

    expreso = conductor.expreso

    return render(request, "expresos/panel_conductor.html", {
        "conductor": conductor,
        "expreso": expreso,
        "ocupados": Estudiante.objects.filter(expreso_asignado=expreso).count()
    })
