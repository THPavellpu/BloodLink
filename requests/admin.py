from django.contrib import admin
from .models import BloodRequest


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_group', 'urgency', 'is_fulfilled', 'created_at')
    list_filter = ('blood_group', 'urgency', 'is_fulfilled', 'created_at')
    search_fields = ('user__username', 'location_name')
    readonly_fields = ('created_at', 'updated_at')
