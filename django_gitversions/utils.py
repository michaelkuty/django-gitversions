
import errno
import os
from django.conf import settings
from django.db import router


class LazyConfig(object):

    @property
    def signal_enabled(self):
        '''enable signal
        '''
        return getattr(settings, 'GITVERSIONS_SIGNAL_ENABLED', False)

    @property
    def autosync(self):
        '''dump all model changes synchronouslly ?
        '''
        return getattr(settings, 'GITVERSIONS_AUTO_SYNC', False)

    @property
    def autocommit(self):
        '''commit every single change ?
        depend on autosync
        '''
        if not self.autosync:
            return False
        return getattr(settings, 'GITVERSIONS_AUTO_COMMIT', True)

    @property
    def autopush(self):
        '''push every single commit ?
        depend on autosync
        '''
        if not self.autosync:
            return False
        return getattr(settings, 'GITVERSIONS_AUTO_PUSH', True)

    @property
    def url(self):
        '''return backup remote url'''
        if hasattr(self, '_url'):
            return self._url
        return getattr(settings,
                       'GITVERSIONS_REPO_URL',
                       'git@gitlab.com:michaelkuty/test-backup.git')

    @property
    def path(self):
        '''return backup root path'''
        if hasattr(self, '_path'):
            return self._path
        return getattr(settings,
                       'GITVERSIONS_ROOT_PATH',
                       '/srv/leonardo/sites/leonardo/backup')

    def get_ssh_cmd(self):
        '''static now'''
        ssh_cmd = getattr(settings,
                          'GITVERSIONS_GIT_SSH_COMMAND',
                          'ssh -i /root/.ssh/test')
        return ssh_cmd


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def get_queryset(model, using, primary_keys, use_base_manager):

    # get all objects
    if not model._meta.proxy and router.allow_migrate(using, model):
        if use_base_manager:
            objects = model._base_manager
        else:
            objects = model._default_manager

        queryset = objects.using(using).order_by(model._meta.pk.name)
        if primary_keys:
            queryset = queryset.filter(pk__in=primary_keys)
        return queryset

    if use_base_manager:
        objects = model._base_manager
    else:
        objects = model._default_manager

    queryset = objects.using(using).order_by(model._meta.pk.name)
    if primary_keys:
        queryset = queryset.filter(pk__in=primary_keys)
    return queryset
