from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

UserModel = get_user_model()


class SingupForm(UserCreationForm):
    """Form of singup user"""

    email = forms.EmailField(
        label="Электронная почта",
        error_messages={
            "unique": "Пользователь с такой почтой уже существует.",
            "invalid": "Введите корректный адрес электронной почты.",
        },
    )

    class Meta:
        model = UserModel
        fields = (
            "username",
            "email",
        )
