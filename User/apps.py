from django.apps import AppConfig
from django.forms import DateField


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'User'
    
    def ready(self) -> None:
        import Payment.signals 
        return super().ready()
