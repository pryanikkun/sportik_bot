from django.contrib import admin

from .models import Notification, NotificationType, Subscription


# Register your models here.

@admin.register(NotificationType)
class NotificationTypeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )
    list_editable = ('name',)
    search_fields = ('name',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'type',
        'text',
    )
    list_editable = ('type', 'text')
    list_filter = ('type',)
    search_fields = ('type', 'text')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'schedule',
        'type',
    )
    list_filter = ('user', 'type')
    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name'
    )
