from bs4 import BeautifulSoup
import sqlite3
from time import sleep
import datetime
import getopt, sys
import requests
import string
import re

verbose = False
duration = False
lastFmToken = ""

def titleFromRaw(raw):
	splitted = str(raw)
	splitted = splitted.split('<br/>')
	splitted_edit = splitted[0]
	splitted_edit = splitted_edit[83:]
	return splitted_edit.strip()


def artistFromRaw(raw):
	splitted = str(raw)
	splitted = splitted.split('<br/>')
	try:
		splitted_edit = splitted[1].strip()
		return splitted_edit.strip()
	except:
		return "error"


def shouldNotIngore(raw):
	splitted = raw.split('\n')
	splitted_edit = splitted[0]
	splitted_edit = splitted_edit[:8]
	if (splitted_edit.encode("utf-8") == "A écouté"):
		return True
	else:
		return False

def open_file():
	if (sys.argv[1].endswith('.html')):
		try:
			file = open(sys.argv[1], "r")
			return file
		except:
			print "Could not open your history file"
			sys.exit()
	else:
		print "Your history file should be an html file"
		sys.exit()

def create_env_db(conn):
	cursor = conn.cursor()
	cursor.execute("""
	CREATE TABLE IF NOT EXISTS songs(
		 id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
		 artist TEXT,
		 title TEXT,
		 year TEXT
	)
	""")
	cursor.execute("""
	CREATE TABLE IF NOT EXISTS artist_count(
		 id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
		 artist TEXT,
		 occurence int
	)
	""")
	cursor.execute("""
	CREATE TABLE IF NOT EXISTS songs_count(
		 id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
		 title TEXT,
		 occurence int
	)
	""")
	cursor.execute("""
	CREATE TABLE IF NOT EXISTS report(
		 id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
		 title TEXT,
		 artist TEXT,
		 duration int,
		 occurence int
	)
	""")
	conn.commit()
	return cursor

def flags():
	opts, args = getopt.getopt(sys.argv[2:], "d:v", ["duration="])
	for o, token in opts:
		if o == "-v":
			global verbose
			verbose = True
		elif o in ("-d", "--duration"):
			global duration
			duration = True
			global lastFmToken
			lastFmToken = token

def parse_html(html_doc, cursor):
	soup = BeautifulSoup(html_doc, "html.parser")
	for p in soup.find_all("div", {"class": "content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"}):
		if shouldNotIngore(p.text):
			print datetime.datetime.now()
			cursor.execute("""INSERT INTO songs(title, artist, year) VALUES(?, ?, ?)""", (repr(titleFromRaw(p)), repr(artistFromRaw(p)), "2018"))

def print_db(cursor, printable):
	#Test results from DB
	print ("####################Full List#####################")
	cursor.execute("""SELECT id, artist, title, year FROM songs""")
	rows = cursor.fetchall()
	for row in rows:
		datetime.datetime.now()
		print('{0} : {1} - {2} - {3} | {4}'.format(row[0], re.sub(' +', ' ', filter(lambda x: x in printable, eval(row[1].encode("utf-8")).replace('\n', '').replace('é', 'e').strip())), re.sub(' +', ' ', filter(lambda x: x in printable, eval(row[2].encode("utf-8")).replace('\n', '').replace('é', 'e').strip())), row[3], datetime.datetime.now()))

def prepare_clean_db(cursor, printable):
	#Artist top
	cursor.execute("""SELECT artist, COUNT(*) FROM songs GROUP BY artist""")
	result = cursor.fetchall()
	for res in result:
		cursor.execute("""INSERT INTO artist_count(artist, occurence) VALUES(?, ?)""", (re.sub(' +', ' ', filter(lambda x: x in printable, eval(res[0].encode("utf-8")).replace('\n', '').replace('é', 'e').strip())), res[1]))

	#Song Top
	cursor.execute("""SELECT title, COUNT(*) FROM songs GROUP BY title""")
	result_song = cursor.fetchall()
	for res_song in result_song:
		cursor.execute("""INSERT INTO songs_count(title, occurence) VALUES(?, ?)""", (re.sub(' +', ' ', filter(lambda x: x in printable, eval(res_song[0].encode("utf-8")).replace('\n', '').replace('é', 'e').strip())), res_song[1]))

