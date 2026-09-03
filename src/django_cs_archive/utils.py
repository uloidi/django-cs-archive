import json
from django.conf import settings
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _

def get_archive_model():
    # Ezarpena: CS_ARCHIVE_MODEL
    model_string = getattr(settings, 'CS_ARCHIVE_MODEL', None)
    if not model_string:
        raise ImproperlyConfigured(_("CS_ARCHIVE_MODEL must be set in settings.py."))
    try:
        return apps.get_model(model_string, require_ready=False)
    except LookupError:
        raise ImproperlyConfigured(_("Could not find model: {model_string}").format(model_string=model_string))

def get_date_field():
    # Ezarpena: CS_ARCHIVE_DATE_FIELD (Defektuz: 'publish_date')
    return getattr(settings, 'CS_ARCHIVE_DATE_FIELD', 'publish_date')

def get_archive_filters():
    # Ezarpena: CS_ARCHIVE_FILTERS (Defektuz: {})
    filters = getattr(settings, 'CS_ARCHIVE_FILTERS', None)
    if filters is None:
        return {}
    if isinstance(filters, str):
        try:
            filters = json.loads(filters)
        except json.JSONDecodeError:
            raise ImproperlyConfigured(_("CS_ARCHIVE_FILTERS contains an invalid JSON string."))
    if isinstance(filters, dict):
        return filters
    raise ImproperlyConfigured(_("CS_ARCHIVE_FILTERS must be a dictionary or a valid JSON string."))