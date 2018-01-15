#!/usr/bin/python3

import sys
import os
import time
import datetime
import subprocess
from urllib.parse import unquote
from pprint import pprint
import telepot
import configparser

# Set variables
config = configparser.ConfigParser()
config.read(sys.argv[1])
token = config.get('settings','token')
chat_id = config.get('settings','chat_id')
dest_dir = config.get('settings','dest_dir')
tm_n = config.get('settings','tm_n')
tm_mov = config.get('settings','tm_mov')
tm_tv = config.get('settings','tm_tv')
tm_temp = config.get('settings','tm_temp')
tm_mode = ""

# Define sub functions
def photo_handler(msg, chat_id):
    pho_id = msg['photo'][-1]['file_id']
    pho_dest = os.path.join('/media/pi/ex500/Pictures', str(msg['date']) + '.jpg')
    bot.download_file(pho_id, pho_dest)
    bot.sendMessage(chat_id,"Photo is saved as\n" + pho_dest) 

def doc_handler(msg, chat_id):
    global tm_mode
    f_id, f_name, f_type = msg['document']['file_id'], msg['document']['file_name'], msg['document']['mime_type'] 
    print(" ")
    for ele in [f_id, f_name, f_type]:
        print(ele)
    if f_type == "application/x-bittorrent":
        if tm_mode == "":
            return bot.sendMessage(chat_id,"PLEASE SEND TORRENT FILE WITH\n'TV' or 'MOV'") 
        if tm_mode == "mov":
            tm_dir = tm_mov
        elif tm_mode == "tv":
            tm_dir = tm_tv
        elif tm_mode == "temp":
            tm_dir = tm_temp
        f_temp = os.path.join(os.path.dirname(os.path.abspath(__file__)),f_name)
        command = "transmission-remote -n '" + tm_n + "' -a " + f_temp + " -w " + tm_dir 
        bot.download_file(f_id, f_temp)
        risp = subprocess.check_output(command, shell=True)
        bot.sendMessage(chat_id, risp)
        subprocess.run("rm " + f_temp, shell=True)
        tm_mode = ""
    elif f_type == "application/octet-stream":
        f_ext = os.path.splitext(f_name)[1]
        if f_ext == '.smi' or f_ext == '.srt':
            f_dest = os.path.join(tm_mov, unquote(f_name))
            bot.download_file(f_id, f_dest)
            bot.sendMessage(chat_id,"Sub file is saved as\n" + f_dest) 

def text_handler(msg, chat_id):
    global tm_mode
    m_text = msg['text'].lower()
    if m_text == "mov":
        tm_mode = "mov"
    elif m_text == "tv":
        tm_mode = "tv"
    else:
        tm_mode = ""
        chat_ids = msg['chat']['id']
        command = msg['text']
        if chat_ids != chat_id:
            bot.sendMessage(chat_ids, 'PERMISSION DENIED')
            return
        if command[:5] == '/read':
            if len(command) == 5:
                doc_name = str(datetime.date.today()) + '.txt'
            else:
                doc_name = command[6:] + '.txt'
            if not os.path.isfile(os.path.join(dest_dir,doc_name)):
                bot.sendMessage(chat_id, doc_name + ' is not exist. "/list" to get list. "/read TEXT_FILE_NAME" to read specific text file.')
                return
            ans = subprocess.check_output("cat " + os.path.join(dest_dir, doc_name), shell=True)
            bot.sendMessage(chat_id, ans)
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

def write_down(txt):
    doc_name = str(datetime.date.today()) + '.txt'
    with open(os.path.join(dest_dir,doc_name), 'a') as f:
        f.write(txt + '\n')

# Define main function
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        return text_handler(msg, chat_id)

    elif content_type == 'document':
        return doc_handler(msg, chat_id)

    elif content_type == 'photo':
        return photo_handler(msg, chat_id)

# Run bot
bot = telepot.Bot(token)
bot.message_loop(handle)
print('Listening...')

while 1:
    time.sleep(10)

