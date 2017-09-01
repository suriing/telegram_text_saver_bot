import sys
import os
import time
import datetime
import configparser
import telepot
import subprocess

# configparser for token & chat_id
config = configparser.ConfigParser()
config.read(sys.argv[1])
token = config.get('settings','token')
chat_id = config.get('settings','chat_id')
dest_dir = config.get('settings','dest_dir')

def write_down(txt):
	doc_name = str(datetime.date.today()) + '.txt'
	with open(dest_dir + doc_name, 'a') as f:
		f.write(txt + '\n')

def handle(msg):
	chat_ids = str(msg['chat']['id'])
	command = msg['text']
	if chat_ids != chat_id:
		bot.sendMessage(chat_ids, 'PERMISSION DENIED')
		return
	if command[:5] == '/read':
		if len(command) == 5:
			doc_name = str(datetime.date.today()) + '.txt'
		else:
			doc_name = command[6:] + '.txt'
			if os.path.isfile(dest_dir + doc_name):
				ans = subprocess.check_output("cat " + dest_dir + doc_name, shell=True)
				bot.sendMessage(chat_id, ans)
			else:
				bot.sendMessage(chat_id, doc_name + ' is not exist')
	elif command == '/list':
		text_list = []
		for files in os.listdir(dest_dir):
			if files.endswith(".txt"):
				text_list.append(files[:-4])
		bot.sendMessage(chat_id,"\n".join(text_list))
	else:
		print('Command received: %s' % command)
		write_down(command)
		bot.sendMessage(chat_id, '\'' + command + '\'' + ' is saved')

bot = telepot.Bot(token)
bot.message_loop(handle)
print('Listening...')
bot.sendMessage(chat_id,'Server booted, text me to save!')

while 1:
    time.sleep(10)

