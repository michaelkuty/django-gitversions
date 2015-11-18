
from __future__ import absolute_import, unicode_literals

from django.core import management
from django.test import TestCase
from leonardo.models import Page
from django_gitversions import versioner


class CommandTest(TestCase):

    def setUp(self):
        '''Make DB strcture'''
        management.call_command('makemigrations',
                                interactive=False)
        management.call_command('migrate',
                                interactive=False)

    def test_01_gitrestore_remote(self):
        management.call_command('gitrestore',
                                url='https://gitlab.com/michaelkuty/test-backup.git')

        self.assertEqual(Page.objects.exists(), True)

    def test_02_gitversions(self):

        management.call_command('gitversions',
                                format='json',
                                indent=4)

        # check local uncomited changes
        self.assertEqual(versioner.backend.check(), True)

    def test_03_gitrestore_local(self):

        # flush restored data
        management.call_command('flush',
                                interactive=False)

        # assert empty db
        self.assertEqual(Page.objects.exists(), False)

        # restore from local
        management.call_command('gitrestore')

        self.assertEqual(Page.objects.exists(), True)

    def test_04_versioner(self):

        self.assertEqual(versioner.backend.check(), True)

        versioner.backend.commit('Initial Commit')

        self.assertEqual(versioner.backend.check(), False)
