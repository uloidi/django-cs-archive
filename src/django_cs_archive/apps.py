from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class CsArchiveConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_cs_archive'
    verbose_name = _("CS Archive")