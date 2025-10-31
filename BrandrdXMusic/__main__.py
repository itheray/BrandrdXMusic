import asyncio
import importlib
import os
from sys import argv
from threading import Thread
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall
from flask import Flask

import config
from BrandrdXMusic import LOGGER, app, userbot
from BrandrdXMusic.core.call import Hotty
from BrandrdXMusic.misc import sudo
from BrandrdXMusic.plugins import ALL_MODULES
from BrandrdXMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

# --- UptimeRobot Web Server ---
web_app = Flask(__name__)

@web_app.route('/')
def hello_world():
    return 'Bot is alive!'

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)
# ------------------------------


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()
    
    # Start the web server in a separate thread
    LOGGER(__name__).info("Starting UptimeRobot web server...")
    web_thread = Thread(target=run_web_server)
    web_thread.daemon = True
    web_thread.start()
    
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("BrandrdXMusic.plugins" + all_module)
    LOGGER("BrandrdXMusic.plugins").info("Successfully Imported Modules...")
    await userbot.start()
    await Hotty.start()
    try:
        await Hotty.stream_call("https://graph.org/file/e999c40cb700e7c684b75.mp4")
    except NoActiveGroupCall:
        LOGGER("BrandrdXMusic").error(
            "Please turn on the videochat of your log group\channel.\n\nStopping Bot..."
        )
        exit()
    except:
        pass
    await Hotty.decorators()
    LOGGER("BrandrdXMusic").info(
        "ᴅʀᴏᴘ ʏᴏᴜʀ ɢɪʀʟꜰʀɪᴇɴᴅ'ꜱ ɴᴜᴍʙᴇʀ ᴀᴛ @BRANDED_PAID_CC ᴊᴏɪɴ @BRANDRD_BOT , @BRANDED_WORLD ꜰᴏʀ ᴀɴʏ ɪꜱꜱᴜᴇꜱ"
    )
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("BrandrdXMusic").info("Stopping Brandrd Music Bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
