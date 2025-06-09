from asgiref.sync import sync_to_async
from app.services.telegram.telegram_channels.form import ChannelForm


class SaveDataChannel:
    @sync_to_async
    def save_valid_form(self, data, channel_data):
        form = ChannelForm(data)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.channel_id = channel_data['channel_id']
            obj.status = channel_data['status']
            obj.last_message_id = channel_data['last_message_id']
            obj.save()
            return {'status': 'ok'}
        return {'status': 'error', 'errors': form.errors}
