
==================
django-gitversions
==================

Manage DB changes by Git.

The basic idea is very simple, dump every model change to filesystem and then version it using SCM(Git for now). After ,,Initial Commit" you can revert every change ever made, just by typing ,,git revert". You can also make some interesting operations knowing from standard Git such as merge for new

**Still under heavy development and testing, also may break your production data!**

.. contents::
    :local:

Features
--------

* dump all database data to easy diffable format
* restore data from remote url or local backup
* make git commit for every model change and push it to remote repository
* make model versions periodically and asynchronous using Celery
* supports more SCM backends (Git, SVN) and more Git providers(Github, Gitlab, Bitbucket)

Why ?
-----

Fixtres are good for some use cases such as restoring new site, backuping some constants, testing or somethink else. These fixtures lives in the repository and it's versioned by some SCM. But dumping/restoring all database data with constrains is impossible. Sometime would be nice to have system which can dump whole database into human readable and easy diffable format and then transform, transport and restore it on another place into another Django site. Yes much easier and reliable is native database backup & restore, but this is not good for some cases. Sometimes you have different db model, but you would like to have ability to restore some tables as a wave of his magic wand.

Example
-------

.. code-block:: bash

    python manage.py gitversions --indent=4 --format=json --exclude=elephantblog

    Dumped 45 applications, 117 models and 2459 instances.

    python manage.py gitrestore --url=git@gitlab.com:michaelkuty/test-backup.git

    Clonning initial data from git@gitlab.com:michaelkuty/test-backup.git
    Loaded 2498 instances and 0 was skipped from total 2498 in 12 loaddata iterations and 25 saving iterations.

Requires
--------

* Django 1.8 +
* PythonGit

Installation
------------

.. code-block:: bash

    pip install django-gitversions

Configuration
-------------

Configuration is quite simple.

.. code-block:: bash

    GITVERSIONS_ROOT_PATH = '/absolute/path/to/your/backup'
    GITVERSIONS_REPO_URL = 'git@gitlab.com:michaelkuty/backup-test.git'

On ``GITVERSIONS_REPO_URL`` depends why git will interact with remote. We recommend using SSH which needs to have configured SSH key on you remote repository. Set your ``GITVERSIONS_GIT_SSH_COMMAND``.

.. code-block:: bash

    GITVERSIONS_GIT_SSH_COMMAND = 'ssh -i /root/.ssh/test'

Then ensure that you have uploaded your public key to remote repository.

In default state ``django-gitversions`` marks all changes and push it synchronouslly, but this behavior makes django slower and it's not recommended for production use, because making versions generates a lot of I/O operations.

.. code-block:: bash

    GITVERSIONS_AUTO_SYNC = False

Using
-----

Using django-gitversion is really simple because there is no magic.

like in any other versioning program you must start with creating initial version, in django-versions is this achieved through running gitversions command which is derived from standard Django ``dumpdata`` and has same parameters, but writes fixtures directly to filesystem. Concretly into ``GITVERSIONS_ROOT_PATH``.

.. code-block:: bash

    python manage.py gitversions web --indent=4 --format=json

    python manage.py gitversions --indent=4 --format=json --exclude=elephantblog

     python manage.py gitrestore --url=git@gitlab.com:michaelkuty/test-backup.git

    Clonning initial data from git@gitlab.com:michaelkuty/test-backup.git
    Loaded 2498 instances and 0 was skipped from total 2498 in 12 loaddata iterations and 25 saving iterations.

Read More
=========

* ...
