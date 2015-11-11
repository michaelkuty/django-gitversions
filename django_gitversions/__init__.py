
from django.apps import AppConfig
from .base import Versioner


default_app_config = 'django_gitversions.Config'


LEONARDO_APPS = ['django_gitversions']

LEONARDO_CONFIG = {
    'GITVERSIONS_ROOT_PATH': ('/srv/leonardo/sites/leonardo/backup', 'Git versions Root path')
}


class Config(AppConfig):
    name = 'django_gitversions'
    verbose_name = "django-gitversions"

versioner = Versioner()
