import os
import sys
import asyncio
import logging
from pyrogram import Client as AFK, idle, filters
from pyrogram.types import Message
from tglogging import TelegramLogHandler
from pyromod import listen
import tgcrypto

# ------------------------ Config ------------------------ #
class Config(object):
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7999745479:AAGz1M3bLDt5Ci7_fnMqJ-uKmK1Hr4xLTuE")
    API_ID = int(os.environ.get("API_ID", "27660379"))
    API_HASH = os.environ.get("API_HASH", "19c71c27733f0954371085198855125a")
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    SESSIONS = "./SESSIONS"

    AUTH_USERS = list(map(int, os.environ.get('AUTH_USERS', '5459854363').split(',')))
    GROUPS = list(map(int, os.environ.get('GROUPS', '-1002761572365').split(',')))

    LOG_CH = int(os.environ.get("LOG_CH", "-1002761572365"))

# ------------------------ Logger ------------------------ #
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        TelegramLogHandler(
            token=Config.BOT_TOKEN,
            log_chat_id=Config.LOG_CH,
            update_interval=2,
            minimum_lines=1,
            pending_logs=200000),
        logging.StreamHandler()
    ]
)
LOGGER = logging.getLogger(__name__)
LOGGER.info("✅ Live log streaming enabled.")

# ------------------------ Store ------------------------ #
class Store(object):
    CPTOKEN = "your_token_here"
    SPROUT_URL = "https://discuss.oliveboard.in/"
    ADDA_TOKEN = ""
    THUMB_URL = "https://telegra.ph/file/84870d6d89b893e59c5f0.jpg"

# ------------------------ Messages ------------------------ #
class Msg(object):
    START_MSG = "**/pro**"
    TXT_MSG = "Hey <b>{user},\n\n`I'm Multi-Talented Robot. I Can Download Many Type of Links.`\n\nSend a TXT or HTML file :-</b>"
    ERROR_MSG = "<b>DL Failed ({no_of_files}) :-</b> \n\n<b>Name: </b>{file_name},\n<b>Link:</b> `{file_link}`\n\n<b>Error:</b> {error}"
    SHOW_MSG = "<b>Downloading :- \n`{file_name}`\n\nLink :- `{file_link}`</b>"
    CMD_MSG_1 = "`{txt}`\n\n**Total Links in File are :-** {no_of_links}\n\n**Send any Index From `[ 1 - {no_of_links} ]` :-**"
    CMD_MSG_2 = "<b>Uploading :- </b> `{file_name}`"
    RESTART_MSG = "✅ HI Bhai log\n✅ PATH CLEARED"

# ------------------------ Prefixes ------------------------ #
prefixes = ["/", "~", "?", "!", "."]

# ------------------------ Client ------------------------ #
plugins = dict(root="plugins")

if __name__ == "__main__":
    if not os.path.exists(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)
    if not os.path.exists(Config.SESSIONS):
        os.makedirs(Config.SESSIONS)

    PRO = AFK(
        "AFK-DL",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        sleep_threshold=120,
        plugins=plugins,
        workdir=Config.SESSIONS,
        workers=2,
    )

    # ------------------------ /stop Command ------------------------ #
    @PRO.on_message(
        (filters.chat(Config.GROUPS) | filters.chat(Config.AUTH_USERS)) &
        filters.command("stop", prefixes=prefixes)
    )
    async def stop_command(bot: AFK, m: Message):
        await m.reply_text("🛑 Bot stopped by admin.")
        LOGGER.warning(f"Bot stopped by user {m.from_user.id}")
        await bot.stop()
        sys.exit(0)

    # ------------------------ Start Bot ------------------------ #
    chat_id = list(set(Config.GROUPS + Config.AUTH_USERS))

    async def main():
        await PRO.start()
        bot_info = await PRO.get_me()
        LOGGER.info(f"<--- @{bot_info.username} Started --->")

        for i in chat_id:
            try:
                await PRO.send_message(chat_id=i, text="**Bot Started! ♾ /pro **")
            except Exception as e:
                LOGGER.warning(f"Couldn't send start message to {i}: {e}")
                continue
        await idle()

    asyncio.get_event_loop().run_until_complete(main())
    LOGGER.info(f"<--- Bot Stopped --->")
