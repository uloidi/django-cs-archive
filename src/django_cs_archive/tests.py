import datetime
from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse, path, include
from django.db import models
from django.core.cache import cache
from django_cs_archive.models import ArchiveUrlMixin

class TestArticle(ArchiveUrlMixin, models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    pub_date = models.DateField()

    class Meta:
        app_label = 'django_cs_archive'

    def __str__(self):
        return self.title

# Mock URLconf for testing
archive_patterns = ([
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', lambda r, *a, **k: None, name='detail'),
], 'archive')

urlpatterns = [
    path('archive/', include('django_cs_archive.urls', namespace='django_cs_archive')),
    path('archive/', include(archive_patterns)),
]

class ArchiveViewsTestCase(TestCase):
    def setUp(self):
        # Clear cache before each test
        cache.clear()
        
        # Create some test articles
        self.now = timezone.now().date()
        self.today_article = TestArticle.objects.create(
            title="Gaurko Artikulu",
            slug="gaurko-artikulu",
            pub_date=self.now
        )
        
        self.yesterday = self.now - datetime.timedelta(days=1)
        self.yesterday_article = TestArticle.objects.create(
            title="Atzoko Artikulu",
            slug="atzoko-artikulu",
            pub_date=self.yesterday
        )
        
        # 10 days ago (belongs to previous weeks/months)
        self.old_date = self.now - datetime.timedelta(days=10)
        self.old_article = TestArticle.objects.create(
            title="Duela Gutxiko Artikulu",
            slug="duela-gutxiko-artikulu",
            pub_date=self.old_date
        )

        self.client = Client()

    def test_archive_index_view(self):
        url = reverse('django_cs_archive:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Check that date_list contains years
        date_list = response.context['date_list']
        years = [d.year for d in date_list]
        self.assertIn(self.now.year, years)
        
        # Check caching
        cache_key = f"cs_archive_years_django_cs_archive.testarticle"
        self.assertIsNotNone(cache.get(cache_key))

    def test_archive_year_view(self):
        url = reverse('django_cs_archive:year', kwargs={'year': self.now.year})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Check months
        date_list = response.context['date_list']
        months = [d.month for d in date_list]
        self.assertIn(self.now.month, months)
        
        cache_key = f"cs_archive_months_django_cs_archive.testarticle_{self.now.year}"
        self.assertIsNotNone(cache.get(cache_key))

    def test_archive_month_view(self):
        url = reverse('django_cs_archive:month', kwargs={'year': self.now.year, 'month': self.now.month})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Check days
        date_list = response.context['date_list']
        days = [d.day for d in date_list]
        self.assertIn(self.now.day, days)
        
        cache_key = f"cs_archive_days_django_cs_archive.testarticle_{self.now.year}_{self.now.month}"
        self.assertIsNotNone(cache.get(cache_key))

    def test_archive_day_view(self):
        url = reverse('django_cs_archive:day', kwargs={
            'year': self.now.year, 
            'month': self.now.month,
            'day': self.now.day
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.today_article, response.context['object_list'])

    def test_archive_today_view(self):
        url = reverse('django_cs_archive:today')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.today_article, response.context['object_list'])

    def test_archive_yesterday_view(self):
        url = reverse('django_cs_archive:yesterday')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.yesterday_article, response.context['object_list'])

    def test_archive_this_week_view(self):
        url = reverse('django_cs_archive:this_week')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Should contain today's and yesterday's articles if they are within this week
        # But we definitely know today_article is in this week
        self.assertIn(self.today_article, response.context['object_list'])

    def test_archive_last_week_view(self):
        url = reverse('django_cs_archive:last_week')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_archive_url_mixin(self):
        expected_url = f"/archive/{self.now.year}/{self.now.strftime('%m')}/{self.now.strftime('%d')}/gaurko-artikulu/"
        self.assertEqual(self.today_article.get_absolute_url(), expected_url)
