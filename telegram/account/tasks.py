from celery.decorators import task


@task(name="send_msg")
def send_msg(account_id):
    from django.core.management import call_command
    call_command('send_msg', account_id)

@task(name="forward_msg")
def forward_msg(account_id):
    from django.core.management import call_command
    call_command('forward_msg', account_id)