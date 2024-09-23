from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User, Follow

UserAdmin.fieldsets += (
    ('Extra Fields', {'fields': ('avatar',)}),
)
UserAdmin.list_display = ('id',
                          'username',
                          'email',
                          'first_name',
                          'last_name',
                          'is_staff',
                          'avatar')
UserAdmin.list_editable += ('avatar',)

ordering = ('id',)

admin.site.register(User, UserAdmin)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Класс настройки модели Follow в админке."""

    list_display = ('user', 'following')
    search_fields = ('user', 'following')
