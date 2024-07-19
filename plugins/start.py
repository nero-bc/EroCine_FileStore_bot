import traceback
from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant, FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from bot import Bot
from database import db
from configs import Config
from plugins.helpers import b64_to_str, str_to_b64
from plugins.send_file import send_media_and_reply
import asyncio
from pyrogram import enums
from plugins.save_media import ( 
     save_media_in_channel, 
     save_batch_media_in_channel 
 )

async def is_req_subscribed(bot, query, FORCE_CHANNEL):
    if await db.find_join_req(query.from_user.id, FORCE_CHANNEL):
        return True
    try:
        user = await bot.get_chat_member(FORCE_CHANNEL, query.from_user.id)
    except UserNotParticipant:
        pass
    except Exception:
        print(traceback.format_exc())
    else:
        if user.status != enums.ChatMemberStatus.BANNED:
            return True
    return False



             

@Bot.on_message(filters.command("start"))
async def start_command_handler(client, message):    
    usr_cmd = message.text.split("_", 1)[-1]
    if usr_cmd == "/start":
        id = message.from_user.id
        user = message.from_user
        if not await db.present_user(id):
            try:
                await db.add_user(id)
            except:
                pass
        reply_markup = InlineKeyboardMarkup(            
            [
                [
                    InlineKeyboardButton("😊 About Me", callback_data="about"),
                    InlineKeyboardButton("💻 Developer Info", callback_data="developer_info")                
                ],
                [
                    InlineKeyboardButton("🔒 Close", callback_data="close")
                ]                 
            ]
        )
        await message.reply_text(
            text=Config.START_MSG.format(            
                first=user.first_name,
                last=user.last_name,
                username=user.mention if not user.username else '@' + user.username,
                id=user.id
            ),
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            quote=True
        )
    else:
        try:
            try:
                channel_id = (b64_to_str(message.text.split('file-')[1].split('_')[0]))
            except:
                channel_id = Config.FORCE_CHANNEL
            try:
                channels_cursor = await db.get_channels()
                channels = await channels_cursor.to_list(length=None)
                for channel in channels:
                     if channel['id'] == channel_id:
                     
                         print(f"channel id : {channel_id}")                
                         FORCE_CHANNEL = int(f"{channel['fsub_id']}")
                         print(f"channel id : {channel_id} | FORCE_CHANNEL : {FORCE_CHANNEL}")
                         if not await is_req_subscribed(client, message, FORCE_CHANNEL):
                             channelz_id = message.text.split('file-')[1].split('_')[0]
                             filez_id = usr_cmd.split("_")[-1]
                             try:
                                 file_id = int(b64_to_str(usr_cmd).split("_")[-1])
                             except (Error, UnicodeDecodeError):
                                 file_id = int(usr_cmd.split("_")[-1])
                             file_id_saved =  await db.get_file_id(message.from_user.id)
                             if file_id_saved:
                                  try:                                       
                                       await db.delete_file_id(message.from_user.id)
                                  except:        
                                       pass                                       
                             else:
                                  await db.save_file_id(message.from_user.id, file_id)        
                             try:
                                 invite_link = await client.create_chat_invite_link(FORCE_CHANNEL, creates_join_request=True)
                             except Exception:
                                 print(traceback.format_exc())
                                 invite_link = None  # Handling case where invite link creation fails
                             if invite_link:
                                 btn = [
                                      [                                           
                                           InlineKeyboardButton("⛔️ ᴊᴏɪɴ ɴᴏᴡ ⛔️", url=invite_link.invite_link)
                                      ],
                                      [
                                           InlineKeyboardButton("Try again", url=f"https://t.me/{Config.BOT_USERNAME}?start=file-{channelz_id}_{filez_id}")
                                      ]
                                 ]
                                 await client.send_message(
                                     chat_id=message.from_user.id,
                                     text="<b>🙁 ғɪʀꜱᴛ ᴊᴏɪɴ ᴏᴜʀ ʙᴀᴄᴋᴜᴘ ᴄʜᴀɴɴᴇʟ ᴛʜᴇɴ ʏᴏᴜ ᴡɪʟʟ ɢᴇᴛ ᴍᴏᴠɪᴇ, ᴏᴛʜᴇʀᴡɪꜱᴇ ʏᴏᴜ ᴡɪʟʟ ɴᴏᴛ ɢᴇᴛ ɪᴛ.\n\nफाइल प्राप्त करने के लिए पहले Join request भेजें । \n\nᴄʟɪᴄᴋ ᴊᴏɪɴ ɴᴏᴡ ʙᴜᴛᴛᴏɴ 👇</b>",
                                     reply_markup=InlineKeyboardMarkup(btn)                    
                                 )
                                 return 
                     else:
                         pass
                                                     
            except Exception:
                print(traceback.format_exc())
        except Exception:
            print(traceback.format_exc())
        try:
            try:
                file_id = int(b64_to_str(usr_cmd).split("_")[-1])
            except (Error, UnicodeDecodeError):
                file_id = int(usr_cmd.split("_")[-1])
            GetMessage = await client.get_messages(chat_id=Config.DB_CHANNEL, message_ids=file_id)
            message_ids = []
            if GetMessage.text:
                message_ids = GetMessage.text.split(" ")
                _response_msg = await message.reply_text(
                    text=f"<b>Total Files: {len(message_ids)}</b>",
                    quote=True,
                    disable_web_page_preview=True
                )
            else:
                message_ids.append(int(GetMessage.id))
            for i in range(len(message_ids)):
                await send_media_and_reply(client, user_id=message.from_user.id, file_id=int(message_ids[i]))
        except Exception as err:
            await message.reply_text(f"<b>Something went wrong!\n\n**Error:</b> {err}")

