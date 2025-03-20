from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.validators import validate_email

from .models import UserProfile


class UserProfileCreateForm(forms.ModelForm):

    error_messages = {
        "password_mismatch": ("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=("Enter the same password as above, for verification."),
    )

    class Meta:
        model = UserProfile
        fields = ("username",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def clean_username(self):
        username = self.cleaned_data["username"]
        username = username.lower()
        validate_email(username)
        return username

    def save(self, commit=True):
        user = super(UserProfileCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserProfileChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=("Password"),
        help_text=(
            "Raw passwords are not stored, so there is no way to see "
            "this user's password, but you can change the password "
            'using <a href="password/">this form</a>.'
        ),
    )

    class Meta:
        model = UserProfile
        fields = "__all__"

    def clean_username(self):
        username = self.cleaned_data["username"]
        username = username.lower()
        validate_email(username)
        return username
