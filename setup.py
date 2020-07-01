import os
import sys
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'ott.utils',
    'pystache',
    'pyramid',
    'pyramid_tm',
    'pyramid_mako',
    'waitress',
]

extras_require = dict(
    dev=[],
)

setup(
    name='ott.proxy',
    version='0.1.0',
    description='Open Transit Tools - OTT Server Proxy',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
    ],
    author="Open Transit Tools",
    author_email="info@opentransittools.org",
    dependency_links=[
        'git+https://github.com/OpenTransitTools/utils.git#egg=ott.utils-0.1.0',
    ],
    license="Mozilla-derived (http://opentransittools.com)",
    url='http://opentransittools.com',
    keywords='ott, otp, services',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    extras_require=extras_require,
    tests_require=requires,
    test_suite="ott.proxy.tests",
    entry_points="""
        [paste.app_factory]
        main = ott.proxy.pyramid.app:main
        [console_scripts]
    """,
)