@Bot.on_message((filters.document | filters.video | filters.audio | filters.photo) & ~filters.chat(Config.DB_CHANNEL) & filters.user(Config.BOT_OWNER))
async def main(bot, message): 

    if message.chat.type == enums.ChatType.PRIVATE:   
        channels_cursor = await db.get_channels()
        channels = await channels_cursor.to_list(length=None)
        
        print(f"{channels}")
        btn = [
             [
                  InlineKeyboardButton(
                       text=f"{channel['name']}", callback_data=f"savefile#{channel['id']}"
                  )                       
             ]
             for channel in channels
        ]
        
        try:
            keyboard = InlineKeyboardMarkup(btn)
            await bot.send_message(
                 chat_id=message.chat.id,
                 text="<b>Choose a channel from below to force subscribe:</b>",
                 reply_to_message_id=message.id,
                 reply_markup=keyboard
            )
        except Exception as e:
            await message.reply_text("Please /save_channel post_channel_id its_forcesubid")

        
    

@Bot.on_message(filters.chat(Config.FROM_CHANNEL))
async def new_post(client, message):
    await db.save_post_ids(message.chat.id, [str(message.id)])        
    

@Bot.on_message(filters.chat(Config.DB_CHANNEL))
async def add_button(client, message):
    if message.photo:
        link = f"https://t.me/{Config.BOT_USERNAME}?start=post_{str_to_b64(str(message.id))}"
        caption = f"<b>📱 𝐖𝐚𝐭𝐜𝐡 𝐎𝐧𝐥𝐢𝐧𝐞 👨‍💻\n\n<a href={link}>Click To Watch\nFull-Video On Next Page</a>\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬</b>"
        try:
            kk = await message.copy(chat_id=Config.FROM_CHANNEL, caption=caption)
            await new_post(client, kk)
            await add_button_to_post(kk, message.id)
        except FloodWait as e:
            print(f"Flood wait encountered. Waiting for {e.x} seconds...")
            time.sleep(e.x)
            await add_button(client, message)  
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        kk = await message.copy(chat_id=Config.FROM_CHANNEL)
        await new_post(client, kk)



@Bot.on_message(filters.command("save_channel") & filters.user(Config.BOT_OWNER))
async def save_channel(bot, message):
    reply = await message.reply("Checking....")
    data = message.text
    userid = message.from_user.id

    try:
        command, id, fsub_id = data.split(" ")
    except ValueError:
        return await reply.edit_text("<b>Command Incomplete,\n\n Usage: /save_channel channelid fsubchannelid \n\nExample: /save_channel -100xxxxxxxx -100xxxxxxx</b>")
    
    try:
        channel_info = await bot.get_chat(int(id))
    except Exception as e:
        return await reply.edit_text("<b>Make me admin in the channels</b>")
    await reply.delete()
    await message.reply(f"{id} {fsub_id} #Name_for_the_channel:",  reply_to_message_id=message.id, reply_markup=ForceReply(True))

@Bot.on_message(filters.command("del_channel") & filters.user(Config.BOT_OWNER))
async def del_channel(bot, message):
    reply = await message.reply("Checking....")
    data = message.text
    userid = message.from_user.id
    try:     
         command, id = data.split(" ")
         await db.del_chat(id)
         await message.reply("channel deleted")
    except Exception as e:           
         await message.reply(f"<b>use proper manner\n\nother error:{e}</b>")
           

@Bot.on_message(filters.private & filters.reply)
async def save_channel_name(bot, name_message):     
     name = name_message.text
     data = name_message.reply_to_message.text
     print(f"{data}")
     id, fsub_id , other = data.split(" ")
     try:          
          chat_data = {"id": id, "name": name, "fsub_id": fsub_id} 
          await db.update_chat(chat_data)
          await name_message.reply("Given information saved")
     except Exception as e:
          await name_message.reply(f"<b>Not set, try again. Error: {e}</b>")
           

@Bot.on_message(filters.command("start_posting") & filters.user(Config.BOT_OWNER))
async def start_posting(client, message):
    
    args = message.text.split()
    if len(args) < 4:
        await message.reply_text("Usage: /start_posting <target_channel_id> <source_message_link_1> <source_message_link_2> ...")
        return

    # Extract target channel ID
    target_channel_id = int(args[1])

    # Extract source channel ID and message IDs from links
    try:
        source_message_id_1 = int(args[2].split('/')[-1])
        source_message_id_2 = int(args[3].split('/')[-1])
        source_channel_idd = "-100" + (args[2].split('/')[-2])
        source_channel_id = int(f"{source_channel_idd}")
    except ValueError:
        await message.reply_text("Invalid link format.")
        return

    # Ensure message IDs are in correct order
    if source_message_id_1 > source_message_id_2:
        source_message_id_1, source_message_id_2 = source_message_id_2, source_message_id_1
    await message.reply_text(f"Started posting from specified messages to channel {target_channel_id}")

    # Start the posting loop
    await post_messages(client, source_channel_id, source_message_id_1, source_message_id_2, target_channel_id)
     
async def post_messages(client, source_channel_id, start_message_id, end_message_id, target_channel_id):
     for message_id in range(start_message_id, end_message_id + 1):
        print(f"{message_id}")
        try:
            # Forward the message to the target channel
            post_message_id = int(message_id)
            await client.copy_message(chat_id=target_channel_id, from_chat_id=source_channel_id, message_id=post_message_id)
            print(f"Forwarded message {message_id} from channel {source_channel_id} to {target_channel_id}")
            # Wait for 1 hour before sending the next message
            await asyncio.sleep(Config.TIME_TO_WAIT)
        except FloodWait as e:
            print(f"FloodWait: Waiting for {e.x} seconds")
            await asyncio.sleep(e.x)
        except Exception as e:
            print(f"Error: {e}")
