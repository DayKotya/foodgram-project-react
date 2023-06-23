from django.contrib import admin

from users.models import User, Subscribe


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'email', 'password', 'first_name', 'last_name'
    )
    list_filter = ('username', 'email')
    search_fields = ('username', 'email', )


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'user', 'author'
    )
    search_fields = ('user__username', 'user__email', )
