from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'blood_group', 'is_available', 'created_at')
    list_filter = ('blood_group', 'is_available', 'created_at')
    search_fields = ('username', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Authentication', {'fields': ('username', 'password', 'email')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone')}),
        ('Blood Donation', {'fields': ('blood_group', 'last_donation_date', 'is_available')}),
        ('Location', {'fields': ('latitude', 'longitude', 'location_name')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
