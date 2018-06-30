#!/usr/local/bin/python

import sys
import os
import time
import datetime
import subprocess
from urllib import unquote
from pprint import pprint
import telepot
import ConfigParser

# Set variables
config = ConfigParser.ConfigParser()
config.read(sys.argv[1])
token = config.get('settings','token')
chat_ids = int(config.get('settings','chat_id'))
dest_dir = config.get('settings','dest_dir')
tm_d1 = config.get('settings','tm_d1')
tm_d2 = config.get('settings','tm_d2')
tm_dt1 = config.get('settings','tm_dt1')
kw_d1 = config.get('settings','kw_d1')
kw_d2 = config.get('settings','kw_d2')
kw_dt1 = config.get('settings','kw_dt1')
dic_tm = {kw_d1:tm_d1, kw_d2:tm_d2, kw_dt1:tm_dt1}
tm_mode = ""

# Define sub functions
def photo_handler(msg, chat_id):
    pho_id = msg['photo'][-1]['file_id']
    pho_dest = os.path.join('/volume1/PhotoGallery', str(msg['date']) + '.jpg')
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
            return bot.sendMessage(chat_id,"PLEASE SEND TORRENT FILE WITH\n'" + kw_d1.upper() + "' or '" + kw_d2.upper() + "'") 
        elif tm_mode in dic_tm:
            tm_dir = dic_tm.get(tm_mode)
            f_temp = os.path.join(os.path.dirname(os.path.abspath(__file__)),f_name)
            command = 'deluge-console "add -p ' + tm_dir + ' ' + f_temp + '"' 
            bot.download_file(f_id, f_temp)
            risp = subprocess.check_output(command, shell=True)
            bot.sendMessage(chat_id, risp)
            subprocess.call("rm '" + f_temp + "'", shell=True)
        tm_mode = ""
    elif f_type == "application/octet-stream":
        f_ext = os.path.splitext(f_name)[1]
        if f_ext == '.smi' or f_ext == '.srt':
            f_dest = os.path.join(tm_d1, unquote(f_name))
            bot.download_file(f_id, f_dest)
            bot.sendMessage(chat_id,"Sub file is saved as\n" + f_dest) 

def text_handler(msg, chat_id):
    global tm_mode
    m_text = msg['text'].lower()
    if m_text in dic_tm:
        tm_mode = m_text
    else:
        command = msg['text']
        tm_mode = ""
        if command[:5] == '/read':
            if len(command) == 5:
                doc_name = datetime.date.today().strftime("%Y_%m_%d") + '.txt'
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
                    text_list.append('/read_' + files[:-4])
            bot.sendMessage(chat_id,"\n".join(text_list))
        else:
            print('Command received: %s' % command)
            write_down(command)
            bot.sendMessage(chat_id, '\'' + command + '\'' + ' is saved')

def write_down(txt):
    doc_name = datetime.date.today().strftime("%Y_%m_%d") + '.txt'
    with open(os.path.join(dest_dir,doc_name), 'a') as f:
        f.write(txt + '\n')

# Define main function
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if chat_ids != chat_id:
        bot.sendMessage(chat_ids, 'PERMISSION DENIED')
        return

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

