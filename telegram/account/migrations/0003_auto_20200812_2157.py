# Generated by Django 2.2.15 on 2020-08-12 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_account_log_in_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='delay_between_msg',
            field=models.PositiveIntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='account',
            name='log_in_code',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
