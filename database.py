import motor.motor_asyncio
from configs import Config
import datetime

DATABASE_URL = Config.DATABASE_URL
DATABASE_NAME = Config.DATABASE_NAME

class Database:
    
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.chat = self.db.chat
        self.ban = self.db.ban
        self.req = self.db.requests
        self.file = self.db.files
        self.fsub = self.db.fsub

    async def add_user(self, user_data):
        user_dict = user_data.to_dict()
        await self.col.insert_one(user_dict)

    async def find_join_req(self, id, channel_id):
        try:
            return bool(await self.req.find_one({'id': id, 'channel_id': channel_id}))
        except Exception as e:
            print(f"{e}")
            
    async def add_join_req(self, id, channel_id):
        await self.req.insert_one({'id': id, 'channel_id': channel_id})

    async def del_join_req(self, channel_id):
        await self.req.delete_many({'channel_id': channel_id})
        
    async def present_user(self, id):
        user = await self.col.find_one({'id': id})
        return bool(user)

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def add_ban_userid(self, id):
        user = {'banid': id}
        await self.ban.insert_one(user)

    async def get_ban_status(self, id):
        user = await self.ban.find_one({'banid': id})
        return bool(user)

    async def remove_ban_userid(self, id):
        await self.ban.delete_one({'banid': id})

    async def save_post_ids(self, chat_id, post_ids):        
        chat_data = await self.chat.find_one({'chat_id': chat_id})
        if chat_data:
            await self.chat.update_one(
                {'chat_id': chat_id},
                {'$addToSet': {'post_ids': {'$each': post_ids}}}
            )
        else:
            new_chat_data = {'chat_id': chat_id, 'post_ids': post_ids}
            await self.chat.insert_one(new_chat_data)
  
    async def get_post_ids(self, chat_id):        
        chat_data = await self.chat.find_one({'chat_id': chat_id})
        if chat_data:
            return chat_data.get('post_ids', [])
        else:
            return []

    async def delete_post_ids(self, chat_id, post_id):
        await self.chat.update_one(
            {'chat_id': chat_id},
            {'$pull': {'post_ids': post_id}}
        )
    async def save_file_id(self, user_id, file_id):
        file_data = {'user_id': user_id, 'file_id': file_id}
        await self.file.insert_one(file_data)
        
    async def get_file_id(self, user_id):
        file_data = await self.file.find_one({'user_id': user_id})
        if file_data:
            return file_data.get('file_id')
        else:
            return None

    async def delete_file_id(self, user_id):
        await self.file.delete_one({'user_id': user_id})
            
    async def update_chat(self, chat_data):
        info =  await self.fsub.find_one({"id": chat_data["id"]})
        if info:
            await self.fsub.update_one({"id": chat_data["id"]}, {"$set": chat_data}, upsert=True)
        else:
            await self.fsub.insert_one(chat_data)

    async def delete_chat(self, chat_id):
        info = await self.fsub.find_one({"id": chat_id})
        
        await self.fsub.delete_one({"id": chat_id})
        
    async def get_fsub_channel_id(self, chat_id):
        try:
            info =  await self.fsub.find_one({"id": chat_id})
            print(f"{info}")
            if info:
                return info.get('fsub_id')
            else:
                return None
        except Exception as e:
            print(f"{e}")
            return None


    async def get_channels(self):
        ch_info = self.fsub.find({})
        return ch_info
    
    async def get_channel(self, channel_id):
        channel_data = await self.fsub.find_one({"id": channel_id})
        print(f"{channel_data}")
        return channel_data
        
db = Database(DATABASE_URL, DATABASE_NAME)
