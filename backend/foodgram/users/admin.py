from django.contrib import admin

from .models import Subscribe


class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'subscribing_user',
        'user_to_subscribe'
    )


admin.site.register(Subscribe, SubscribeAdmin)

