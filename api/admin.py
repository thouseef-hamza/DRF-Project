from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# Register your models here.


class UserModelAdmin(BaseUserAdmin):
    list_display = ["id","email", "username","tc", "is_admin"]
    list_display_links = ["id","email"]
    list_filter = ["is_admin"]
    fieldsets = [
        ("User Credentials", {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("username","tc")}), 
        ("Permissions", {"fields": ("is_admin",)}),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "username","tc", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email","id"]
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(User, UserModelAdmin)