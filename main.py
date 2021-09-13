import encodings
from tqdm import tqdm
import telethon
from telethon import TelegramClient, sync, functions, errors, types
from telethon.extensions import markdown
import asyncio
import time
from config import *
import markdown2
loop = asyncio.get_event_loop()





class GropAlbum:
    def __init__(self, albumId, media, mess):
        self.albumId = albumId
        self.media = media
        self.mess = mess
        self.medias = []

    def inputMedia(self, media):
        self.medias.append(media)

    def lenMedia(self):
        return len(self.medias)

    def getStatus(self, albumId):
        if albumId == self.albumId:
            return True
        elif self.albumId is None:
            return 'None'
        else:
            return 'main', self.medias, self.mess

class ForwardAlbum:
    def __init__(self, albumId):
        self.albumId = albumId
        self.ids = []

    def inputId(self, messId):
        self.ids.append(messId)

    def getIds(self):
        return self.ids

    def getStatus(self, albumId):
        if albumId == self.albumId:
            return True
        elif self.albumId is None:
            return 'None'
        else:
            return 'forward', self.ids



async def main():
    chat = ForwardAlbum(None)
    async with TelegramClient(session, api_id, api_hash) as client:
        for mess_id in tqdm([20, 21]):
            mess_id = mess_id+1
            mess = await client.get_messages(from_channel, ids=mess_id)
            print(mess)
            if mess is None:
                continue
            if mess.grouped_id is not None:
                albumId = mess.grouped_id
            else:
                albumId = None
            status = chat.getStatus(albumId)
            if mess.fwd_from is not None:
                if status is True and albumId is None:
                    await client.forward_messages(in_channel, mess_id, from_channel)
                elif status is True and albumId is not None:
                    chat.inputId(mess_id)
                elif status is not True:
                    if status[0] == 'main':
                        await client.send_file(in_channel, chat.medias, caption=chat.mess)
                        chat = ForwardAlbum(albumId)
                        chat.inputId(mess_id)
                    elif status[0] == 'forward':
                        await client.forward_messages(in_channel, chat.ids, from_channel)
                        chat = ForwardAlbum(albumId)
                        chat.inputId(mess_id)
                    elif status == 'None':
                        chat = ForwardAlbum(albumId)
                        chat.inputId(mess_id)
            elif mess.grouped_id is not None:
                if status is True:
                    chat.inputMedia(mess.media)
                elif status is not True:
                    if status[0] == 'main':
                        await client.send_file(in_channel, chat.medias, caption=chat.mess)
                        chat = GropAlbum(albumId, mess.media, mess.message)
                    elif status[0] == 'forward':
                        await client.forward_messages(in_channel, chat.ids, from_channel)
                        chat = GropAlbum(albumId, mess.media, mess.message)
                    elif status == 'None':
                        chat = GropAlbum(albumId, mess.media, mess.message)
            else:
                await client.send_message(in_channel, mess, parse_mode='HTML')
            time.sleep(1)

                # await client.forward_messages(entity=in_channel, messages=[76, 77], from_peer=from_channel)
            # await client.send_file(in_channel, [mess.media], caption=mess.message)

loop.run_until_complete(main())