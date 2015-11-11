
import errno
import os
from django.conf import settings
from django.db import router
from django_gitversions.serializers import VersionSerializer
from django_gitversions.git import git


class Versioner(object):

    @property
    def root_path(self):
        '''returns backup root path'''
        # create dir /app_label/model_name/pk.json
        return getattr(settings, 'GITVERSIONS_ROOT_PATH', '.')

    def base_model_path(self, model):
        return '/'.join([model._meta.app_label,
                         model._meta.model_name])

    def commit(self, instance, user=None):
        '''Construct commit message and commit'''
        message = 'Instance of {}({}) was changed'.format(
            instance._meta.model_name, instance.pk)
        git.commit(message, user=user)

    def handle(self, queryset, model, primary_keys=True, path=None,
               use_base_manager=True, using='default', indent=4, format='json',
               use_natural_foreign_keys=True, use_natural_primary_keys=True):
        '''Save all objects in queryset.
        '''

        # use model._meta ?
        VersionSerializerCls = getattr(
            model, 'version_manager', VersionSerializer)
        serializer = VersionSerializerCls.create_serializer(format)

        objects = queryset if isinstance(
            queryset, list) else queryset.iterator()

        for obj in objects:

            model_base_path = '/'.join([self.root_path,
                                        self.base_model_path(model)])
            mkdir_p(model_base_path)
            path = '/'.join([model_base_path,
                             '{}.{}'.format(obj.pk, format)])

            attrs = 'rw+'
            if not os.path.exists(path):
                attrs = 'arw+'
            with open(path, attrs) as file:

                serializer.serialize([obj], **{'indent': indent,
                                               'use_natural_foreign_keys': use_natural_foreign_keys,
                                               'use_natural_primary_keys': use_natural_primary_keys,
                                               'stream': file})


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
