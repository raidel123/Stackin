#!/usr/bin/env python

import os
import subprocess
import git
import json

from subprocess import PIPE

PATH = os.getcwd()
repos = ["pdfbox"]

def foo():
	print 'hello world!'

def aa():
    print "\t\ta)"
    a = subprocess.check_output('git rev-list --count HEAD', shell=True)
    a = a.rstrip('\n')
    print "\t\t\tTotal Number of Commits:", a

gitP = subprocess.Popen(('git log --pretty="%ae%n%ce"'), shell=True, stdout=PIPE)
    sortP = subprocess.Popen(('sort'), shell=True, stdin=gitP.stdout, stdout=PIPE)
    uniqP = subprocess.Popen(('uniq'), shell=True, stdin=sortP.stdout, stdout=PIPE)
    c = subprocess.check_output('wc -l', shell=True, stdin=uniqP.stdout)
    c = c.rstrip('\n')
	print "\t\t\tNumber of contributors:", c

if __name__ == "__main__":
	foo()
