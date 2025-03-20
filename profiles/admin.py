from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserProfileChangeForm, UserProfileCreateForm
from .models import UserProfile


class UserProfileAdmin(UserAdmin):
    add_form = UserProfileCreateForm
    form = UserProfileChangeForm
    model = UserProfile
    list_display = ["username", "first_name", "last_name", "is_staff"]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ["avatar"]}),)
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


admin.site.register(UserProfile, UserProfileAdmin)
