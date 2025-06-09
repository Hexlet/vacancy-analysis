from telethon.tl.functions.channels import GetFullChannelRequest

class DataChannel:
    async def get_channel_data(self, client, entity):
        full = await client(GetFullChannelRequest(entity))
        channel_id = entity.id
        status = 'active'
        last_message_id = full.full_chat.read_inbox_max_id
        return {
            'channel_id': channel_id,
            'status': status,
            'last_message_id': last_message_id
        }