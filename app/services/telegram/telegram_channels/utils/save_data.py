from asgiref.sync import sync_to_async
from django.db import IntegrityError
from django.http import JsonResponse

from app.services.telegram.telegram_channels.form import ChannelForm


class SaveDataChannel:
    @sync_to_async
    def save_valid_form(self, data, channel_data):
        try:
            form = ChannelForm(data)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.channel_id = channel_data['channel_id']
                obj.status = channel_data['status']
                obj.last_message_id = channel_data['last_message_id']
                obj.save()
                return {'status': 'ok', 'details': 'The channel was created'}
            return {
                'status': 'error',
                'errors': 'Form is not valid',
                'details': 'form.errors'
            }
        except IntegrityError as e:
            return JsonResponse({
                'status': 'error',
                'error': 'The channel with such username or ID exists',
                'details': str(e)
            }, status=400)
