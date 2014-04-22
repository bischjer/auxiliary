from __future__ import with_statement
from fabric.api import *
import os

this_directory = os.path.dirname(os.path.abspath(__file__))

modules = ['',]

def cleanpyc():
    print "Number of .pyc files we found was: %s" % local('find . -iname \'*.pyc\' | wc -l')
    local('find . -iname \'*.pyc\' -delete', capture=False)
    local("find . -name 'logs' -prune -exec rm -r '{}' \;", capture=False) 

def todo():
    local('grep -ir "TODO:" %s' % this_directory)

def distribute():
    local('python setup.py bdist --format zip')
