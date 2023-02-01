from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as OrigUserAdmin

from .forms import UserChangeForm, UserCreationForm

from .models import User

# Register your models here.
class AppUserAdmin(OrigUserAdmin):
    # The forms to add and change user instances
    add_form = UserCreationForm
    form = UserChangeForm

    list_display = ("username", "email", "first_name", "last_name")

    fieldsets = (
        # (None, {"fields": ("password")}),
        # ('Personal Data', {"fields": ("first_name", "last_name")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                )
            },
        ),
    )


class AuthUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name")


# admin.site.register(User, AppUserAdmin)
admin.site.register(User, AuthUserAdmin)
