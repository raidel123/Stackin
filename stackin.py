#!/usr/bin/env python
import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats.stats import pearsonr

#---------------------------------------------------------------------------
# Globals
# connect to sqlite3 DataBase file
conn = sqlite3.connect("csv_database.db")  # Opens file if exists, else creates file
cur = conn.cursor()

#---------------------------------------------------------------------------

def createdb(file=None):
	if file is None:
		file = 'hw4_data.csv'

	# print pd.read_csv(file, nrows=5)
	# conn = sqlite3.connect("csv_database.db")  # Opens file if exists, else creates file
	# cur = conn.cursor()  # This object lets us actually send messages to our DB and receive results

	for chunk in pd.read_csv(file, chunksize=4, encoding='utf-8'):
		chunk.to_sql(name="csv_table", con=conn, if_exists="append", index=False)  #"name" is name of table

#---------------------------------------------------------------------------
# Plot Distribution
def PlotDistribution(df, o_title, n_title):
	df.plot(kind='box', vert=False, showfliers=True, title=o_title)
	df.plot(kind='box', vert=False, showfliers=False, title=n_title)
	distribution = df.describe().to_string().split('\n')[1:]

	for field in distribution:
		print '\t\t', field
	plt.show()

#---------------------------------------------------------------------------
# extract tags from list
def GetTags(tags_list):
	tags = {}
	for list in tags_list:
		t_list = list.split('>')
		for i_tag in t_list:
			key = i_tag[1:]

			if key == '':
				continue

			if key not in tags:
				tags[key] = 1
			else:
				tags[key] += 1

	return tags

#---------------------------------------------------------------------------
def GetUsers(tags_list):
	users = {}
	for user in tags_list:
		if user not in users:
			users[user] = 1
		else:
			users[user] += 1

	return tags
#---------------------------------------------------------------------------
# 3.1
def QueryAnswerCount():

	# cur.execute("SELECT AVG(AnswerCount) FROM csv_table")
	# df = pd.read_sql_query("SELECT Score FROM csv_table WHERE PostTypeID=1;", conn)
	cur.execute("SELECT AnswerCount FROM csv_table WHERE PostTypeID=1;")

	rows = cur.fetchall()

	num_answers  = 0
	num_not_null = 0
	for row in rows:
		if row[0] is not None:
			num_answers  += row[0]
			num_not_null += 1

	print '\t\t\tTotal Answers:', num_answers
	print '\t\t\tNumber of Questions:', len(rows)
	print '\t\t\t------------------------------'
	print '\t\t\tAverage:', num_answers/len(rows)
	print '\t\t\t------------------------------'

#---------------------------------------------------------------------------
# 3.2
def QuestionSDistribution():

	df = pd.read_sql_query("SELECT Score FROM csv_table WHERE PostTypeID=1;", conn)
	o_title = '(3.2a) Question Score Distribution (Outliers)'
	n_title = '(3.2b) Question Score Distribution (No-Outliers)'
	PlotDistribution(df, o_title, n_title)

#---------------------------------------------------------------------------
# 3.3
def AnswerSDistribution():
	df = pd.read_sql_query("SELECT Score FROM csv_table WHERE PostTypeID=2;", conn)
	o_title = '(3.3a) Answer Score Distribution (Outliers)'
	n_title = '(3.3b) Answer Score Distribution (No-Outliers)'
	PlotDistribution(df, o_title, n_title)

#---------------------------------------------------------------------------
# 3.4
def AcceptedASDistribution():
	df = pd.read_sql_query("SELECT Score FROM csv_table WHERE PostTypeID=2 AND Id IN (SELECT AcceptedAnswerId FROM csv_table WHERE PostTypeID=1);", conn)
	o_title = '(3.4a) Accepted Answer Score Distribution (Outliers)'
	n_title = '(3.4b) Accepted Answer Score Distribution (No-Outliers)'
	PlotDistribution(df, o_title, n_title)

