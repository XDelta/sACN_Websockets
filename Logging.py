from os.path import dirname, join
from datetime import datetime

log_file = open(join(dirname(__file__), 'sacn-wss.log'), mode='a+', encoding='utf-8', errors='ignore', buffering=1)

class Logging(object):

	def log(self, text):
		log_text = datetime.now().strftime("%m/%d/%y - %H:%M:%S")
		con = datetime.now().strftime("%H:%M:%S") #console doesn't need day
		log_file.write("["+log_text+"] "+text+'\n')
		print("["+con+"] "+text)

	def closeLog(self):
		log_file.close()

wssl = Logging()
