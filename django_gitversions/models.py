from django.db.models.signals import post_save
from django_gitversions import versioner

ignored_senders = ['constance']
versioned_models = ['Page']


def gitversion(sender, **kwargs):

    model_name = sender._meta.model_name
    if model_name not in ignored_senders and model_name in versioned_models:
        versioner.handle([kwargs['instance']])

    versioner.handle(
        queryset=[kwargs['instance']],
        model=sender)


post_save.connect(gitversion)
