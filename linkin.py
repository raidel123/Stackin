#!/usr/bin/env python

import os
import subprocess
import glob
import json

from subprocess import PIPE
from datetime import datetime

#---------------------------------------------------------------------------
# Globals
PATH = os.getcwd()
reports_dir = "pdfbox_issues"
repo = "pdfbox"

#---------------------------------------------------------------------------
# Get short hashes for all commits
def getHashes():
    hashes = subprocess.check_output('git log --pretty=format:"%h"', shell=True)
    hashes = hashes.split('\n')

    #print "hashes:", hashes
    return hashes

#---------------------------------------------------------------------------
# 1.1
def IssueReport():

    issues = []
    issue_files = glob.glob(PATH + '/' + reports_dir + '/' + '*')
    # print issue_files

    for file in issue_files:
        try:
            with open(file) as f:
                file = json.load(f)
            issues.extend(file['issues'])
    	except ValueError as e:
            print('invalid json: %s' % e)
            return None # or: raise

    # print "\t\t", len(issues)

    # print issues

    return issues;

#---------------------------------------------------------------------------
# 1.3
def BugsByName(issues):
    bug_names = []
    # print len(issues)
    for issue in issues:
        issue_name = issue['fields']['issuetype']['name']
        issue_key = issue['key']
        # print issue_key
        if issue_name == "Bug":
            # print issue_key
            bug_names.append(issue_key)

            '''
            if issue_key in bug_names:
                rc_per_cat[issue_name] += 1
            else:
                rc_per_cat[issue_name] = 1
            '''

    return bug_names

#---------------------------------------------------------------------------
# 2.1
def CommitsFixBugs(hashes):
    commit_info = {}
    bugs = BugsByName(IssueReport())
    # print bugs
    for hash in hashes:
        # commits = subprocess.check_output('git log --name-only --oneline ' + hash, shell=True)
        commits = subprocess.check_output('git show --pretty="format:%s" --name-only --oneline ' + hash, shell=True)
        commits = commits.split('\n')[:-1]
        #print "commits:", commits
        commit_list = []
        for commit in commits:
            commit_list.append(commit.split('\n'))

        commit_info[hash] = commit_list

    files_changed = []
    for key, value in commit_info.iteritems():
        # print "verbose:",key, value
        commit_msg = value[0][0]
        if 'bug' in (commit_msg).lower() :
            # print commit_msg
            for bug_name in bugs:
                # print bug_name
                if bug_name in commit_msg:
                    # print key, len(value)-1, value
                    files_changed.append(len(value)-1)

    print "\t\tMinimum Number of Files:", min(files_changed)
    print "\t\tMaximum Number of Files:", max(files_changed)
    print "\t\tAverage Number of Files:", sum(files_changed)/len(files_changed)

#---------------------------------------------------------------------------
# 2.2
def TimeDifferenceBugs():
    commit_info = {}
    bugs = BugsByName(IssueReport())
    # print bugs
    # commits = subprocess.check_output('git log --name-only --oneline ' + hash, shell=True)
    # commits = subprocess.check_output('git show --pretty="format:%s" --name-only --oneline ' + hash, shell=True)

    times_commits = {}
    closed_commits = {}

    issues = IssueReport()
    commits = subprocess.check_output('git log --pretty="format:%ad~%s"', shell=True)
    # print 'decode:', commits.decode('utf-8')

    commits = commits.split('\n')[:-1]

    for commit in commits:
        # print commits[i].split('~')
        date_t = commit.split('~')[0].split('+')[0]
        date = datetime.strptime(date_t, '%c ')

        times_commits[date] = commit


    times_commits = sorted(times_commits.iteritems())
    #for key, value in times_commits:
        # print key, value

    for issue in issues:
        issue_name = issue['fields']['issuetype']['name']
        issue_status = issue['fields']['status']['name']
        issue_key = issue['key']
        if issue_name == "Bug" and (issue_status == "Closed" or issue_status == "Resolved"):
            # created = (issue['fields']['created']).split('+')[0]
            resolved = (issue['fields']['resolutiondate']).split('+')[0]

            # created_date = datetime.strptime(created, '%Y-%m-%dT%H:%M:%S.%f')
            resolved_date = datetime.strptime(resolved, '%Y-%m-%dT%H:%M:%S.%f')
            closed_commits[issue_key] = resolved_date

    time_difference = []
    for j_key, j_value in closed_commits.iteritems():
        for g_key, g_value in times_commits:
            # print "verbose:", j_key, g_value
            if j_key.lower() in g_value.decode('utf-8').lower() and 'bug' in g_value.decode('utf-8').lower():
                delta = j_value - g_key
                # print delta.total_seconds()
                time_difference.append(abs(delta.total_seconds()))
                break

    print "\t\tMinimum Time Difference (in seconds):", min(time_difference)
    print "\t\tMaximum Time Difference (in seconds):", max(time_difference)
    print "\t\tAverage Time Difference (in seconds):", sum(time_difference)/len(time_difference)

    '''
    #print "commits:", commits
    commit_list = []
    for commit in commits:
        commit_list.append(commit.split('\n'))

    commit_info[hash] = commit_list
    '''


############################################################################

if __name__ == "__main__":
    os.chdir(PATH + '/' + repo)

    print "[2] Linking commits with bug reports (50 points):\n"
    # print "\tDownloading reported issues on JIRA for pdfbox..."

    #-----------------------------------------------------------------------
    print "\t(2.1) Maximun, Minimum, and Average Time Difference per Bug Fix:\n"
    hashes = getHashes()
    CommitsFixBugs(hashes)
    print

    #-----------------------------------------------------------------------
    print "\t(2.2) Maximun, Minimum, and Average Number of Files per Bug Fix:\n"
    TimeDifferenceBugs()
    print

    #-----------------------------------------------------------------------

    os.chdir(PATH)

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
