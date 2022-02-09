import subprocess
import time
import os


try:
	
	if os.path.exists(r'C:\Program Files\Mozilla Firefox\firefox.exe'):

		print('Opening ___')
		for i in range(5):
			print(i, end='\b')
			time.sleep(1)
		subprocess.run(r'C:\Program Files\Mozilla Firefox\firefox.exe')
	

except FileNotFoundError:
	print('Oopsie')