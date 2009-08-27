#!/usr/bin/env python
'''
Created on Apr 20, 2009

@author: kurtjx
'''
import sys
from distutils.core import setup
try:
    import mutagen
except:
    print 'ERROR: mutagen is not installed - try $ easy_install mutagen'
    sys.exit(1)
try:
    import musicbrainz2
except:
    print 'ERROR: musicbrainz2 is not installed - http://musicbrainz.org/doc/python-musicbrainz2_Download'

setup(name='gnatlib',
      version='0.01',
      description='A module for looking up musicbrainz URIs',
      author='Kurt Jacobson',
      author_email='kurt.jacobson (at) elec.qmul.ac.uk',
      url='http://omras2.org/gnatlib',
      packages=['gnatlib'],
     )
