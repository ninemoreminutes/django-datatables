#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='django-datatables',
    version='0.1.0',
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
    install_requires=['Django>=1.3'],
    setup_requires=[],
    tests_require=['Django>=1.3', 'django-setuptest'],
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
        },
        'upload_sphinx': {
            'upload_dir': 'docs/_build/html',
        },
        'aliases': {
            'dev_build': 'egg_info test sdist build_sphinx',
            'release_build': 'egg_info -b "" -R test sdist build_sphinx',
        },
    },
)
