from django.contrib import admin

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
    print(queryset[0])
get_sign_code.short_description = "Get sign code"

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone')
    search_fields = ['phone']
    actions = [get_sign_code]