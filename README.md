Simple python telegram bot based on Telepot library to save text message to server. 
No need to set port-forwardings, no custom signed certificates, no webhooks, no bullshit.

# You'll need to run bot.py:

- Python interpreter, on debian: "sudo apt-get python3".
- Telepot library, on debian with python installed: "sudo pip install telepot".
- Telegram bot token, obtainable via @BotFather chat, write it at the 'settings.txt'.
- Personal chatid, write it at the 'settings.txt'.
- Text file destination directory, write it at the 'settings.txt'.
- Photo file destination directory, write it at the 'settings.txt'. 
- Transmission remote ID and password, write it at the 'settings.txt'. 
- Transmission download destination, write it at the 'settings.txt'.

To enable bot to comunicate with you ( due to telegram security policy, anti-spam etc...), 
you need to chat first by opening bot chat and sending "/start", enough to unlock bot direct messaging without human interaction.

# To run bot

- **$ python3 bot.py settings.txt [&]** 
- (to give bot root access) **$ sudo python3 bot.py settings.txt [&]**
- [&] is for background process

# Usage

- msg
  - with out below commands, every message will be wrote in 'dest_dir/YYYY-MM-DD.txt'
  - /list : return text file name of your destination directory
  - /read [text name] : return contents of text file. without [text name], it will return YYYY-MM-DD.txt(today)
- photo
  - to save photo to your server, send it to bot.
- document
  - torrent
    - to download torrent contents to your server, send it to bot with text (MOV or TV).
  - smi/srt
    - to save smi/srt to your server, send it to bot.

The bot is configured to reply only to your chatid (in yor chat) for security reasons, 
ever use spaces to indentate or you'll get execution errors, use tabs instead.
