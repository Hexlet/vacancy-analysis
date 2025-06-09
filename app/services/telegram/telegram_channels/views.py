from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Channel
from .form import ChannelForm
from app.services.telegram.telegram_client import TelegramChannelClient
from app.services.telegram.telegram_channels.utils.exists_channel import ExistsTelegramChannel
from app.services.telegram.telegram_channels.utils.get_data import DataChannel
from app.services.telegram.telegram_channels.utils.save_data import SaveDataChannel
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.

class IndexChannelView(View):
    def get(self, request, *args, **kwargs):
        channels = Channel.objects.all().values(
            'id', 'username', 'channel_id', 'status', 'last_message_id')
        return JsonResponse(list(channels), safe=False)


class ShowChannelView(View):
    def get(self, request, *args, **kwargs):
        channel = get_object_or_404(Channel, id=kwargs['pk'])
        return JsonResponse({
            'id': channel.id,
            'username': channel.username,
            'channel_id': channel.channel_id,
            'status': channel.status,
            'last_message_id': channel.last_message_id,
        })

@method_decorator(csrf_exempt, name='dispatch')
class AddChannelView(View):

    async def get(self, request, *args, **kwargs):
        form = ChannelForm()
        return JsonResponse({
            'status': 'error',
            'error': form.errors,
            'data': form.data
        })


    async def post(self, request, *args, **kwargs):
        data = request.POST

        # Проверка в Telegram (асинхронно)
        client_wrapper = await TelegramChannelClient.create()
        client = client_wrapper.client

        username = data.get('username')
        exist = ExistsTelegramChannel()
        exists = await exist.check_channel_exists(client, username)

        if not exists:
            return JsonResponse({'status': 'error', 'errors': {'username': ['Канал не найден в Telegram']}})

        entity = await client.get_entity(username)
        data_channel = DataChannel()
        channel_data = await data_channel.get_channel_data(client, entity)

        save_data = SaveDataChannel()
        result = await save_data.save_valid_form(data, channel_data)
        return JsonResponse(result)


@method_decorator(csrf_exempt, name='dispatch')
class DeleteChannelView(View):
    def post(self, request, *args, **kwargs):
        channel_id = kwargs.get('pk')
        channel = get_object_or_404(Channel, id=channel_id)
        channel.delete()
        return JsonResponse({'status': 'deleted'})
