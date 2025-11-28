# src/nyt_archive/views.py
from django.views.generic.dates import (
    YearArchiveView, MonthArchiveView, DayArchiveView, DateDetailView
)
from .utils import get_archive_model, get_date_field

class DynamicArchiveMixin:
    """
    Mixin honek kudeatzen du konfigurazio dinamikoa settings-etik.
    """
    make_object_list = True
    allow_future = False
    month_format = '%m'

    def get_queryset(self):
        model = get_archive_model()
        return model.objects.all()

    def get_date_field(self):
        return get_date_field()

class ArchiveYearView(DynamicArchiveMixin, YearArchiveView):
    pass

class ArchiveMonthView(DynamicArchiveMixin, MonthArchiveView):
    pass

class ArchiveDayView(DynamicArchiveMixin, DayArchiveView):
    pass
