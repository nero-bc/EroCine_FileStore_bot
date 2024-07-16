import asyncio
from configs import Config
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from plugins.helpers import str_to_b64


async def reply_forward(message: Message, file_id: int):
    try:
        await message.reply_text(
            f"<b>This message will be Deleted After 10 min ⏰</b>\n",
            disable_web_page_preview=True, quote=True)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await reply_forward(message, file_id)
    except Exception as ex:
        print(f"An error occurred while replying: {ex}")


async def media_forward(bot: Client, user_id: int, file_id: int):
    try:
        return await bot.copy_message(chat_id=user_id, from_chat_id=Config.DB_CHANNEL,
                                      message_id=file_id)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return media_forward(bot, user_id, file_id)
    except Exception as ex:
        print(f"An error occurred while forwarding media: {ex}")



async def send_media_and_reply(bot: Client, user_id: int, file_id: int):
    sent_message = await media_forward(bot, user_id, file_id)
    await reply_forward(message=sent_message, file_id=file_id)
    asyncio.create_task(delete_after_delay(sent_message, 1800))

async def delete_after_delay(message, delay):
    await asyncio.sleep(delay)
    await message.delete()
