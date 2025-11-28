from django.urls import path
from .views import (
    ArchiveMainView, ArchiveYearView, ArchiveMonthView, 
    ArchiveDayView
)

app_name = 'django_cs_archive'

urlpatterns = [
    # 1. Erroa: Urteen zerrenda (/archive/)
    path('', ArchiveMainView.as_view(), name='index'),

    # 2. Urtea: Hilabeteen zerrenda (/archive/2025/)
    path('<int:year>/', ArchiveYearView.as_view(), name='year'),
    
    # 3. Hilabetea: Artikulu zerrenda (/archive/2025/03/)
    path('<int:year>/<int:month>/', ArchiveMonthView.as_view(), name='month'),
    
    path('<int:year>/<int:month>/<int:day>/', ArchiveDayView.as_view(), name='day'),
]