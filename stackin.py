#!/usr/bin/env python

import os
import subprocess
import json
import glob
#import git

from subprocess import PIPE

PATH = os.getcwd()
MAXRESULTS = 1000

reports_dir = "pdfbox_issues"
repo = "pdfbox"

def IssueReport(project):

	issues = []
	issue_files = glob.glob(PATH + '/' + reports_dir + '/' + '*')

	for file in issue_files:
		try:
			with open(file) as f:
				file = json.load(f)

			issues.extend(file['issues'])

		except ValueError as e:
			print('invalid json: %s' % e)
			return None # or: raise

	return issues;



if __name__ == "__main__":
	print "Downloading reported issues on JIRA for pdfbox..."
	issues = IssueReport(repo)

	for item in issues:
		for key in item.keys():
			print key



'''
USEFUL OPERATIONS:

# ---------------------------------------------------------------
# Iterate through dictionary

	for key, value in item.iteritems():
		print key, value

	for key in item.keys():
		print key


# ---------------------------------------------------------------
# Subprocess pipes for multiple system calls

	gitP = subprocess.Popen(('git log --pretty="%ae%n%ce"'), shell=True, stdout=PIPE)
	sortP = subprocess.Popen(('sort'), shell=True, stdin=gitP.stdout, stdout=PIPE)
	uniqP = subprocess.Popen(('uniq'), shell=True, stdin=sortP.stdout, stdout=PIPE)
	c = subprocess.check_output('wc -l', shell=True, stdin=uniqP.stdout)
	# c = c.rstrip('\n')
	print "\t\t\tNumber of contributors:", c

# ---------------------------------------------------------------
# Get all the issue reports from curl

	def IssueReport(project):
		# TODO : uncomment for submission
		# json_dir = reports_dir+repo+str(0)+'.json'
		# subprocess.call('curl -o ' + json_dir + ' "https://issues.apache.org/jira/rest/api/2/search?jql=project="' + project + '"&startAt=0&maxResults=1000"', shell=True)

		try:
			with open(json_dir) as f:
				file = json.load(f)
				total_issues = file['total']
		except ValueError as e:
			print('invalid json: %s' % e)
			return None # or: raise

		issues_left = total_issues - MAXRESULTS
		page = 1
		while issues_left > 0:
			json_dir = reports_dir + '/' + repo + str(page) + '.json'

			subprocess.call('curl -o ' + json_dir + ' "https://issues.apache.org/jira/rest/api/2/search?jql=project="' + project + '"&startAt=' + str(page*MAXRESULTS) + '&maxResults=1000"', shell=True)
			# a = subprocess.check_output('curl -o' + ("pdfbox_issues/"+repo+page+".json") + '"https://issues.apache.org/jira/rest/api/2/search?jql=project="' + project + '"&startAt=' + str(page*1000) + '&maxResults=1000"', shell=True)

			page 			+= 1
			# if issues_left > MAXRESULTS:
			issues_left 	-= MAXRESULTS
			# else:
				# issues_left		-= issues_left

# ---------------------------------------------------------------
# ---------------------------------------------------------------
# ---------------------------------------------------------------
# ---------------------------------------------------------------
# ---------------------------------------------------------------
# ---------------------------------------------------------------



'''
