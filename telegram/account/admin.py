from openpyxl import load_workbook

from django.utils import timezone
from django.contrib import admin, messages
from django.utils.translation import ngettext
from django import forms
from django.core.files.storage import default_storage

from .models import Account


class AccountForm(forms.ModelForm):
    ids_excel = forms.FileField(required=False)
    
    class Meta:
        model = Account
        fields = '__all__'


def send_msg(modeladmin, request, queryset):
    from .tasks import send_msg
    account = queryset[0]
    send_msg.delay(account.id)
    modeladmin.message_user(request, ngettext(
        'messages will be sended.',
        'messages will be sendeds.',
        queryset.count(),
    ), messages.SUCCESS)
    send_msg.short_description = "messages will be sended"


def forward_msg(modeladmin, request, queryset):
    from .tasks import forward_msg
    account = queryset[0]
    forward_msg.delay(account.id)
    modeladmin.message_user(request, ngettext(
        'messages will be sended.',
        'messages will be sendeds.',
        queryset.count(),
    ), messages.SUCCESS)
    forward_msg.short_description = "messages will be sended"


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone')
    search_fields = ['phone']
    actions = [forward_msg, send_msg]
    form = AccountForm

    def save_model(self, request, obj, form, change):
        if 'ids_excel' in request.FILES:
            obj.ids = []
            excel = request.FILES['ids_excel']
            path = default_storage.save('tmp/ids_{}.xlsx'.format(int(timezone.now().timestamp())), excel)
            sheet = load_workbook(filename='{}'.format(path)).active
            ids = [cell.value for cell in sheet['A']]
            default_storage.delete('tmp/ids_{}.xlsx'.format(int(timezone.now().timestamp())),)
            obj.ids += ids
        obj.save()