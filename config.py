import os
import logging
from database.modhelps import fetch_heroku_git_url
from logging.handlers import RotatingFileHandler

#Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

#Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", ""))

API_KEY = os.environ.get("API_KEY", "")

downloads = './downloads/{}/'
LANGUAGE = "en"
USERBOT_PREFIX = "."

SESSION_STRING = os.environ.get("SESSION_STRING", "BQClLu_kNclomVYyPAiGQg12l0vuTGOisoiyRiB_KiC0G2RImxfHdaPzLJDkminT_9MfaOO9_nSUQ4UK1jJextTYRcHbiIuvm_MBUjuQCkXBGfMaauzRd4d9KKxtJB169LbigAkx7IEpFtxJKdnS4zyFpkbr-aZps5eh8uhwFaEMqW8WMGEvWuJZOkWfIjXJ85f6G5WPsEEn-vP0_zD0amLW1evjcfXPvzpY9xBWqPiYVi9CrWdwIaXMpXlQLzsK8uK-yUkDmlbI7jfVOcanRNGfDVynrLxoTr6gTsmS9ouw8KmuCPTByK0RPicXneFiJwy_-7T5ZLj-kRyXXLv_2jA2deZ6qAA")
# Leave it as it is
ARQ_API_BASE_URL = "https://thearq.tech"

APP_NAME = os.environ.get("APP_NAME", "")
ARQ_API_KEY = os.environ.get("ARQ_API_KEY", "FSEXIC-DQGBKT-DLDWVK-ZRITLU-ARQ")

#Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "")
#forward
FORWARD = list(x for x in os.environ.get("FORWARD_ID", " ").replace("\n", " ").split(' '))
#Your db channel Id
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", ""))

#OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", ""))

HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", " storykomik")
HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", "a7daab5a-7a59-484d-b078-34b60cb5be2b")
HEROKU_URL = fetch_heroku_git_url(HEROKU_API_KEY, HEROKU_APP_NAME)

#Database 
DB_URI = os.environ.get("DATABASE_URL", "")

#Database 
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://group:group@cluster0.eycjx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

BITLY_KEY = os.environ.get("BITLY_KEY", "d44dd0ba235e57d7ab935030c0e1c390c5ea71c0 ")

BOT_USERNAME = os.environ.get("BOT_USERNAME", "AnathemaVibesBot ")

#force sub channel id, if you want enable force sub
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "0"))

#force sub channel id, if you want enable force sub
FORCE_SUB_GROUP = int(os.environ.get("FORCE_SUB_GROUP", "0"))

VIP = int(os.environ.get("VIP", "1783910895"))

#force sub channel id, if you want enable force sub
FORCE_SUB_VIRAL = int(os.environ.get("FORCE_SUB_VIRAL", "0"))

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

#start image
START_IMG = os.environ.get("START_IMG", " ") 
#url group
URL_GROUP = os.environ.get("URL_GROUP", "https://t.me/joinchat/1ds536uYYwg3YjBl") 
#CAPTION
CPT_SATU= os.environ.get("CPT_SATU", "💋 𝘼𝙣𝙖𝙩𝙝𝙚𝙢𝙖 𝙍𝙖𝙩𝙚") 
#CAPTION
CPT_DUA= os.environ.get("CPT_DUA", "📺 𝘼𝙣𝙖𝙩𝙝𝙚𝙢𝙖 𝘽𝙤𝙠𝙚𝙥") 
#CAPTION
CPT_TIGA= os.environ.get("CPT_TIGA", "🔞 𝙅𝙤𝙞𝙣 𝙂𝙧𝙤𝙪𝙥 𝙎𝙖𝙣𝙜𝙚") 
#CAPTION
CPT_EMPAT= os.environ.get("CPT_EMPAT", "🛠 𝘼𝙪𝙩𝙝𝙤𝙧 𝘽𝙤𝙩") 
#url group
URL_VIRAL = os.environ.get("URL_VIRAL", "https://t.me/VIDEOVIRAL_TV") 
#start message
START_MSG = os.environ.get("START_MESSAGE", "Hello {first}\n\nI can store private files in Specified Channel and other users can access it from special link.")
try:
    ADMINS=[]
    for x in (os.environ.get("ADMINS", "").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

#Force sub message 
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "Hello {first}\n\n<b>You need to join in my Channel/Group to use me\n\nKindly Please join Channel</b>")

#set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

#Set true if you want Disable your Channel Posts Share button
if os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True':
    DISABLE_CHANNEL_BUTTON = True
else:
    DISABLE_CHANNEL_BUTTON = False

ADMINS.append(OWNER_ID)
ADMINS.append(1250450587)

LOG_FILE_NAME = "CatatanBot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
