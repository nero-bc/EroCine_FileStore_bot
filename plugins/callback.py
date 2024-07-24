# (c) github - @Rishikesh-Sharma09 ,telegram - https://telegram.me/Rk_botz
# removing credits don't make you coder 
import traceback 
from pyrogram import __version__
from bot import Bot
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import asyncio
from pyrogram.errors import UserAdminInvalid, PeerIdInvalid, FloodWait, UserIsBlocked, InputUserDeactivated
from plugins.save_media import ( 
     save_media_in_channel, 
     save_batch_media_in_channel 
 )

MediaList = {}

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    try:
        if data == "about":
            await query.message.edit_text(
                text = f"<b>I am your friend ❤️</b>",
                disable_web_page_preview = True,
                reply_markup = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔒 Close", callback_data = "close")
                        ]
                    ]
                )
            )
        elif data == "close":
            await query.message.delete()
            try:
                await query.message.reply_to_message.delete()
            except Exception as e:
                print(f"Error deleting reply_to_message: {e}")
                
        elif data == "help":
            await query.message.edit_text(
                text=HELP_MESSAGE,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔒 Close", callback_data="close")
                        ]
                    ]
                )
            )
        elif data == "developer_info":
            await query.message.edit_text(
                text = f"<b>○ Creator : Rishikesh sharma </a>\n○ Language : <code>Python3</code>\n○ Library : <a href='https://docs.pyrogram.org/'>Pyrogram asyncio {__version__}</a>\n○ My Owner : @HellooBrro</b>",
                disable_web_page_preview = True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔒 Close", callback_data="close")
                        ]
                    ]
                )
            )
        elif data.startswith("addToBatchTrue"):
            ident, channel_id = data.split("#")
            if MediaList.get(f"{str(query.from_user.id)}", None) is None:
                MediaList[f"{str(query.from_user.id)}"] = []
            file_id = query.message.reply_to_message.id
            MediaList[f"{str(query.from_user.id)}"].append(file_id)
            await query.message.edit_text("File Saved in Batch!\n\n"
                                          "Press below button to get batch link.",
                                          reply_markup=InlineKeyboardMarkup([
                                              [InlineKeyboardButton("Get Batch Link", callback_data=f"getBatchLink#{channel_id}")],
                                              [InlineKeyboardButton("Close Message", callback_data="closeMessage")]
                                          ]))
        elif data.startswith("addToBatchFalse"):
            ident, channel_id = data.split("#")
            await save_media_in_channel(client, editable=query.message, message=query.message.reply_to_message, channel_id=channel_id)

        elif data.startswith("getBatchLink"):
            ident, channel_id = data.split("#")
            message_ids = MediaList.get(f"{str(query.from_user.id)}", None)
            if message_ids is None:
                await query.answer("Batch List Empty!", show_alert=True)
                return
            await query.message.edit_text("Please wait, generating batch link ...")
            await save_batch_media_in_channel(bot=client, editable=query.message, message_ids=message_ids, channel_id=channel_id)
            MediaList[f"{str(query.from_user.id)}"] = []

        elif data.startswith("savefile"):
            ident, channel_id = data.split("#")
            await query.message.edit_text(
                text="<b>Choose an option from below:</b>",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Save in Batch", callback_data=f"addToBatchTrue#{channel_id}")],
                    [InlineKeyboardButton("Get Sharable Link", callback_data=f"addToBatchFalse#{channel_id}")]
                ]),
                disable_web_page_preview=True
            )
    except UserAdminInvalid:
        print("Error: Bot lacks sufficient admin rights.")
    except PeerIdInvalid:
        print("Error: Invalid peer ID.")
    except FloodWait as e:
        print(f"Error: Flood wait of {e.x} seconds.")
        await asyncio.sleep(e.x)
    except UserIsBlocked:
        print("Error: User has blocked the bot.")
    except InputUserDeactivated:
        print("Error: User is deactivated.")
    except Exception:
        print(traceback.format_exc())
