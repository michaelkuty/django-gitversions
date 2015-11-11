
from __future__ import absolute_import

from git import Repo, Actor
from django.conf import settings


class GitVersioner(object):

    def __init__(self, *args, **kwargs):
        super(GitVersioner, self).__init__(*args, **kwargs)

        self.init()

    def init(self, path=None):
        return Repo.init(path or self.path)

    @property
    def repo(self):
        if not hasattr(self, '_git'):
            self._git = Repo(self.path)
        return self._git

    @property
    def path(self):
        return getattr(settings, 'GITVERSIONS_ROOT_PATH', '/srv/leonardo/sites/leonardo/backup')

    @property
    def origin(self):
        return self.repo.create_remote('origin', self.repo.remotes.origin.url)

    def check(self):
        '''git status returns true if something was changed'''

        check_add = True if len(self.repo.untracked_files) > 0 else False

        if check_add:
            return True

        return True if len(self.repo.index.diff(None)) > 0 else False

    def commit(self, message=None, user=None):
        '''Git Commit All local changes'''

        # check changes
        if not self.check():
            return False

        author = Actor("An author", "author@example.com")
        committer = Actor("A committer", "committer@example.com")
        self.repo.index.add(['.'])
        # commit by commit message and author and committer
        self.repo.index.commit(message,
                               author=author, committer=committer)

    def push(self):
        '''Push changes to remote repository'''
        self.origin.push()

    def pull(self):
        '''Push changes to remote repository'''
        self.origin.pull()

    def reset(self):
        '''Reset changes'''
        self.repo.reset()

git = GitVersioner()
