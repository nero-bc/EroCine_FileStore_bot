# (c) github - @Rishikesh-Sharma09 ,telegram - https://telegram.me/Rk_botz
# removing credits doesn't make you coder 

from bot import Bot
from pyrogram import Client, filters, enums
from pyrogram.types import ChatJoinRequest
from database import db
from configs import Config
from plugins.send_file import send_media_and_reply

@Bot.on_chat_join_request()
async def join_reqs(client, message: ChatJoinRequest):
  if not await db.find_join_req(message.from_user.id, message.chat.id):
    await db.add_join_req(message.from_user.id, message.chat.id)
    file_id =  await db.get_file_id(message.from_user.id)
    GetMessage = await client.get_messages(chat_id=Config.DB_CHANNEL, message_ids=file_id)
    message_ids = []
    if GetMessage.text:        
        message_ids = GetMessage.text.split(" ")
        
    else:
        message_ids.append(int(GetMessage.id))
    for i in range(len(message_ids)):
        await send_media_and_reply(client, user_id=message.from_user.id, file_id=int(message_ids[i]))
    
    await db.delete_file_id(message.from_user.id)

@Bot.on_message(filters.command("delreq") & filters.private & filters.user(Config.BOT_OWNER))
async def del_requests(client, message):
    
    await db.del_join_req()    
    await message.reply("<b>⚙ ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ ᴄʜᴀɴɴᴇʟ ʟᴇғᴛ ᴜꜱᴇʀꜱ ᴅᴇʟᴇᴛᴇᴅ</b>")
