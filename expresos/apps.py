from django.apps import AppConfig

class ExpresosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'expresos'

    def ready(self):
        import expresos.signals
