# from asgiref.sync import sync_to_async
import time
from django.utils import timezone
from django.core.management.base import BaseCommand
from telethon import TelegramClient, events, sync

from account import models as acc_models


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('account_id', type=int, help='Indicates the id of account')

    def handle(self, *args, **options):
        account_id = options['account_id']
        account = acc_models.Account.objects.get(pk=account_id)
        print('***** Send msg... {}, time: {}'.format(account.phone, timezone.now()))
        client = TelegramClient(account.phone, account.api_id, account.api_hash)

        try:
            assert client.connect()
        except AssertionError:
            if not client.is_user_authorized():
                client.send_code_request(account.phone)
            me = client.sign_in(account.phone, account.log_in_code)
            client.start()

        # try:
        #     client.send_message('@ghorbani_mohammad', 'Hello! bot started')
        # except:
        #     print('error')

        for id in account.ids:
            client.send_message(id, account.msg)
            time.sleep(account.delay_between_msg)


        client.disconnect()