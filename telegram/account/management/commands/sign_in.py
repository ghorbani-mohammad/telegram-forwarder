from django.utils import timezone
from django.core.management.base import BaseCommand
from telethon import TelegramClient

from account import models as acc_models


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('account_id', type=int, help='Indicates the id of account')

    def handle(self, *args, **options):
        account_id = options['account_id']
        account = acc_models.Account.objects.get(pk=account_id)
        print('Sing in... {}, time: {}'.format(account.phone, timezone.now()))
        client = TelegramClient(account.phone, account.api_id, account.api_hash)
        client.connect()
        client.send_code_request(account.phone)
