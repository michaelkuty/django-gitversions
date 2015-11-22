import inspect
import os
from . import settings
from django_gitversions import versioner

ignored_apps = settings.GITVERSIONS_IGNORED_APPS
ignored_models = settings.GITVERSIONS_IGNORED_MODELS
versioned_models = settings.GITVERSIONS_VERSIONED_MODELS


def gitversion(sender, **kwargs):
    '''Simple signals which handles all changes because
    we don't care about what changed. We have Git diff.
    '''

    if versioner.signal_enabled:

        model_name = sender._meta.model_name
        app_name = sender._meta.app_label
        instance = kwargs['instance']

        if app_name not in ignored_apps and model_name not in ignored_models:
            '''LOL
            http://stackoverflow.com/a/32314405/4884542
            '''
            user = None
            for entry in reversed(inspect.stack()):
                if os.path.dirname(__file__) + '/views.py' == entry[1]:
                    try:
                        user = entry[0].f_locals['request'].user
                    except:
                        pass

            versioner.handle([instance], model=sender, user=user)
