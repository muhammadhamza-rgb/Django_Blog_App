from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove help texts
        for fieldname in ["username", "password1", "password2"]:
            self.fields[fieldname].help_text = None


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove help texts
        for fieldname in ["username"]:
            self.fields[fieldname].help_text = None


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_picture"]
