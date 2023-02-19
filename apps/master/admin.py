from django.contrib import admin

# Register your models here.
from .models import UserPreferensi


class UserPreferensiAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "pref",
    )
    list_filter = ("user",)


admin.site.register(UserPreferensi, UserPreferensiAdmin)
