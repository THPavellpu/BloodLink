from django.contrib import admin
from .models import NotificationToken


@admin.register(NotificationToken)
class NotificationTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username', 'token')
    readonly_fields = ('created_at', 'updated_at')
