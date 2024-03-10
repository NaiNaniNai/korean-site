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


class EditProfileForm(forms.ModelForm):
    """Form of edit profile"""

    avatar = forms.ImageField(required=False, label="Изображение")
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Фамилия"}),
        required=False,
        label="Фамилия",
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Имя"}),
        required=False,
        label="Имя",
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "placeholder": "ГГГГ-ММ-ДД"}),
        required=False,
        label="Дата рождения",
    )

    class Meta:
        model = UserModel
        fields = ("avatar", "last_name", "first_name", "date_of_birth")


class ResetPasswordForm(forms.ModelForm):
    """Form of reset password in account"""

    username = forms.CharField(
        label="user", widget=forms.TextInput(attrs={"placeholder": "Имя пользователя"})
    )
    email = forms.EmailField(
        label="envelope",
        widget=forms.EmailInput(attrs={"placeholder": "Электронная почта"}),
    )
    password = forms.CharField(
        label="lock", widget=forms.PasswordInput(attrs={"placeholder": "Новый пароль"})
    )
    repeated_password = forms.CharField(
        label="lock",
        widget=forms.PasswordInput(attrs={"placeholder": "Повторите пароль"}),
    )

    class Meta:
        model = UserModel
        fields = ("username", "email", "password", "repeated_password")
