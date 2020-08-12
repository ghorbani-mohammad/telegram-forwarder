from django.contrib import admin, messages
from django.utils.translation import ngettext

from .models import Channel, Broker, Account

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'username')
    search_fields = ['name', 'username']


@admin.register(Broker)
class BrokerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ['name']

def get_sign_code(modeladmin, request, queryset):
    from .tasks import sing_in
    account = queryset[0]
    sing_in.delay(account.id)
    modeladmin.message_user(request, ngettext(
        'You will shortly get the sign_in code.',
        'You will shortly get the sign_in codes.',
        queryset.count(),
    ), messages.SUCCESS)
    sing_in.short_description = "Export selected factors as excel file"
    get_sign_code.short_description = "Get sign_in code"

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone')
    search_fields = ['phone']
    actions = [get_sign_code]