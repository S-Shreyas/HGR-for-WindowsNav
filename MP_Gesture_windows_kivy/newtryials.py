import sqlite3
import os
import string

print('{', end=' ')
num = 1000


for letter in string.ascii_uppercase:
	
	if letter == 'J' or letter == 'Z':
		pass
	else:
		print("'" + letter + "'" + ':' + "'" + str(num) + '.png' + "'" + ',', end=' ')
		num += 1

print('}')