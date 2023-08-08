from django.forms import ModelForm
from django.contrib.auth.password_validation import validate_password
from django import forms

from django.contrib.auth.models import User
from .models import Profile


class UserLoginForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-field username-field",
                    "placeholder": "Enter username:",
                }
            ),
            "password": forms.PasswordInput(
                attrs={
                    "class": "form-field password-field",
                    "placeholder": "Enter password:",
                }
            ),
        }


class UserRegForm(ModelForm):
    rpassword = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-field password-field",
                "placeholder": "Repeat password:",
            }
        )
    )

    class Meta:
        model = User
        fields = ["username", "password", "email"]

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-field username-field",
                    "placeholder": "Enter username:",
                }
            ),
            "password": forms.PasswordInput(
                attrs={
                    "class": "form-field password-field",
                    "placeholder": "Enter password:",
                }
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-field email-field", "placeholder": "Enter email:"}
            ),
        }

    def clean_username(self):
        username = self.cleaned_data["username"]
        MIN_LENGTH = 6
        MAX_LENGTH = 12

        if len(username) < MIN_LENGTH or len(username) > MAX_LENGTH:
            raise forms.ValidationError(
                f"Username should be between 6 to 12 characters."
            )

        return username

    # the django inbuilt function that validate the password properly
    def clean_password(self):
        password = self.cleaned_data["password"]
        validate_password(password)
        return password

    # check if the two password are entered exactly the same
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password"):
            password = cleaned_data["password"]
            rpassword = cleaned_data["rpassword"]

            if password != rpassword:
                raise forms.ValidationError("Password does not match.")

    # hash the password
    def save(self):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.save()

        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]

        widgets = {
            "username": forms.TextInput(attrs={"class": "username form-field"}),
            "email": forms.TextInput(attrs={"class": "email form-field"}),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["gender", "profile_pic", "desc", "website"]

        widgets = {
            "desc": forms.TextInput(attrs={"class": "desc form-field"}),
            "website": forms.TextInput(attrs={"class": "website form-field"}),
            "gender": forms.Select(attrs={"class": "gender"}),
            "desc": forms.Textarea(attrs={"class": "desc"}),
        }
