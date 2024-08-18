import os
from os import getenv

from dotenv import load_dotenv

load_dotenv()
API_ID = os.environ["API_ID"]
API_HASH = os.environ["API_HASH"]
SESSION = os.environ["SESSION"]
FEDBAN_API_KEY = os.environ["FEDBAN_API_KEY"]
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
MONGO_URL = os.environ["MONGO_URL"]
CMD_HANDLER = ["?"]
cohere_key = os.getenv("COHERE_KEY", "")
LOG_ID = os.getenv("LOG_ID", None)

AFK_CACHE = {}
BOT_CMD_INFO = {}
BOT_CMD_MENU = {}
BOT_HELP = {}
CMD_INFO = {}
CMD_MENU = {}
HELP_DICT = {}
TEMPLATES = {}

class ENV_TEMPLATE:
    airing_template = "AIRING_TEMPLATE"
    airpollution_template = "AIRPOLLUTION_TEMPLATE"
    alive_pic = "ALIVE_PIC"
    alive_template = "ALIVE_TEMPLATE"
    anilist_user_template = "ANILIST_USER_TEMPLATE"
    anime_template = "ANIME_TEMPLATE"
    btn_in_help = "BUTTONS_IN_HELP"
    character_template = "CHARACTER_TEMPLATE"
    chat_info_template = "CHAT_INFO_TEMPLATE"
    climate_api = "CLIMATE_API"
    climate_template = "CLIMATE_TEMPLATE"
    command_template = "COMMAND_TEMPLATE"
    currency_api = "CURRENCY_API"
    custom_pmpermit = "CUSTOM_PMPERMIT"
    gban_template = "GBAN_TEMPLATE"
    github_user_template = "GITHUB_USER_TEMPLATE"
    help_emoji = "HELP_EMOJI"
    help_template = "HELP_TEMPLATE"
    is_logger = "IS_LOGGER"
    lyrics_api = "LYRICS_API"
    manga_template = "MANGA_TEMPLATE"
    ocr_api = "OCR_API"
    ping_pic = "PING_PIC"
    ping_template = "PING_TEMPLATE"
    pm_logger = "PM_LOGGER"
    pm_max_spam = "PM_MAX_SPAM"
    pmpermit = "PMPERMIT"
    pmpermit_pic = "PMPERMIT_PIC"
    remove_bg_api = "REMOVE_BG_API"
    thumbnail_url = "THUMBNAIL_URL"
    statistics_template = "STATISTICS_TEMPLATE"
    sticker_packname = "STICKER_PACKNAME"
    tag_logger = "TAG_LOGGER"
    telegraph_account = "TELEGRAPH_ACCOUNT"
    time_zone = "TIME_ZONE"
    unload_plugins = "UNLOAD_PLUGINS"
    unsplash_api = "UNSPLASH_API"
    usage_template = "USAGE_TEMPLATE"
    user_info_template = "USER_INFO_TEMPLATE"

os_configs = [
    "API_HASH",
    "API_ID",
    "SESSION",
    "FEDBAN_API_KEY",
    "GOOGLE_API_KEY",
    "CMD_HANDLER",
    "cohere_key",
]
all_env: list[str] = [
    value for key, value in ENV_TEMPLATE.__dict__.items() if not key.startswith("__")
]
