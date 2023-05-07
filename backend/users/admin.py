from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'first_name', 'last_name', 'email')
    search_fields = ('username', 'email',)


admin.site.register(User, UserAdmin)
