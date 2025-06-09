from telethon.errors import UsernameInvalidError, UsernameNotOccupiedError, ChannelInvalidError
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.channels import GetFullChannelRequest


class ExistsTelegramChannel:
    async def check_channel_exists(self, client, identifier):
        try:
            if isinstance(identifier, str):
                result = await client(ResolveUsernameRequest(identifier))
                return bool(result.chats)
            elif isinstance(identifier, int):
                entity = await client.get_entity(identifier)
                if hasattr(entity, 'megagroup') or hasattr(entity, 'broadcast'):
                    await client(GetFullChannelRequest(entity))
                    return True
                return False
            else:
                print("Неверный тип данных для идентификатора.")
                return False
        except (UsernameNotOccupiedError, UsernameInvalidError, ChannelInvalidError):
            return False
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return False