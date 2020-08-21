import time
from sqlite3 import OperationalError

from django.utils import timezone
from django.core.management.base import BaseCommand
from telethon import TelegramClient, events, sync
from telethon.errors import PhoneCodeInvalidError, ApiIdInvalidError, FloodWaitError


from account import models as acc_models


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('account_id', type=int, help='Indicates the id of account')

    def handle(self, *args, **options):
        account_id = options['account_id']
        account = acc_models.Account.objects.get(pk=account_id)
        print('***** Forward msg... {}'.format(account.phone))
        
        client = TelegramClient(None, account.api_id, account.api_hash)

        try:
            assert client.connect()
        except AssertionError:
            if not client.is_user_authorized():
                client.send_code_request(account.phone)
                print('before')
                time.sleep(30)
                print('after')
            account = acc_models.Account.objects.get(pk=account_id)
            print(account.log_in_code)
            if account.log_in_code is None:
                return 'phone code invalid'
            try:
                me = client.sign_in(account.phone, account.log_in_code)
                client.start()
            except PhoneCodeInvalidError:
                return 'phone code invalid'
            except ApiIdInvalidError:
                return 'api invalid'
            except FloodWaitError:
                return 'flood error'
            except OperationalError:
                return 'sqlite error'
        except ApiIdInvalidError:
            return 'api invalid'
        except FloodWaitError:
            return 'flood error'
        except OperationalError:
            return 'sqlite error'

        client.send_message(account.admin_username, '🔴 🔴 Hey admin I am your bot!')
        account.logged = True
        account.save()
        print('successful login to {}'.format(account.phone))
        @client.on(events.NewMessage(incoming=True))
        async def my_event_handler(event):
            chat = await event.get_chat()
            sender = await event.get_sender()
            if sender.username == account.admin_username:
                account.refresh_from_db()
                print('msg from admin')
                for id in account.ids:
                    time.sleep(account.delay_between_msg)
                    try:
                        await event.forward_to(id)
                    except Exception as e:
                        print('error: user id {} not found'.format(id))
                        print(str(e))
                        continue
                    time.sleep(account.delay_between_msg)


        client.run_until_disconnected()