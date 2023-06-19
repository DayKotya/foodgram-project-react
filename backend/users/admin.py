from django.contrib import admin

from users import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'email', 'password', 'first_name', 'last_name'
    )
    list_filter = ('username', 'email')


@admin.register(models.Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'user', 'author'
    )
