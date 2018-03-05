#!/usr/bin/env python
import os
import sqlite3

import pandas as pd
import matplotlib.pyplot as plt

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
# 3.1
def QueryAnswerCount():

	# cur.execute("SELECT AVG(AnswerCount) FROM csv_table")
	cur.execute("SELECT AnswerCount FROM csv_table")

	rows = cur.fetchall()

	num_answers  = 0
	num_not_null = 0
	for row in rows:
		if row[0] is not None:
			num_answers  += row[0]
			num_not_null += 1

	print '\t\tExcluding Null Entries:'
	print '\t\t\t------------------------------'
	print '\t\t\tAverage:', num_answers/num_not_null
	print '\t\t\t------------------------------'
	print '\t\t\tTotal Answers:', num_answers
	print '\t\t\tNumber of Questions:', num_not_null
	print

	print '\t\tIncluding Null Entries:'
	print '\t\t\t------------------------------'
	print '\t\t\tAverage:', num_answers/len(rows)
	print '\t\t\t------------------------------'
	print '\t\t\tTotal Answers:', num_answers
	print '\t\t\tNumber of Questions:', len(rows)

#---------------------------------------------------------------------------
# 3.2
def QuestionSDistribution():
	# conn = sqlite3.connect("csv_database.db")
	# cur = conn.cursor()

	# cur.execute("")
	df = pd.read_sql_query("SELECT Id, Score FROM csv_table", conn)
	#print df
	#print df['Id'].values
	#print df['Score'].values

#---------------------------------------------------------------------------
# 3.3
def AnswerSDistribution():
	print '\t\t'

#---------------------------------------------------------------------------
# 3.4
def AcceptedASDistribution():
	print '\t\t'

#---------------------------------------------------------------------------
# 3.5


#---------------------------------------------------------------------------
# 3.6


#---------------------------------------------------------------------------
# 3.7


#---------------------------------------------------------------------------
# 3.8


#---------------------------------------------------------------------------
# 3.9


#---------------------------------------------------------------------------
# 3.1-

############################################################################

if __name__ == "__main__":
	print "[3] Mining StackOverflow (150 points):\n"
	# print "\tDownloading reported issues on JIRA for pdfbox..."
	# createdb()

	#-----------------------------------------------------------------------
	# TODO : Uncomment query
	print "\t(3.1) :\n"
	# QueryAnswerCount()
	print

	#-----------------------------------------------------------------------
	# TODO :
	print "\t(3.2) :\n"
	QuestionSDistribution();
	print

	#-----------------------------------------------------------------------
	# TODO :
	print "\t(3.3) :\n"

	print

	#-----------------------------------------------------------------------
	# TODO :
	print "\t(3.4) :\n"

	print

	#-----------------------------------------------------------------------
	# TODO :
	print "\t(3.5) :\n"

	print

	#-----------------------------------------------------------------------
	# TODO :
	print "\t(3.6) :\n"

	print

	#-----------------------------------------------------------------------
	# TODO :
	print "\t(3.7) :\n"

	print

	#-----------------------------------------------------------------------
	# TODO :
	print "\t(3.8) :\n"

	print

	#-----------------------------------------------------------------------
	# TODO :
	print "\t(3.9) :\n"

	print

	#-----------------------------------------------------------------------
	# TODO
	print "\t(3.10) :\n"

	print
