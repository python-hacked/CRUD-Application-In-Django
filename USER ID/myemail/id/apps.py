from django.apps import AppConfig


class IdConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'id'



class UsersConfig(AppConfig):
    name = 'users'
 
    def ready(self):
        import users.signals    
