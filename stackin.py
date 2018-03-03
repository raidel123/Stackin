#!/usr/bin/env python

import os
import subprocess
import json
#import git

from subprocess import PIPE

PATH = os.getcwd()
MAXRESULTS = 1000


repo = "pdfbox"

def foo():
	print 'hello world!'

def IssueReport(project):

	a = subprocess.check_output('curl -o ' + ("pdfbox_issues/"+repo+str(0)+".json") + ' "https://issues.apache.org/jira/rest/api/2/search?jql=project="' + project + '"&startAt=0&maxResults=1000"', shell=True)
	a = a.rstrip('\n')
	print a

	'''
	maxreached = False
	page = 0
	while not maxreached:
		a = subprocess.check_output('curl -o' + ("pdfbox_issues/"+repo+page+".json") + '"https://issues.apache.org/jira/rest/api/2/search?jql=project="' + project + '"&startAt=' + str(page*1000) + '&maxResults=1000"', shell=True)
		a = a.rstrip('\n')
		print a
	'''

	'''
	gitP = subprocess.Popen(('git log --pretty="%ae%n%ce"'), shell=True, stdout=PIPE)
	sortP = subprocess.Popen(('sort'), shell=True, stdin=gitP.stdout, stdout=PIPE)
	uniqP = subprocess.Popen(('uniq'), shell=True, stdin=sortP.stdout, stdout=PIPE)
	c = subprocess.check_output('wc -l', shell=True, stdin=uniqP.stdout)
	c = c.rstrip('\n')
	print "\t\t\tNumber of contributors:", c
	'''

if __name__ == "__main__":
	print "Downloading reported issues on JIRA for pdfbox..."
	report = IssueReport(repo)
