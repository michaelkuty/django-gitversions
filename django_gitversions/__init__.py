
from django.apps import AppConfig
from .base import Versioner


default_app_config = 'django_gitversions.Config'


LEONARDO_APPS = ['django_gitversions']

LEONARDO_OPTGROUP = 'Git Versions'

LEONARDO_CONFIG = {
    'GITVERSIONS_ROOT_PATH': ('/srv/leonardo/sites/leonardo/backup',
                              'Git versions Root path'),
    'GITVERSIONS_AUTO_SYNC': (True,
                              'Commit & Push all changes synchronously.'),
    'GITVERSIONS_REPO_URL': ('git@gitlab.com:michaelkuty/test-backup.git',
                             'Backup remote url.'),
}


class Config(AppConfig):
    name = 'django_gitversions'
    verbose_name = "django-gitversions"

versioner = Versioner()
