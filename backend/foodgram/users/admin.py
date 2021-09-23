from django.contrib import admin

from .models import Follow, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'email',
        'username',
        'password',
        'first_name',
        'last_name',
        'is_subscribed',
        'is_active',
        'is_staff',
    )
    list_editable = ('password',)
    search_fields = ('email', 'username',)
    list_filter = ('email', 'username',)
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    search_fields = ('user',)
    list_filter = ('user',)
