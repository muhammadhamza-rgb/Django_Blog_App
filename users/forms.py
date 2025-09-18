from django import forms
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string

from .models import Profile
from .sendgrid_email import send_email_via_sendgrid


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


class SendGridPasswordResetForm(PasswordResetForm):
    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        # Render the subject and body
        subject = render_to_string(subject_template_name, context)
        subject = "".join(subject.splitlines())  # remove newlines

        body = render_to_string(email_template_name, context)

        # Send via SendGrid API
        send_email_via_sendgrid(to_email, subject, body)
