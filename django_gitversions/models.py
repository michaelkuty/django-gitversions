from django.db.models.signals import post_save
from .signals import gitversion


post_save.connect(gitversion)
