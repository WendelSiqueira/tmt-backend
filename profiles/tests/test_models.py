import pytest
from django.contrib.auth import get_user_model
from profiles.forms import UserProfileCreateForm
from profiles.models import UserProfile


UserProfile = get_user_model()

@pytest.mark.django_db
def test_user_profile_creation():
    user = UserProfile.objects.create_user(username="testuser@test.com", password="testpassword")
    assert user.username == "testuser@test.com"
    assert user.check_password("testpassword")


@pytest.mark.django_db
def test_user_profile_create_form_valid_data():
    form_data = {
        "username": "testuser@example.com",
        "password1": "strongpassword123",
        "password2": "strongpassword123",
    }
    form = UserProfileCreateForm(data=form_data)
    assert form.is_valid()
    user = form.save()
    assert user.username == "testuser@example.com"
    assert user.check_password("strongpassword123")


@pytest.mark.django_db
def test_user_profile_create_form_password_mismatch():
    form_data = {
        "username": "testuser@example.com",
        "password1": "strongpassword123",
        "password2": "differentpassword123",
    }
    form = UserProfileCreateForm(data=form_data)
    assert not form.is_valid()
    assert "password_mismatch" in form.error_messages
    assert "password2" in form.errors


@pytest.mark.django_db
def test_user_profile_create_form_invalid_email():
    form_data = {
        "username": "invalid-email",
        "password1": "strongpassword123",
        "password2": "strongpassword123",
    }
    form = UserProfileCreateForm(data=form_data)
    assert not form.is_valid()
    assert "username" in form.errors
