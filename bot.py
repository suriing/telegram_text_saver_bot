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
tm_n = config.get('settings','tm_n')
tm_dest = config.get('settings','tm_dest')

def write_down(txt):
    doc_name = str(datetime.date.today()) + '.txt'
    with open(dest_dir + doc_name, 'a') as f:
        f.write(txt + '\n')

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    chat_ids = str(msg['chat']['id'])

    if content_type == 'text':
        command = msg['text']
        if chat_ids != chat_id:
            bot.sendMessage(chat_ids, 'PERMISSION DENIED')
            return
        if command[:5] == '/read':
            if len(command) == 5:
                doc_name = str(datetime.date.today()) + '.txt'
            else:
                doc_name = command[6:] + '.txt'
            if not os.path.isfile(dest_dir + doc_name):
                bot.sendMessage(chat_id, doc_name + ' is not exist. "/list" to get list. "/read TEXT_FILE_NAME" to read specific text file.')
                return
            ans = subprocess.check_output("cat " + dest_dir + doc_name, shell=True)
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
    elif content_type == 'document':
        f_id = msg['document']['file_id']
        f_name = msg['document']['file_name']
        f_type = msg['document']['mime_type']
        if f_type == "application/x-bittorrent":
            f_temp = os.path.join(os.path.dirname(os.path.abspath(__file__)),f_name)
            command = "transmission-remote -n '" + tm_n + "' -a " + f_temp + " -w " + tm_dest 
            bot.download_file(f_id, f_temp)
            risp = subprocess.check_output(command, shell=True)
            bot.sendMessage(chat_id, risp)
            subprocess.run("rm " + f_temp, shell=True)

bot = telepot.Bot(token)
bot.message_loop(handle)
print('Listening...')

while 1:
    time.sleep(10)

