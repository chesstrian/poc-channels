from django.contrib import admin

from chat.models import Room


@admin.register(Room)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name',)
