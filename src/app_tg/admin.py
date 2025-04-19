from django.contrib import admin

from .models import TGUser


class TGUserAdmin(admin.ModelAdmin):
    list_display = ['tg_id', 'username', 'created_at', 'updated_at']
    list_filter = ['username', ]
    search_fields = ['tg_id', 'username', 'first_name', 'last_name']
    save_on_top = True


admin.site.register(TGUser, TGUserAdmin)
