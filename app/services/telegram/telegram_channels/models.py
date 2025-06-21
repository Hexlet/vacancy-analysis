from django.db import models


class Channel(models.Model):
    username = models.CharField(
        max_length=255, unique=True, verbose_name=('channel_name')
    )
    channel_id = models.IntegerField(
        max_length=255, unique=True, verbose_name=('channel_id')
    )
    status = models.CharField(
        max_length=10, verbose_name=('channel_status'), blank=True, null=True
    )
    last_message_id = models.IntegerField(
        max_length=255,
        unique=True,
        verbose_name=('last_message_id'),
        blank=True,
        null=True
    )
