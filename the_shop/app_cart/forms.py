from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CerateOrderForm(forms.Form):

    name = forms.CharField(max_length=100, required=False, help_text='ФИО')
    phone = forms.CharField(min_length=10, max_length=10, required=True, help_text='Номер телефона')
    mail = forms.EmailField(label='email', help_text='Имэйл')
    city = forms.CharField(max_length=100, required=True, help_text='Город')
    address = forms.CharField(max_length=300, required=True, help_text='Адрес')
    delivery = forms.CharField(max_length=100, required=False, help_text='Тип доставки')
    pay = forms.CharField(max_length=100, required=False, help_text='Тип оплаты')
    comment = forms.CharField(max_length=300, required=False, help_text='Комментарий к заказу')

    def clean_name(self):
        full_name = self.cleaned_data['name']
        names = full_name.split()
        if len(names) != 3:
            raise ValidationError("Нужны Фамилия Имя Отчество через пробел")
        return full_name

    class Meta:
        model = User
        fields = ('user', 'name_for_order', 'phone_for_order', 'mail_for_order', 'city_for_order', 'address_for_order', 'delivery_type', 'payment_type')
