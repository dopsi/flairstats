import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "flairstats",
    version = "0.0.1",
    author = "Simon Doppler",
    author_email = "dopsi.dev@gmail.com",
    description = ("Get subreddit statistics"),
    license = "MIT",
    keywords = "reddit statistics",
    url = "http://github.com/dopsi/flairstats",
    packages=['flairstats'],
    data_files=[
        ('share/doc/flairstats/config', ['config/config.json']),
        ('lib/systemd/system', ['systemd/system/flairstats-fetchbot@.service', 'systemd/system/flairstats-fetchbot@.timer'])
    ],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 2- Pre-Alpha",
        "Topic :: Text Processing :: Markup :: HTML",
        "License :: OSI Approved :: MIT License",
    ],
    install_dependencies=[
        'htmlgenerator',
        'praw'
    ]
)
