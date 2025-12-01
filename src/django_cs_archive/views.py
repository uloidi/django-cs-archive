from django.views.generic.dates import (
    ArchiveIndexView, YearArchiveView, MonthArchiveView, 
    DayArchiveView, DateDetailView
)
from .utils import get_archive_model, get_date_field
from django.utils import timezone
class DynamicArchiveMixin:
    make_object_list = True
    allow_future = False
    month_format = '%m'

    def get_queryset(self):
        model = get_archive_model()
        return model.objects.all()

    def get_date_field(self):
        return get_date_field()

# 1. BISTA BERRIA: Urteak zerrendatzeko (/archive/)
class ArchiveMainView(DynamicArchiveMixin, ArchiveIndexView):
    date_list_period = 'year'  # Honek urteak aterako ditu 'date_list' aldagaian
    template_name = "django_cs_archive/archive_index.html"

# 2. URTE BISTA: Hilabeteak zerrendatzeko (/archive/2025/)
class ArchiveYearView(DynamicArchiveMixin, YearArchiveView):
    make_object_list = True # Artikuluak ere eskuragarri egongo dira, baina txantiloian hilabeteak erakutsiko ditugu
    template_name = "django_cs_archive/archive_year.html"

# 3. HILABETE BISTA: Artikuluak zerrendatzeko (/archive/2025/03/)
class ArchiveMonthView(DynamicArchiveMixin, MonthArchiveView):
    template_name = "django_cs_archive/archive_month.html"

class ArchiveDayView(DynamicArchiveMixin, DayArchiveView):
    template_name = "django_cs_archive/archive_day.html"

class ArchiveTodayView(DynamicArchiveMixin, DayArchiveView):
    template_name = "django_cs_archive/archive_day.html"

    def get_dated_items(self):
        # Gaurko datako artikuluak soilik itzuli
        today = timezone.now().date()
        date_field = self.get_date_field()
        filter_kwargs = {
            f"{date_field}__year": today.year,
            f"{date_field}__month": today.month,
            f"{date_field}__day": today.day,
        }
        return self.get_queryset().filter(**filter_kwargs)
class ArchiveThisWeekView(DynamicArchiveMixin, ArchiveIndexView):
    template_name = "django_cs_archive/archive_this_week.html"

    def get_dated_items(self):
        # Aste honetako artikuluak soilik itzuli
        today = timezone.now().date()
        start_of_week = today - timezone.timedelta(days=today.weekday())
        end_of_week = start_of_week + timezone.timedelta(days=6)
        date_field = self.get_date_field()
        filter_kwargs = {
            f"{date_field}__date__gte": start_of_week,
            f"{date_field}__date__lte": end_of_week,
        }
        return self.get_queryset().filter(**filter_kwargs)