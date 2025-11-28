# src/nyt_archive/urls.py
from django.urls import path
from .views import (
    ArchiveYearView, ArchiveMonthView, ArchiveDayView, ArchiveDetailView
)

app_name = 'nyt_archive'  # Namespace garrantzitsua da

urlpatterns = [
    path('<int:year>/', ArchiveYearView.as_view(), name='year'),
    path('<int:year>/<int:month>/', ArchiveMonthView.as_view(), name='month'),
    path('<int:year>/<int:month>/<int:day>/', ArchiveDayView.as_view(), name='day'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', ArchiveDetailView.as_view(), name='detail'),
]