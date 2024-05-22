from django.apps import AppConfig


class ResourceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'resource'

    def ready(self):
        from resource import signals