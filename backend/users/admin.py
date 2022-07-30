from django.contrib import admin
# from django.utils.translation import ugettext_lazy as _
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Follow


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'first_name', 'last_name', 'password', 'is_subscribed')
    list_filter = ('email', 'username', 'first_name', 'last_name', 'password', 'is_subscribed')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'first_name', 'last_name','password1', 'password2',
                'is_staff', 'is_active', 'is_subscribed')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)   

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Follow)