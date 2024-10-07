# from django.apps import apps
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from user_management.models import CustomUser


# Register your models here.
# app = apps.get_app_config("user_management")
#
# for model in app.get_models():
#     try:
#         admin.site.register(model)
#     except admin.sites.AlreadyRegistered:
#         pass

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = CustomUser
    list_display = ('email', 'full_name', 'is_student', 'is_admin', 'is_staff', 'is_active')
    search_fields = ('email', 'full_name')
    ordering = ('email',)

    readonly_fields = ('date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name',)}),
        ('Permissions', {
            'fields': (
                ('is_superuser',),
                ('is_active', 'is_staff', 'is_student', 'is_admin'),
            ),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'full_name', 'password1', 'password2',
                ('is_student', 'is_admin', 'is_active', 'is_staff')
            )
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
