from django.db import models
from django.contrib.postgres.fields import ArrayField

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Channel(BaseModel):
    name = models.CharField(blank=True, max_length=100, null=True)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Broker(BaseModel):
    name = models.CharField(blank=True, max_length=100, null=True)
    source_channels = models.ManyToManyField(Channel, related_name='source_bots', related_query_name='source_bot')
    destination_channels = models.ManyToManyField(Channel, related_name='destination_bots', related_query_name='destination_bot')

    def __str__(self):
        return self.name


class Account(BaseModel):
    phone = models.CharField(max_length=14)
    api_id = models.PositiveIntegerField()
    api_hash = models.CharField(max_length=100)
    log_in_code = models.PositiveIntegerField(null=True, blank=True)
    delay_between_msg = models.PositiveIntegerField(default=5)
    ids = ArrayField(models.CharField(max_length=50), blank=True, null=True)

    msg = models.TextField(null=True, blank=True)
    admin_username = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.phone
