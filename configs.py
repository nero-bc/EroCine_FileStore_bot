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
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7273754371:AAFfZV3Y0IMkBObAlq51KzfE8OwUu4YSdFw")
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "Filestore1_bot")
    DB_CHANNEL = int(os.environ.get("DB_CHANNEL", "-1002229157684"))
    BOT_OWNER = int(os.environ.get("BOT_OWNER", "2145003945"))
    DATABASE_URL = os.environ.get("DATABASE_URL", "mongodb+srv://anujkumarverma175:Akv2@cluster0.nk3nexm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    DATABASE_NAME = os.environ.get("DATABASE_NAME", "FilmCity_English")
    #UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "-1001848348787")
    #LOG_CHANNEL = os.environ.get("LOG_CHANNEL", "-1001799594060")
    CAPTION = os.environ.get("CAPTION", "{file_caption}")
    PROTECT_CONTENT = os.environ.get("PROTECT_CONTENT", "False")
    FROM_CHANNEL = int(os.environ.get("FROM_CHANNEL", "-1001994745210"))
    TOO_CHANNEL = int(os.environ.get("TOO_CHANNEL", "-1002091445087"))
    START_MSG = os.environ.get("START_MESSAGE", "<b>ʜᴇʟʟᴏ , {first} 🤗\n\nɪ ᴀᴍ ᴛʜᴇ Cʜᴀɴɴᴇʟ ғɪʟᴇ-sᴛᴏʀᴇ ʙᴏᴛ. 😊\n\nᴍᴀᴅᴇ ʙʏ ♥️ ʙʏ Rishikesh Sharma</b>")    
    FORCE_CHANNEL = int(os.environ.get("FORCE_CHANNEL", "-1002028982032"))
    TIME_TO_WAIT = int(os.environ.get("TIME_TO_WAIT", "3600"))
