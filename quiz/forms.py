from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text="Required. Inform a valid email address.")

    class Meta:
        # User model
        model = User
        # Fields to be displayed on the form
        fields = ["username", "email", "password1", "password2"]