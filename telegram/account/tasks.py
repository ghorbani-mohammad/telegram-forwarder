from celery.decorators import task

@task(name="sing_in")
def sing_in(account_id):
    from django.core.management import call_command
    call_command('sign_in', account_id)
