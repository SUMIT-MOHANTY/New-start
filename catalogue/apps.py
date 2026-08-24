from django.apps import AppConfig
from pathlib import Path


class CatalogueConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalogue'

    def ready(self):
        """Create media directories on startup so file uploads work on Railway."""
        from django.conf import settings
        for subdir in ('site', 'products', 'testimonials'):
            dir_path = Path(settings.MEDIA_ROOT) / subdir
            dir_path.mkdir(parents=True, exist_ok=True)
