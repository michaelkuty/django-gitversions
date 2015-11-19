
from __future__ import absolute_import

import os

from django.utils.functional import cached_property
from git import Actor, Repo
from django_gitversions.utils import mkdir_p

from .base import Backend


class GitBackend(Backend):

    def __init__(self, path=None, url=None, *args, **kwargs):
        super(GitBackend, self).__init__(*args, **kwargs)

        # override only if is not None
        if path:
            self._path = path
        if url:
            self._url = url

        # temporary set ssh_command context
        self.get_ssh_cmd()

    def init(self, path=None):
        '''Inicialize repo object or init/clone new Git repo'''

        if os.path.isdir(self.path):
            self._repo = Repo.init(path or self.path)
        else:
            if self._url:
                # clone remote is there url
                mkdir_p(self.path)
                self._repo = Repo.clone_from(self._url,
                                             self.path,
                                             branch='master')

        return self._repo

    @property
    def repo(self):
        '''Try create instance of repo object or init new Git one'''
        if not hasattr(self, '_repo'):
            try:
                self._repo = Repo(self.path)
            except:
                self.init()
        return self._repo

    @cached_property
    def origin(self):
        if len(self.repo.remotes) > 0:
            return self.repo.remotes[0]
        return self.repo.create_remote('origin', self.url)

    def get_diff(self):
        '''return diff array'''
        return self.repo.index.diff(None)

    def get_ssh_cmd(self):
        '''override for just now and TODO use git context'''
        ssh_cmd = super(GitBackend, self).get_ssh_cmd()
        os.environ['GIT_SSH_COMMAND'] = ssh_cmd
        return ssh_cmd

    def check(self):
        '''git status returns true if something was changed'''

        check_add = True if len(self.repo.untracked_files) > 0 else False

        if check_add:
            return True

        return True if len(self.get_diff()) > 0 else False

    def commit(self, message=None, user=None, push=False, fail_silently=True):
        '''Git Commit All local changes'''

        # check changes
        if not self.check():
            return False

        author = Actor(
            "GitVersioner" if not user else str(user),
            "author@example.com" if not user else str(user.mail),
        )
        committer = author
        self.repo.git.add(all=True)
        # commit by commit message and author and committer
        self.repo.index.commit(message,
                               author=author, committer=committer)

        if push:
            self.push()

    def push(self, fail_silently=True):
        '''Push changes to remote repository'''

        # temporary call
        self.get_ssh_cmd()

        try:
            self.repo.git.push(all=True)
        except Exception as e:
            if not fail_silently:
                raise e

    def pull(self):
        '''Push changes to remote repository'''
        self.origin.pull()

    def reset(self):
        '''Reset changes'''
        self.repo.reset()

    def destroy(self, fail_silently=True):
        '''remove all'''
        import shutil
        try:
            shutil.rmtree(self.path)
        except Exception as e:
            if not fail_silently:
                raise e
