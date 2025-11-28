# Zure paketean (adibidez models.py)
from django.urls import reverse
from .utils import get_date_field

class ArchiveUrlMixin:
    def get_absolute_url(self):
        date_field_name = get_date_field()
        date_val = getattr(self, date_field_name)
        
        return reverse('archive:detail', kwargs={
            'year': date_val.year,
            'month': date_val.strftime('%m'),
            'day': date_val.strftime('%d'),
            'slug': self.slug  # Suposatzen da ereduak 'slug' daukala
        })