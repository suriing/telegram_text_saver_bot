import sys
import os
import time
import random
import datetime
import subprocess
import configparser
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

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
	chat_ids = msg['chat']['id']
	command = msg['text']
	print('Command received: %s' % command)
	write_down(command)
	bot.sendMessage(chat_id, '\'' + command + '\'' + ' is saved')

bot = telepot.Bot(token)
bot.message_loop(handle)
print('Listening...')
bot.sendMessage(chat_id,'Server booted, text me to save!')

while 1:
    time.sleep(10)

