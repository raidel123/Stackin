#!/usr/bin/env python

import os
import subprocess
import json
import glob
import textwrap
import calendar

from subprocess import PIPE
from tabulate import tabulate
from datetime import datetime
from scipy.stats.stats import pearsonr

#---------------------------------------------------------------------------
# Global Variables

PATH = os.getcwd()
MAXRESULTS = 1000

reports_dir = "pdfbox_issues"
repo = "pdfbox"

#---------------------------------------------------------------------------
# 1.1
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

	print "\t\t", len(issues)

	return issues;

#---------------------------------------------------------------------------
# 1.2
def IssuePerCategory(issues):
	issue_per_cat = {}
	for issue in issues:
		issue_name = issue['fields']['issuetype']['name']
		if issue_name in issue_per_cat:
			issue_per_cat[issue_name] += 1
		else:
			issue_per_cat[issue_name] = 1

	total = 0.0
	for key, value in issue_per_cat.iteritems():
		total += float(value)

	results = {}
	for key, value in issue_per_cat.iteritems():
		results[key] = [key, value, "{0:.2f}%".format(value/total * 100)]

	tab_list = tabulate([value for value in results.values()], headers=["Category", "(#) Issues", "(%) Percent"]).split('\n')

	for list in tab_list:
		print '\t\t', list

	return issue_per_cat

#---------------------------------------------------------------------------
# 1.3
def RCPerCategory(issues, issues_per_cat):
	rc_per_cat = {}
	for issue in issues:
		issue_name 	 = issue['fields']['issuetype']['name']
		issue_status = issue['fields']['status']['name']
		if issue_status == "Closed" or issue_status == "Resolved":
			if issue_name in rc_per_cat:
				rc_per_cat[issue_name] += 1
			else:
				rc_per_cat[issue_name] = 1

	for key, value in rc_per_cat.iteritems():
		print '\t\t', "{0:.2f}%".format(float(value)/issues_per_cat[key] * 100), 'of the', issues_per_cat[key], 'number of reported', key.upper(), 'have been resolved.'

	return rc_per_cat

#---------------------------------------------------------------------------
# 1.4
def TopReporter(issues):
	reporters = {}
	for issue in issues:
		if issue['fields']['reporter'] is not None:
			reporter_key = issue['fields']['reporter']['key']
			if reporter_key in reporters:
				reporters[reporter_key] += 1
			else:
				reporters[reporter_key] = 1

	max = []
	for key, value in reporters.iteritems():
		if not max:
			 max = [key, value]
		else:
			if value > max[1]:
				max = [key, value]

	print '\t\tTop Reporter Key:', max[0]
	print '\t\tNumber of Reports:', max[1]

	return reporters

#---------------------------------------------------------------------------
# 1.5
def MonthlyIssues(issues):
	monthly_issues = {}
	bug_dates = []
	for issue in issues:
		# take off the +0000 part of the created date, get the beginning([0])
		issue_name = issue['fields']['issuetype']['name']
		if issue_name == "Bug":
			created = (issue['fields']['created']).split('+')[0]

			date = datetime.strptime(created, '%Y-%m-%dT%H:%M:%S.%f')
			bug_dates.append(date)

			key = (date.year, date.month)
			if key not in monthly_issues:
				monthly_issues[key] = 1
			else:
				monthly_issues[key] += 1

	monthly_count = []
	for key in sorted(monthly_issues.keys()):
		monthly_count.append([key[0], str(key[1]) + '-' + calendar.month_name[key[1]], monthly_issues[key]])

	print '\t\ta) First Bug Reported:', min(bug_dates)
	print '\t\tb) Last Bug Reported :', max(bug_dates)
	print

	print '\t\tc) All Bugs Reported By Year, Month:'
	tab_list = 	tabulate(monthly_count,
				headers=["Year", "Month", "(#) Bugs Reported"]).split('\n')
	for list in tab_list:
		print '\t\t\t', list

	return monthly_issues

#---------------------------------------------------------------------------
# 1.6
def UnresolvedBugs(issues):
	unresolved = 0
	for issue in issues:
		issue_name = issue['fields']['issuetype']['name']
		resolution = issue['fields']['resolution']
		# resolution_name = issue['fields']['resolution']['name']
		if issue_name == "Bug" and resolution is None:
			unresolved += 1

	print '\t\t', unresolved
	return unresolved

#---------------------------------------------------------------------------
# 1.7
def BugsPriorityField(issues):
	priority_names = []
	for issue in issues:
		issue_name = issue['fields']['issuetype']['name']
		priority = issue['fields']['priority']

		if issue_name == "Bug" and priority is not None:
			priority_names.append(issue['fields']['priority']['name'])

	priority_names = sorted(list(set(priority_names)))
	for item in priority_names:
		print '\t\t', item

	return priority_names

#---------------------------------------------------------------------------
# 1.8
def BugResolutionTime(issues):
	resolution_delta = []
	for issue in issues:
		issue_name = issue['fields']['issuetype']['name']
		issue_status = issue['fields']['status']['name']
		if issue_name == "Bug" and (issue_status == "Closed" or issue_status == "Resolved"):
			created = (issue['fields']['created']).split('+')[0]
			resolved = (issue['fields']['resolutiondate']).split('+')[0]

			created_date = datetime.strptime(created, '%Y-%m-%dT%H:%M:%S.%f')
			resolved_date = datetime.strptime(resolved, '%Y-%m-%dT%H:%M:%S.%f')
			delta = resolved_date - created_date

			resolution_delta.append(delta)

	print '\t\t a) Average Time:'
	print '\t\t\t', reduce(lambda x, y: x + y, resolution_delta) / len(resolution_delta)
	print
	print '\t\t b) Longest Time:'
	print '\t\t\t', max(resolution_delta)
	print
	print '\t\t c) Shortest Time:'
	print '\t\t\t', min(resolution_delta)
	print

	return resolution_delta

