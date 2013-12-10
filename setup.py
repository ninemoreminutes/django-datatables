#!/usr/bin/env python

# Python
import os
import subprocess
import time

# Setuptools
from setuptools import setup, find_packages
from setuptools.command.egg_info import egg_info as _egg_info

class egg_info(_egg_info):
    """Custom egg_info class to capture revision from Subversion."""

    def tags(self):
        version = ''
        if self.tag_build:
            version += self.tag_build
        if self.tag_svn_revision:
            version += '-r%s' % self.get_svn_revision()
        if self.tag_date:
            version += time.strftime("-%Y%m%d")
        return version

    def get_svn_revision(self):
        try:
            revision = _egg_info.get_svn_revision(self)
        except TypeError:
            revision = _egg_info.get_svn_revision()
        if revision == '0':
            path = os.path.dirname(__file__)
            try:
                cmdline = ['svnversion', '-n', path]
                rev = subprocess.check_output(cmdline).strip()
                if rev and rev != 'exported' and 'unvers' not in rev.lower():
                    revision = rev
            except:
                pass
        return revision

# Read version from datatables/__init__.py (don't import)
__version__ = [line for line in file('datatables/__init__.py', 'rb') \
               if line.startswith('__version__')][0].split(\
               '=')[1].strip().lstrip('\'').rstrip('\'')

setup(
    name='django-datatables',
    version=__version__,
    author='Nine More Minutes, Inc.',
    author_email='support@ninemoreminutes.com',
    description='Django integration of DataTables jQuery plugin.',
    long_description=file('README', 'rb').read(),
    license='BSD',
    keywords='django datatables jquery tables',
    url='https://projects.ninemoreminutes.com/projects/django-datatables/',
    packages=find_packages(exclude=['test_app', 'test_project']),
    include_package_data=True,
    zip_safe=False,
    install_requires=['Django>=1.4', 'decorator'],
    setup_requires=[],
    tests_require=[
        'decorator',
        'Django',
        'django-fortunecookie>=0.1.1',
        'django-setuptest',
        'django-debug-toolbar',
        'django-devserver',
        'django-extensions',
        'South',
    ],
    test_suite='test_suite.TestSuite',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: JavaScript',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
    ],
    options={
        'egg_info': {
            'tag_svn_revision': 1,
            'tag_build': '.dev',
        },
        'build_sphinx': {
            'source_dir': 'docs',
            'build_dir': 'docs/_build',
            'all_files': True,
            'version': __version__,
            'release': __version__,
        },
        'upload_sphinx': {
            'upload_dir': 'docs/_build/html',
        },
        'aliases': {
            # FIXME: Add test to aliases below.
            'dev_build': 'egg_info sdist build_sphinx',
            'release_build': 'egg_info -b "" sdist build_sphinx',
            'release_and_upload': 'egg_info -b "" sdist register upload',
        },
    },
    cmdclass={'egg_info': egg_info},
)
