from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import *
from .models import BankSoal


class PostSoal(admin.ModelAdmin):
    list_display = ('id', 'question', 'type', 'subject', 'source', 'year','preview_button')
    list_filter = ('subject', 'source', 'year')
    search_fields = ['question','subject', 'source', 'year', 'id']
    readonly_fields = ['preview_button']
    
    def preview_button(self, obj):
        if obj.id:
            url = reverse('render-preview', args=[obj.id])
            return format_html('<a href="{}" target="_blank">Preview</a>', url)
        else:
            return '(Save and continue editing to preview)'
        
admin.site.register(BankSoal, PostSoal)