import asyncio
from configs import Config
from pyrogram import Client
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from pyrogram.errors import FloodWait
from plugins.helpers import str_to_b64


async def forward_to_channel(bot: Client, message: Message, editable: Message):
    try:
        __SENT = await message.forward(Config.DB_CHANNEL)
        return __SENT
    except FloodWait as sl:
        if sl.value > 45:
            await asyncio.sleep(sl.value)
            await bot.send_message(
                chat_id=int(Config.DB_CHANNEL),
                text=f"<b>#FloodWait:</b>\nGot FloodWait of `{str(sl.value)}s` from `{str(editable.chat.id)}` !!",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Ban User", callback_data=f"ban_user_{str(editable.chat.id)}")]
                    ]
                )
            )
        return await forward_to_channel(bot, message, editable)


async def save_batch_media_in_channel(bot: Client, editable: Message, message_ids: list, channel_id: int):
    try:
        message_ids_str = ""
        for message in (await bot.get_messages(chat_id=editable.chat.id, message_ids=message_ids)):
            sent_message = await forward_to_channel(bot, message, editable)
            if sent_message is None:
                continue
            message_ids_str += f"{str(sent_message.id)} "
            await asyncio.sleep(2)
        SaveMessage = await bot.send_message(
            chat_id=Config.DB_CHANNEL,
            text=message_ids_str,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Delete Batch", callback_data="closeMessage")
            ]])
        )
        share_link = f"https://t.me/{Config.BOT_USERNAME}?start=file-{str_to_b64(str(channel_id))}_{str_to_b64(str(SaveMessage.id))}"
        await editable.edit(
            f"<b>Batch Files Stored in my Database!</b>\n\nHere is the Permanent Link of your files: {share_link} \n\n"
            f"Just Click the link to get your files!",
            disable_web_page_preview=True
        )
        
    except Exception as err:
        await editable.edit(f"Something Went Wrong!\n\n<b>Error:</b> `{err}`")
        await bot.send_message(
            chat_id=int(Config.LOG_CHANNEL),
            text=f"<b>#ERROR_TRACEBACK:</b>\nGot Error from `{str(editable.chat.id)}` !!\n\n<b>Traceback:</b> `{err}`",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Ban User", callback_data=f"ban_user_{str(editable.chat.id)}")]
                ]
            )
        )

# @Rk_botz
async def save_media_in_channel(bot: Client, editable: Message, message: Message, channel_id: int):
    try:
        forwarded_msg = await message.forward(Config.DB_CHANNEL)
        file_er_id = str(forwarded_msg.id)
        share_link = f"https://t.me/{Config.BOT_USERNAME}?start=file-{str_to_b64(str(channel_id))}_{str_to_b64(file_er_id)}"
        await editable.edit(
            "<b>Your File Stored in my Database!</b>\n\n"
            f"Here is the Permanent Link of your file: {share_link} \n\n"
            "Just Click the link to get your file!",
            disable_web_page_preview=True
        )
    except FloodWait as sl:
        if sl.value > 45:
            print(f"Sleep of {sl.value}s caused by FloodWait ...")
            await asyncio.sleep(sl.value)
            await bot.send_message(
                chat_id=int(Config.DB_CHANNEL),
                text="<b>#FloodWait:</b>\n"
                     f"Got FloodWait of `{str(sl.value)}s` from `{str(editable.chat.id)}` !!",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Ban User", callback_data=f"ban_user_{str(editable.chat.id)}")]
                    ]
                )
            )
        await save_media_in_channel(bot, editable, message)
    except Exception as err:
        await editable.edit(f"Something Went Wrong!\n\n<b>Error:</b> `{err}`")
        await bot.send_message(
            chat_id=int(Config.DB_CHANNEL),
            text="<b>#ERROR_TRACEBACK:</b>\n"
                 f"Got Error from `{str(editable.chat.id)}` !!\n\n"
                 f"<b>Traceback:</b> `{err}`",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Ban User", callback_data=f"ban_user_{str(editable.chat.id)}")]
                ]
            )
        )         
