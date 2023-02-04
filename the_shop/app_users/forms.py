from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .validators import file_size
from django.core.exceptions import ValidationError
from .models import UserProfile


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, required=False, help_text='ФИО')
    phone_number = forms.CharField(min_length=10, max_length=10, required=True, help_text='Номер телефона')
    email = forms.EmailField(label='email', help_text='Имэйл')
    avatar = forms.FileField(required=False, validators=[file_size])

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError("Пользователь с таким имэйлом уже есть")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        new = UserProfile.objects.filter(phone_number=phone_number)
        if new.count():
            raise ValidationError("Пользователь с таким номером уже есть")
        return phone_number

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        names = full_name.split()
        if len(names) != 3:
            raise ValidationError("Нужны Фамилия Имя Отчество через пробел")
        return full_name

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2')


class ChangeProfileForm(forms.Form):
    full_name = forms.CharField(max_length=100, required=False, help_text='ФИО')
    phone_number = forms.CharField(min_length=10, max_length=10, required=True, help_text='Номер телефона')
    email = forms.EmailField(label='email', help_text='Имэйл')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError("Пользователь с таким имэйлом уже есть")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        new = UserProfile.objects.filter(phone_number=phone_number)
        if new.count():
            raise ValidationError("Пользователь с таким номером уже есть")
        return phone_number

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        names = full_name.split()
        if len(names) != 3:
            raise ValidationError("Нужны Фамилия Имя Отчество через пробел")
        return full_name


class AvatarForm(forms.Form):
    avatar = forms.FileField(required=False, validators=[file_size])


class RestorePasswordForm(forms.Form):
    email = forms.EmailField()
