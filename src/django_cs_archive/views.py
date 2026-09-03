from django.views.generic.dates import (
    ArchiveIndexView,
    YearArchiveView,
    MonthArchiveView,
    DayArchiveView,
    DateDetailView,
    TodayArchiveView,
)
from .utils import get_archive_model, get_date_field, get_archive_filters
from django.utils import timezone
from django.core.cache import cache


class DynamicArchiveMixin:
    make_object_list = False
    allow_future = False
    month_format = "%m"

    def get_queryset(self):
        model = get_archive_model()
        filters = get_archive_filters()
        if filters:
            return model.objects.filter(**filters)
        return model.objects.all()

    def get_date_field(self):
        return get_date_field()


# 1. BISTA BERRIA: Urteak zerrendatzeko (/archive/)
class ArchiveMainView(DynamicArchiveMixin, ArchiveIndexView):
    make_object_list = False  # Txantiloian ez ditugu artikuluak zerrendatuko, urteak bakarrik, beraz False jarrita asko azkartzen da
    date_list_period = "year"  # Honek urteak aterako ditu 'date_list' aldagaian
    template_name = "django_cs_archive/archive_index.html"

    def get_date_list(self, queryset, date_type=None, ordering="ASC"):
        cache_key = f"cs_archive_years_{queryset.model._meta.label_lower}"
        date_list = cache.get(cache_key)
        if date_list is None:
            date_list = super().get_date_list(queryset, date_type, ordering)
            date_list = list(date_list)
            cache.set(cache_key, date_list, 60 * 60 * 24)  # 24 orduz gorde
        return date_list


# 2. URTE BISTA: Hilabeteak zerrendatzeko (/archive/2025/)
class ArchiveYearView(DynamicArchiveMixin, YearArchiveView):
    make_object_list = False  # Txantiloian ez ditugu artikuluak zerrendatuko, hilabeteak bakarrik, beraz False jarrita asko azkartzen da
    template_name = "django_cs_archive/archive_year.html"

    def get_date_list(self, queryset, date_type=None, ordering="ASC"):
        year = self.get_year()
        cache_key = f"cs_archive_months_{queryset.model._meta.label_lower}_{year}"
        date_list = cache.get(cache_key)
        if date_list is None:
            date_list = super().get_date_list(queryset, date_type, ordering)
            date_list = list(date_list)
            cache.set(cache_key, date_list, 60 * 60 * 12)  # 12 orduz gorde
        return date_list


# 3. HILABETE BISTA: Artikuluak zerrendatzeko (/archive/2025/03/)
class ArchiveMonthView(DynamicArchiveMixin, MonthArchiveView):
    template_name = "django_cs_archive/archive_month.html"

    def get_date_list(self, queryset, date_type=None, ordering="ASC"):
        year = self.get_year()
        month = self.get_month()
        cache_key = f"cs_archive_days_{queryset.model._meta.label_lower}_{year}_{month}"
        date_list = cache.get(cache_key)
        if date_list is None:
            date_list = super().get_date_list(queryset, date_type, ordering)
            date_list = list(date_list)
            cache.set(cache_key, date_list, 60 * 15)  # 15 minutuz gorde
        return date_list


class ArchiveDayView(DynamicArchiveMixin, DayArchiveView):
    template_name = "django_cs_archive/archive_day.html"
    make_object_list = True

    def get_date_list(self, queryset, date_type=None, ordering="ASC"):
        return []


class ArchiveTodayView(DynamicArchiveMixin, TodayArchiveView):
    template_name = "django_cs_archive/archive_today.html"
    allow_empty = True
    make_object_list = True

    def get_date_list(self, queryset, date_type=None, ordering="ASC"):
        return []


class ArchiveThisWeekView(DynamicArchiveMixin, ArchiveIndexView):
    template_name = "django_cs_archive/archive_this_week.html"
    date_list_period = "week"
    allow_empty = True
    make_object_list = True

    def get_date_list(self, queryset, date_type=None, ordering="ASC"):
        # Django-ren barne-logikak date_list hutsik badago queryset.none() bueltatzen du
        # bista honetan, beraz gaurko eguna bueltatuko dugu datu-basea ez kargatzeko.
        return [timezone.now().date()]

    def get_queryset(self):
        # Lehenik Mixin-eko queryset-a lortu
        qs = super().get_queryset()

        # Datak kalkulatu
        today = timezone.now().date()
        start_of_week = today - timezone.timedelta(days=today.weekday())
        end_of_week = start_of_week + timezone.timedelta(days=6)

        date_field = self.get_date_field()

        # Egiaztatu eremua DateTimeField edo DateField den
        field = qs.model._meta.get_field(date_field)
        from django.db.models import DateTimeField
        if isinstance(field, DateTimeField):
            filter_kwargs = {
                f"{date_field}__date__gte": start_of_week,
                f"{date_field}__date__lte": end_of_week,
            }
        else:
            filter_kwargs = {
                f"{date_field}__gte": start_of_week,
                f"{date_field}__lte": end_of_week,
            }
        return qs.filter(**filter_kwargs)


class ArchiveYesterdayView(DynamicArchiveMixin, ArchiveIndexView):
    template_name = "django_cs_archive/archive_yesterday.html"
    allow_empty = True
    make_object_list = True

    def get_date_list(self, queryset, date_type=None, ordering="ASC"):
        yesterday = timezone.now().date() - timezone.timedelta(days=1)
        return [yesterday]

    def get_queryset(self):
        qs = super().get_queryset()
        yesterday = timezone.now().date() - timezone.timedelta(days=1)
        date_field = self.get_date_field()

        # Egiaztatu eremua DateTimeField edo DateField den
        field = qs.model._meta.get_field(date_field)
        from django.db.models import DateTimeField
        if isinstance(field, DateTimeField):
            filter_kwargs = {
                f"{date_field}__date": yesterday,
            }
        else:
            filter_kwargs = {
                f"{date_field}": yesterday,
            }
        return qs.filter(**filter_kwargs)


class ArchiveLastWeekView(DynamicArchiveMixin, ArchiveIndexView):
    template_name = "django_cs_archive/archive_last_week.html"
    allow_empty = True
    make_object_list = True

    def get_date_list(self, queryset, date_type=None, ordering="ASC"):
        today = timezone.now().date()
        start_of_this_week = today - timezone.timedelta(days=today.weekday())
        start_of_last_week = start_of_this_week - timezone.timedelta(days=7)
        return [start_of_last_week]

    def get_queryset(self):
        qs = super().get_queryset()
        today = timezone.now().date()
        start_of_this_week = today - timezone.timedelta(days=today.weekday())
        start_of_last_week = start_of_this_week - timezone.timedelta(days=7)
        end_of_last_week = start_of_last_week + timezone.timedelta(days=6)

        date_field = self.get_date_field()

        # Egiaztatu eremua DateTimeField edo DateField den
        field = qs.model._meta.get_field(date_field)
        from django.db.models import DateTimeField
        if isinstance(field, DateTimeField):
            filter_kwargs = {
                f"{date_field}__date__gte": start_of_last_week,
                f"{date_field}__date__lte": end_of_last_week,
            }
        else:
            filter_kwargs = {
                f"{date_field}__gte": start_of_last_week,
                f"{date_field}__lte": end_of_last_week,
            }
        return qs.filter(**filter_kwargs)
