
from django_gitversions.utils import LazyConfig


class Backend(LazyConfig):

    def init(self, path=None, url=None):
        '''Inicialize repo object or init new Git repo'''
        raise NotImplementedError

    @property
    def repo(self):
        '''Try create instance of repo object or init new Git one'''
        raise NotImplementedError

    def commit(self, message=None, user=None, push=False, fail_silently=True):
        '''Commit All local changes'''
        raise NotImplementedError

    def push(self, fail_silently=True):
        '''Push changes to remote repository'''
        raise NotImplementedError

    def pull(self):
        '''Push changes to remote repository'''
        raise NotImplementedError

    def reset(self):
        '''Reset changes'''
        raise NotImplementedError
