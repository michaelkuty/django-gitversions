from __future__ import absolute_import

from celery import shared_task
from django_gitversions import versioner
from django.core import management


@shared_task
def commit():
    '''Commit changes.'''
    versioner.backend.commit()
    return {'result': 'Database changes was commited to backup service.'}


@shared_task
def push():
    '''Push data to remote repository.'''
    versioner.backend.push(force=True)
    return {'result': 'Database changes was pushed to backup service.'}


@shared_task
def dumpall():
    '''Dump all data.'''
    management.call_command('gitvesions',
                            format='json',
                            indent=4)
    return {'result': 'Database changes was pushed to backup service.'}
