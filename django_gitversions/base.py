
import os
import glob
from django.conf import settings
from django_gitversions.serializers import VersionSerializer
from .utils import LazyConfig, mkdir_p


class Versioner(LazyConfig):

    '''Simple object which has responsibility for loading and dumping all data

    this class is merged with Django Serializer class and then is used
    for serializing and deserialize data in json,yaml and xml formats.

    in the constructctor is inicialized SCM backend which is available under
    backend property. This backend must implement basic SCM commands such as
    commit, push, ..

    '''

    def __init__(self, path=None, url=None, *args, **kwargs):
        '''The constructctor accepts two core attributes
        path to backup directory which must be writable and
        url of remote origin which is now expexted in ssh format
        '''
        super(Versioner, self).__init__(*args, **kwargs)

        # override only if is not None
        if path:
            self._path = path
        if url:
            self._url = url

    @property
    def backend(self):
        '''return SCM backend git,svn, ..'''
        if not hasattr(self, '_backend'):
            from django_gitversions.backends.git import GitBackend
            self._backend = GitBackend(self.path, self.url)
        return self._backend

    def base_model_path(self, model):
        '''model path in app_label/model_name format'''
        return '/'.join([model._meta.app_label,
                         model._meta.model_name])

    def handle(self, queryset, model, primary_keys=True, path=None, autocommit=None,
               use_base_manager=True, using='default', indent=4, format='json',
               use_natural_foreign_keys=True, use_natural_primary_keys=True, user=None):
        '''Save all objects in queryset to filesystem and auto commit & push.
        '''

        # use model._meta ?
        VersionSerializerCls = getattr(
            model, 'version_manager', VersionSerializer)
        serializer = VersionSerializerCls.create_serializer(format)

        objects = queryset if isinstance(
            queryset, list) else queryset.iterator()

        for obj in objects:

            model_base_path = '/'.join([self.path,
                                        self.base_model_path(model)])
            mkdir_p(model_base_path)
            path = '/'.join([model_base_path,
                             '{}.{}'.format(obj.pk, format)])

            attrs = 'w'
            if not os.path.exists(path):
                attrs = 'arw+'

            with open(path, attrs) as file:

                serializer.serialize([obj], **{'indent': indent,
                                               'use_natural_foreign_keys': use_natural_foreign_keys,
                                               'use_natural_primary_keys': use_natural_primary_keys,
                                               'stream': file})

            if (autocommit is not None and autocommit) or (self.autocommit and autocommit is None):
                msg = 'Instance {}({}) was changed. \n For Humans: Object {} was changed.'.format(
                    obj._meta.model_name, obj.pk, obj)
                try:
                    self.backend.commit(msg,
                                        push=self.autopush,
                                        user=user)
                except Exception as e:
                    raise e

    def get_all_fixtures(self):
        '''returns all paths
        TODO: properly join paths for globing
        '''
        fixtures = []

        for app_path in glob.glob(self.path + "/*"):
            for model_path in glob.glob(app_path + '/*'):
                for instance_path in glob.glob(model_path + '/*.json'):
                    fixtures.append(instance_path)
        return fixtures
