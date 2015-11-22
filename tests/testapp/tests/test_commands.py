
from __future__ import absolute_import, unicode_literals

from django.contrib.sites.models import Site
from django.conf import settings
from django.core import management
from django.test import TestCase
from django_gitversions import versioner
from leonardo.models import Page


class CommandTest(TestCase):

    def setUp(self):
        '''Make DB strcture'''

        management.call_command('makemigrations',
                                interactive=False)
        management.call_command('migrate',
                                interactive=False)

    def test_settings(self):

        self.assertEqual(versioner.autosync, False)
        self.assertEqual(versioner.autocommit, False)
        self.assertEqual(versioner.autopush, False)
        self.assertEqual(str(versioner.url), str(settings.GITVERSIONS_REPO_URL))

    def test_01_gitrestore_remote(self):

        management.call_command('gitrestore')

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

        # remove local files
        #versioner.backend.destroy()

        management.call_command('gitversions',
                                format='json',
                                indent=4)

        # check local uncomited changes
        self.assertEqual(versioner.backend.check(), True)

        versioner.backend.commit('Initial Commit')

        self.assertEqual(versioner.backend.check(), False)

        # cleanup

    def test_save_another(self):
        # Regression for #17415
        # On some backends the sequence needs reset after save with explicit ID.
        # Test that there is no sequence collisions by saving another site.
        Site(domain="example2.com", name="example2.com").save()

    def tearDown(self):
        #versioner.backend.destroy()
        pass
