import sqlite3
import os


def fetch(img_id):

	conn = sqlite3.connect(r'data\GestVals.db')
	cursor = conn.cursor()

	cursor.execute(""" 

					SELECT * FROM savedir WHERE ID = (?)

		 			""", (img_id,))

	fetch_vals = cursor.fetchall()
	fetch_id, fetch_name, fetch_dir = fetch_vals[0][0], fetch_vals[0][1], fetch_vals[0][2]

	conn.close()

	return fetch_id, fetch_name, fetch_dir

def change(change_id, change_name, change_dir):

	conn = sqlite3.connect(r'data\GestVals.db')
	cursor = conn.cursor()


	cursor.execute(""" 

					UPDATE savedir SET Name = (?), Dir = (?) WHERE ID = (?)

	 				""", (change_name, change_dir, change_id))

	conn.commit()
	conn.close()

def edit_gest_fetch(img_id):

	conn = sqlite3.connect(r'data\GestVals.db')
	cursor = conn.cursor()

	cursor.execute(""" 

					SELECT * FROM savedir WHERE Name = (?)

		 			""", (img_id,))

	fetch_vals = cursor.fetchall()
	fetch_id, fetch_name, fetch_dir = fetch_vals[0][0], fetch_vals[0][1], fetch_vals[0][2]

	conn.close()

	return fetch_id, fetch_name, fetch_dir


def create():

	conn = sqlite3.connect(r'data\GestVals.db')
	cursor = conn.cursor()

	cursor.execute(""" 

					CREATE TABLE IF NOT EXISTS savedir (ID text NOT NULL, Name text NOT NULL, Dir text NOT NULL, PRIMARY KEY (ID))

	 				""")

	for item in os.listdir(r'data\\dp_img'):
		cursor.execute('''

						INSERT OR IGNORE INTO  savedir VALUES ((?), (?), 'Dir')

					''', (item, 'NA:'+item))

	conn.commit()
	conn.close()
