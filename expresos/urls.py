from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('expreso/<int:expreso_id>/', views.detalle_expreso, name='detalle_expreso'),
    path('expreso/<int:expreso_id>/tomar/', views.tomar_expreso, name='tomar_expreso'),
    path('expreso/<int:expreso_id>/dejar/', views.dejar_expreso, name='dejar_expreso'),
    path('expreso/<int:expreso_id>/sugerencia/', views.enviar_sugerencia, name='enviar_sugerencia'),
    
    path('expreso/<int:expreso_id>/gps/', views.gps_expreso, name='gps_expreso'),
    path('api/expreso/<int:expreso_id>/posicion/', views.api_posicion_expreso, name='api_posicion_expreso'),

    path("expreso/<int:expreso_id>/gps/", views.gps_ruta, name="gps_ruta"),

    path('gps/<int:expreso_id>/', views.gps_en_vivo, name='gps_en_vivo'),

    path('mi_panel/', views.mi_panel, name='mi_panel'),
    
    # 🔔 NOTIFICACIONES (NUEVA RUTA)
    path('notificaciones/', views.ver_notificaciones, name='ver_notificaciones'), 
    
    
    path('mapa-global/', views.mapa_global, name='mapa_global'),
    path('gps-todos/', views.gps_todos, name='gps_todos'),

    path("conductor/", views.panel_conductor, name="panel_conductor"),

]
