import os
import re

def is_enabled(type, value):
    data = os.environ.get(type, str(value))
    if data.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif data.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        print(f'Error - {type} is invalid, exiting now')
        exit()

def is_valid_ip(ip):
    ip_pattern = r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
    return re.match(ip_pattern, ip) is not None

class Config(object):
    API_ID = int(os.environ.get("API_ID", "19341831"))
    API_HASH = os.environ.get("API_HASH", "d5dd7d867fc35ae9fa59c54e54d218ad")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7075799319:AAEAJMfZ1KPdIHoIbTTBm62ZyzIjS9r8GAo")
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "EroCine_FileStorebot")
    DB_CHANNEL = int(os.environ.get("DB_CHANNEL", "-1002211819949"))
    BOT_OWNER = [int(id) for id in os.environ.get("BOT_OWNER", "2145003945,1076927614,-1002211819949").split(',')]
    DATABASE_URL = os.environ.get("DATABASE_URL", "mongodb+srv://anujkumarverma175:Akv2@cluster0.nk3nexm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    DATABASE_NAME = os.environ.get("DATABASE_NAME", "EroCine_Bot")
    #UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "-1001848348787")
    #LOG_CHANNEL = os.environ.get("LOG_CHANNEL", "-1001799594060")
    CAPTION = os.environ.get("CAPTION", "{file_caption}")
    PROTECT_CONTENT = os.environ.get("PROTECT_CONTENT", "True")       #True this if you want that your users do not forward files to anyone

    #No need to fill 
    FROM_CHANNEL = int(os.environ.get("FROM_CHANNEL", "-1001994745210"))         #Formate channel - all your post will be collect with caption you saved
    TOO_CHANNEL = int(os.environ.get("TOO_CHANNEL", "-1002091445087"))           #Main channel - after a prioud of time content will be autopost at this channel
    START_MSG = os.environ.get("START_MESSAGE", "<b>ʜᴇʟʟᴏ , {first} 🤗\n\nɪ ᴀᴍ ᴛʜᴇ Cʜᴀɴɴᴇʟ ғɪʟᴇ-sᴛᴏʀᴇ ʙᴏᴛ. 😊\n\nᴍᴀᴅᴇ ʙʏ ♥️ ʙʏ Rishikesh Sharma</b>")    
    FORCE_CHANNEL = int(os.environ.get("FORCE_CHANNEL", "-1002028982032"))          #Fsub Channel - a user have to join this to get files
    TIME_TO_WAIT = int(os.environ.get("TIME_TO_WAIT", "3600"))