#---------------------------------------------------------------------------
# 1.9
def BugPResolutionTime(issues):
	priority_delta = {}

	for issue in issues:
		issue_name = issue['fields']['issuetype']['name']
		issue_status = issue['fields']['status']['name']

		if issue_name == "Bug" and (issue_status == "Closed" or issue_status == "Resolved"):
			priority = issue['fields']['priority']

			if priority is None:
				continue

			priority_name = issue['fields']['priority']['name']

			created = (issue['fields']['created']).split('+')[0]
			resolved = (issue['fields']['resolutiondate']).split('+')[0]

			created_date = datetime.strptime(created, '%Y-%m-%dT%H:%M:%S.%f')
			resolved_date = datetime.strptime(resolved, '%Y-%m-%dT%H:%M:%S.%f')
			delta = resolved_date - created_date

			if priority_name in priority_delta:
				priority_delta[priority_name].append(delta)
			else:
				priority_delta[priority_name] = [delta]

	for priority, deltas in sorted(priority_delta.iteritems()):

		print '\t\tPriority:', priority
		print '\t\t----------------------------------------------------------'
		print '\t\t a) Average Time:'
		print '\t\t\t', reduce(lambda x, y: x + y, deltas) / len(deltas), '\n'
		print '\t\t b) Longest Time:'
		print '\t\t\t', max(deltas), '\n'
		print '\t\t c) Shortest Time:'
		print '\t\t\t', min(deltas), '\n'

	print '\t\t=========================================================='
	print '\t\tObservations:'
	print '\t\t=========================================================='
	print '\t\t From the results gathered above, issues marked as "Major"'
	print '\t\t are on average resolved/closed much faster than issues'
	print '\t\t marked as "Minor". However, on average issues that are'
	print '\t\t marked as "Blocker", or "Trivial" are resolved faster than'
	print '\t\t "Major" issues. An Issue marked as "Major" holds by far'
	print '\t\t the shortest resolution time, resolved within 19 seconds.'

	return priority_delta



#---------------------------------------------------------------------------
# 1.10
def LinearCorrelation(issues):
	correlation_data = {}
	for issue in issues:
		issue_name = issue['fields']['issuetype']['name']
		issue_status = issue['fields']['status']['name']
		if issue_name == "Bug" and (issue_status == "Closed" or issue_status == "Resolved"):
			created = (issue['fields']['created']).split('+')[0]
			resolved = (issue['fields']['resolutiondate']).split('+')[0]

			created_date = datetime.strptime(created, '%Y-%m-%dT%H:%M:%S.%f')
			resolved_date = datetime.strptime(resolved, '%Y-%m-%dT%H:%M:%S.%f')
			delta = resolved_date - created_date
			watchers = issue['fields']['watches']['watchCount']

			correlation_data[issue['key']] = [delta, watchers]

	x = [value[0].total_seconds() for value in correlation_data.values()]
	y = [value[1] for value in correlation_data.values()]

	corr_coef, p_value = pearsonr(x, y)
	print '\t\tPearson Correlation:', corr_coef, '\n'
	print '\t\tP-Value: ', p_value, '\n'

	return correlation_data


############################################################################

if __name__ == "__main__":
	print "[1] Analyzing issue tracker activity (150 points):\n"
	# print "\tDownloading reported issues on JIRA for pdfbox..."

	#-----------------------------------------------------------------------
	print "\t(1.1) Number of Issues Reported:\n"
	issues = IssueReport(repo)
	print

	#-----------------------------------------------------------------------
	print "\t(1.2) Issues Per Category:\n"
	issues_per_cat = IssuePerCategory(issues)
	print

	#-----------------------------------------------------------------------
	print "\t(1.3) Resolved/Closed Per Category:\n"
	rc_per_cat = RCPerCategory(issues, issues_per_cat)
	print

	#-----------------------------------------------------------------------
	print "\t(1.4) Top Reporter:\n"
	TopReporter(issues)
	print

	#-----------------------------------------------------------------------
	# TODO : Create a graph for the data output
	print "\t(1.5) Monthly Issues Reported:\n"
	MonthlyIssues(issues)
	print

	#-----------------------------------------------------------------------
	# TODO : not sure if null is the way to go for unresolved, no "unresolved" field
	print "\t(1.6) Number of Unresolved Bugs (Resolution is null):\n"
	UnresolvedBugs(issues)
	print

	#-----------------------------------------------------------------------
	print "\t(1.7) Values in Priority Field (Not Including null):\n"
	BugsPriorityField(issues)
	print

	#-----------------------------------------------------------------------
	print "\t(1.8) Time to Resolve a Bug:\n"
	BugResolutionTime(issues)
	print

	#-----------------------------------------------------------------------
	print "\t(1.9) Time to Resolve a Bug by Priority:\n"
	BugPResolutionTime(issues)
	print

	#-----------------------------------------------------------------------
	# TODO
	print "\t(1.10) Is there a Linear Correlation?:\n"
	LinearCorrelation(issues)
	print
