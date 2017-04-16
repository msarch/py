#!/usr/bin/env python

from distutils.core import setup

setup(name='pylygon',
      version='1.3.2rc',
      author='Chandler Armstrong',
      author_email='omni.armstrong@gmail.com',
      url='http://code.google.com/p/pylygon/',
      description='polygon object for python',
      download_url='http://code.google.com/p/pylygon/downloads/list',
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   'Topic :: Software Development :: Libraries :: pygame'],
      packages=['pylygon'],
      requires=['pygame(>=1.9.1)'],
      provides=['pylygon'])
