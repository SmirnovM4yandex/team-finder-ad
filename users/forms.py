from django import forms
from django.contrib.auth import authenticate

from core.constants import INVALID_CREDENTIALS_MESSAGE

from users.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Пароль",
    )

    class Meta:
        model = User

        fields = [
            "name",
            "surname",
            "email",
            "password",
        ]

        labels = {
            "name": "Имя",
            "surname": "Фамилия",
            "email": "Email",
        }


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
    )

    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Пароль",
    )

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        user = authenticate(
            email=email,
            password=password,
        )

        if not user:
            raise forms.ValidationError(
                INVALID_CREDENTIALS_MESSAGE
            )

        cleaned_data["user"] = user

        return cleaned_data


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User

        fields = [
            "name",
            "surname",
            "avatar",
            "about",
            "phone",
            "github_url",
        ]

        labels = {
            "name": "Имя",
            "surname": "Фамилия",
            "avatar": "Аватар",
            "about": "О себе",
            "phone": "Телефон",
            "github_url": "GitHub",
        }

        widgets = {
            "about": forms.Textarea(
                attrs={
                    "rows": 5,
                }
            ),
        }
