#!/usr/bin/env python

# Setuptools
from setuptools import setup, find_packages

# Read version from datatables/__init__.py
__VERSION__ = [line for line in file('datatables/__init__.py', 'rb') \
               if line.startswith('__VERSION__')][0].split(\
               '=')[1].strip().lstrip('\'').rstrip('\'')

setup(
    name='django-datatables',
    version=__VERSION__,
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
    install_requires=['Django>=1.3', 'decorator'],
    setup_requires=[],
    tests_require=['Django>=1.3', 'decorator', 'django-fortunecookie>=0.1.1', 'django-setuptest'],
    test_suite='test_app.TestSuite',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
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
            'version': __VERSION__,
            'release': __VERSION__,
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
)