def print_full_tops(cursor):
	print ("####################Top Artists#####################")
	cursor.execute("""SELECT artist, occurence FROM artist_count ORDER by occurence DESC""")
	rows = cursor.fetchall()
	for row in rows:
		datetime.datetime.now()
		print('{0} - {1}'.format(row[0].encode("utf-8"), row[1]))

	print ("####################Top Songs#####################")
	cursor.execute("""SELECT title, occurence FROM songs_count ORDER by occurence DESC""")
	rows = cursor.fetchall()
	for row in rows:
		datetime.datetime.now()
		print('{0} - {1}'.format(row[0].encode("utf-8"), row[1]))

def delete_duplicate(cursor, printable):
	#Doublon Deletor
	cursor.execute("""SELECT title, COUNT(*), artist FROM songs GROUP BY title""")
	result_doublon = cursor.fetchall()
	for res_doublon in result_doublon:
		cursor.execute("""INSERT INTO report(title, artist, occurence) VALUES(?, ?, ?)""", (re.sub(' +', ' ', filter(lambda x: x in printable, eval(res_doublon[0].encode("utf-8")).replace('\n', '').strip())), re.sub(' +', ' ', filter(lambda x: x in printable, eval(res_doublon[2].encode("utf-8")).replace('\n', '').strip())), res_doublon[1],))

def get_duration(cursor):
	#Count duration
	cursor.execute("""SELECT id, artist, title FROM report""")
	rows = cursor.fetchall()
	for row in rows:
		datetime.datetime.now()
		parameters = {"method": "track.getInfo", "api_key": lastFmToken, "artist": row[1].encode("utf-8"), "track": row[2].encode("utf-8"), "format": "json"}
		response = requests.get("http://ws.audioscrobbler.com//2.0/", params=parameters)
		if (response.status_code == 200):
			json_parsed = response.json()
			if ('error' in json_parsed):
				print "error found"
				cursor.execute("""UPDATE report SET duration = ? WHERE id = ?""", (0, row[0]))
				continue
			else:
				duration = json_parsed['track']['duration']
				cursor.execute("""UPDATE report SET duration = ? WHERE id = ?""", (duration, row[0]))

	#Calcul total duration
	if verbose:
		print ("####################Full List WITHOUT DOUBLON AND DURATION#####################")
	total_duration = 0
	error_rate = 0
	cursor.execute("""SELECT id, artist, title, duration, occurence FROM report""")
	rows = cursor.fetchall()
	for row in rows:
		datetime.datetime.now()
		song_count = row[0]
		if verbose:
			print('{0} : {1} - {2}- {3} - occurence : {4}'.format(row[0], row[1].encode("utf-8"), row[2].encode("utf-8"), row[3], row[4]))
		total_duration += row[3] * row[4]
		if row[3] == 0:
			error_rate = error_rate + 1
	return (total_duration, error_rate, song_count)

def gen_report(cursor, data):
	#Top 10 Report
	sys.stdout = open('report.dat', 'w')
	print ("#################### Top Artists #####################")
	cursor.execute("""SELECT artist, occurence FROM artist_count ORDER by occurence DESC LIMIT 10""")
	rows = cursor.fetchall()
	for row in rows:
		datetime.datetime.now()
		print('{0} - {1}'.format(row[0].encode("utf-8"), row[1]))

	print ("#################### Top Songs #####################")
	cursor.execute("""SELECT title, occurence FROM songs_count ORDER by occurence DESC LIMIT 10""")
	rows = cursor.fetchall()
	for row in rows:
		datetime.datetime.now()
		print('{0} - {1}'.format(row[0].encode("utf-8"), row[1]))

	if duration:
		print ("\n#################### Duration #####################")
		print ('Total duration : {0}', data[0])
		print ('Total song count : ', data[2])
		print ('Error count : ', data[1])
		print ('Error rate : {0}%'.format((float(data[1])/data[2])*100))
	sys.stdout.close()

def main():
	flags()
	#Config
	printable = set(string.printable)
	conn = sqlite3.connect('gmusic.db')
	cursor = create_env_db(conn)
	data = ""

	file = open_file()
	html_doc = file.read()

	print ("Welcome on GMusic Year Wrapper.")
	print ("We are now processing your file. Note that this process can be long (generally between 1 and 4 hours)")
	print ("No more informations will be displayed during this process. You can check log.dat at any time to check progression.")

	#Start log in log file
	if verbose:
		sys.stdout = open('log.dat', 'w')

	parse_html(html_doc, cursor)
	if verbose:
		print_db(cursor, printable)
	prepare_clean_db(cursor, printable)
	if verbose:
		print_full_tops(cursor)
	delete_duplicate(cursor, printable)
	if duration:
		data = get_duration(cursor)
	if verbose:
		sys.stdout.close()
	gen_report(cursor, data)

main()