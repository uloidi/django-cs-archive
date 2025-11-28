# django-cs-archive

A New York Times-style date-based archiving system (YYYY/MM/DD) for Django applications.

This package wraps Django's powerful generic date views into a plug-and-play solution. It follows the "Convention over Configuration" philosophy: just add a few lines to your `settings.py`, and you're ready to go.

## Features

* 📅 **Full Hierarchy:** Year, Month, Day, and Detail (Slug) views.
* ⚙️ **Centralized Configuration:** Managed via `settings.py`, similar to `AUTH_USER_MODEL`.
* 🔌 **Plug-and-play:** No need to write complex views or URL patterns manually.
* 🐍 **Compatibility:** Supports Django 3.2+.

## Installation

Install via pip:

```bash
pip install django-cs-archive
```

## Configuration

This is the most important part. Follow these three simple steps:

### 1. `settings.py`

Add the app to your installed apps and define which model you want to archive.

```python
INSTALLED_APPS = [
    # ... other apps
    'django_cs_archive',
]

# REQUIRED: The model to be managed by the archive
# Format: 'app_label.ModelName'
CS_ARCHIVE_MODEL = 'blog.Article' 

# OPTIONAL: The name of the date/datetime field in your model
# Defaults to 'publish_date' if not set.
CS_ARCHIVE_DATE_FIELD = 'pub_date'
```

### 2. `urls.py`

Include the archive URLs in your project's main URL configuration. You can choose any prefix you like (e.g., `news/`, `archive/`, `blog/`).

```python
from django.urls import path, include

urlpatterns = [
    # ...
    path('news/', include('django_cs_archive.urls')),
]
```

### 3. Prepare your Model (`models.py`)

Your model (defined in `CS_ARCHIVE_MODEL`) must satisfy at least two requirements:
1.  Have a **Date** or **DateTime** field (matching the name in settings).
2.  Have a **Slug** field (named `slug`) to generate unique URLs.

It is highly recommended to add the `get_absolute_url` method to easily generate links in your templates:

```python
from django.db import models
from django.urls import reverse

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique_for_date='pub_date') # Important for data integrity
    pub_date = models.DateTimeField()
    content = models.TextField()

    def get_absolute_url(self):
        # Generate the URL using django-cs-archive namespace
        return reverse('django_cs_archive:detail', kwargs={
            'year': self.pub_date.year,
            'month': self.pub_date.strftime('%m'),
            'day': self.pub_date.strftime('%d'),
            'slug': self.slug,
        })
```

## Usage

Once configured, the following URLs will be automatically available (assuming you used the `news/` prefix):

* `/news/2024/` -> All articles from 2024.
* `/news/2024/03/` -> All articles from March 2024.
* `/news/2024/03/15/` -> All articles from that specific day.
* `/news/2024/03/15/my-article-slug/` -> The full article detail view.

### In Templates

Use the `django_cs_archive` namespace to generate links:

```html
<!-- Link to a specific article -->
<a href="{{ article.get_absolute_url }}">Read more</a>

<!-- Link to the yearly archive -->
<a href="{% url 'django_cs_archive:year' year=2024 %}">2024 Archive</a>
```

## Customization (Templates)

The package looks for standard Django templates. To customize the look and feel, create the following files in your project's templates directory:

* `templates/django_cs_archive/archive_year.html`
* `templates/django_cs_archive/archive_month.html`
* `templates/django_cs_archive/archive_day.html`
* `templates/django_cs_archive/archive_detail.html`

---

### License

MIT License.