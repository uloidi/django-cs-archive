from django.urls import path
from .views import (
    ArchiveMainView, ArchiveYearView, ArchiveMonthView, 
    ArchiveDayView, ArchiveTodayView, ArchiveThisWeekView,
    ArchiveYesterdayView, ArchiveLastWeekView
)

app_name = 'django_cs_archive'

urlpatterns = [
    # 1. Erroa: Urteen zerrenda (/archive/)
    path('', ArchiveMainView.as_view(), name='index'),
    
    path('today/', ArchiveTodayView.as_view(), name='today'),
    
    path('yesterday/', ArchiveYesterdayView.as_view(), name='yesterday'),
    
    path('this-week/', ArchiveThisWeekView.as_view(), name='this_week'),
    
    path('last-week/', ArchiveLastWeekView.as_view(), name='last_week'),

    # 2. Urtea: Hilabeteen zerrenda (/archive/2025/)
    path('<int:year>/', ArchiveYearView.as_view(), name='year'),
    
    # 3. Hilabetea: Artikulu zerrenda (/archive/2025/03/)
    path('<int:year>/<int:month>/', ArchiveMonthView.as_view(), name='month'),
    
    path('<int:year>/<int:month>/<int:day>/', ArchiveDayView.as_view(), name='day'),


]