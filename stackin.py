#!/usr/bin/env python
import os
import pandas as pd
import sqlite3


def createdb():
	file = 'hw4_data.csv'
	# print pd.read_csv(file, nrows=5)
	connex = sqlite3.connect("csv_database.db")  # Opens file if exists, else creates file
	cur = connex.cursor()  # This object lets us actually send messages to our DB and receive results

	for chunk in pd.read_csv(file, chunksize=4, encoding='utf-8'):
		chunk.to_sql(name="csv_table", con=connex, if_exists="append", index=False)  #"name" is name of table
		# print(chunk.iloc[0, 1])

	'''
	chunksize = 100000
	i = 0
	j = 1
	for df in pd.read_csv(file, chunksize=chunksize, iterator=True):
	      df = df.rename(columns={c: c.replace(' ', '') for c in df.columns})
	      df.index += j
	      i+=1
	      df.to_sql('table', csv_database, if_exists='append')
	      j = df.index[-1] + 1
	'''

#---------------------------------------------------------------------------
############################################################################

if __name__ == "__main__":
	print "[3] Mining StackOverflow (150 points):\n"
	# print "\tDownloading reported issues on JIRA for pdfbox..."

	#-----------------------------------------------------------------------
	print "\t(3.1) :\n"
	createdb()
	print

	#-----------------------------------------------------------------------
	print "\t(3.2) :\n"

	print

	#-----------------------------------------------------------------------
	print "\t(3.3) :\n"

	print

	#-----------------------------------------------------------------------
	print "\t(3.4) :\n"

	print

	#-----------------------------------------------------------------------
	# TODO : Create a graph for the data output
	print "\t(3.5) :\n"

	print

	#-----------------------------------------------------------------------
	# TODO : not sure if null is the way to go for unresolved, no "unresolved" field
	print "\t(3.6) :\n"

	print

	#-----------------------------------------------------------------------
	print "\t(3.7) :\n"

	print

	#-----------------------------------------------------------------------
	print "\t(3.8) :\n"

	print

	#-----------------------------------------------------------------------
	print "\t(3.9) :\n"

	print

	#-----------------------------------------------------------------------
	# TODO
	print "\t(3.10) :\n"

	print


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
