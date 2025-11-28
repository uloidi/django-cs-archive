from django.conf import settings
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured

def get_archive_model():
    # Ezarpena: CS_ARCHIVE_MODEL
    model_string = getattr(settings, 'CS_ARCHIVE_MODEL', None)
    if not model_string:
        raise ImproperlyConfigured("CS_ARCHIVE_MODEL ezarri behar da settings.py fitxategian.")
    try:
        return apps.get_model(model_string, require_ready=False)
    except LookupError:
        raise ImproperlyConfigured(f"Ezin da aurkitu eredua: {model_string}")

def get_date_field():
    # Ezarpena: CS_ARCHIVE_DATE_FIELD (Defektuz: 'publish_date')
    return getattr(settings, 'CS_ARCHIVE_DATE_FIELD', 'publish_date')