#---------------------------------------------------------------------------
# 3.5
def AcceptedUSDistribution():
	# df = pd.read_sql_query("SELECT Score FROM csv_table WHERE PostTypeID=2 AND Id IS NOT IN (SELECT AcceptedAnswerId FROM csv_table WHERE PostTypeID=1);", conn)
	df = pd.read_sql_query("SELECT Score FROM csv_table WHERE PostTypeID=2 AND Id NOT IN (SELECT AcceptedAnswerId FROM csv_table WHERE PostTypeID=1 AND AcceptedAnswerId IS NOT NULL);", conn)
	o_title = '(3.5a) Unaccepted Answer Score Distribution (Outliers)'
	n_title = '(3.5b) Unaccepted Answer Score Distribution (No-Outliers)'
	PlotDistribution(df, o_title, n_title)
	# print df

#---------------------------------------------------------------------------
# 3.6
def PearsonCorrelation():
	df = pd.read_sql_query("SELECT Score, AnswerCount FROM csv_table WHERE PostTypeID=1;", conn)

	x = df['Score'].values.tolist()
	y = df['AnswerCount'].values.tolist()

	corr_coef, p_value = pearsonr(x, y)
	print '\t\tPearson Correlation:', corr_coef, '\n'
	print '\t\tP-Value: ', p_value

#---------------------------------------------------------------------------
# 3.7
def TagFrequency():

	df = pd.read_sql_query("SELECT Tags FROM csv_table WHERE PostTypeID=1;", conn)
	tags_list = df['Tags'].values.tolist()

	tags = GetTags(tags_list)

	count = 0
	for key, value in sorted(tags.iteritems(), key=lambda (k,v): (v,k), reverse=True):
		count += 1
		print '\t\t', count, ") %s: %s" % (key, value)
		if count == 10:
			break

#---------------------------------------------------------------------------
# 3.8
def TopUsers():
	df = pd.read_sql_query("SELECT Id FROM csv_table WHERE PostTypeID=2;", conn)
	users_list = df['Id'].values.tolist()

	users = GetUsers(users_list)

	count = 0
	for key, value in sorted(users.iteritems(), key=lambda (k,v): (v,k), reverse=True):
		count += 1
		print '\t\t', count, ") %s: %s" % (key, value)
		if count == 10:
			break

#---------------------------------------------------------------------------
# 3.9
def TopTagsWAnswer():
	print

#---------------------------------------------------------------------------
# 3.10
def TopTagsWAAnswer():
	print

############################################################################

if __name__ == "__main__":
	print "[3] Mining StackOverflow (150 points):\n"
	# print "\tDownloading reported issues on JIRA for pdfbox..."
	# createdb()

	#-----------------------------------------------------------------------
	# TODO : Uncomment query
	print "\t(3.1) Average Number of Answers per Question:\n"
	# QueryAnswerCount()
	print

	#-----------------------------------------------------------------------
	# TODO : Uncomment query
	print "\t(3.2) Distribution of Scores for Questions:\n"
	# QuestionSDistribution()
	print

	#-----------------------------------------------------------------------
	# TODO : Uncomment query
	print "\t(3.3) Distribution of Scores for Answers:\n"
	# AnswerSDistribution()
	print

	#-----------------------------------------------------------------------
	# TODO : Uncomment query
	print "\t(3.4) Distribution of Scores for Accepted Answers:\n"
	# AcceptedASDistribution()
	print

	#-----------------------------------------------------------------------
	# TODO : Uncomment query
	print "\t(3.5) Distribution of Scores for Unaccepted Answers:\n"
	# AcceptedUSDistribution()
	print

	#-----------------------------------------------------------------------
	# TODO : Uncomment query
	print "\t(3.6) Correlation Between the Question Score and Number of Answers:\n"
	# PearsonCorrelation()
	print

	#-----------------------------------------------------------------------
	# TODO : Uncomment query
	print "\t(3.7) Top 10 Frequent Tags:\n"
	# TagFrequency()
	print

	#-----------------------------------------------------------------------
	# TODO : Uncomment query
	print "\t(3.8) Top 10 Users by Number of Questions Answered:\n"
	TopUsers()
	print

	#-----------------------------------------------------------------------
	# TODO : Uncomment query
	print "\t(3.9) Top 5 Frequent Tags of Questions Without an Answer:\n"
	TopTagsWAnswer()
	print

	#-----------------------------------------------------------------------
	# TODO : Uncomment query
	print "\t(3.10) Top 5 Frequent Tags of Questions Without an Accepted Answer:\n"
	TopTagsWAAnswer()
	print

	print
