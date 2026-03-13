from django.contrib import admin
from .models import AlertSubscription, NotificationLog


@admin.register(AlertSubscription)
class AlertSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'frequency', 'is_active', 'created_at']
    list_filter = ['frequency', 'is_active']
    search_fields = ['email', 'name']


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ['subscription', 'empty_leg', 'sent_at', 'was_read']
    list_filter = ['was_read']
