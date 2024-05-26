from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class ResourceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'resource'
    verbose_name = _("Resurslar")

    def ready(self)->None:
        from resource import signals