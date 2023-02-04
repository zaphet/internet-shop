from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    STATUS_CHOISES = [
        ('a', 'Активный'),
        ('n', 'Не активный')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    second_name = models.CharField(max_length=30, blank=True, verbose_name='Отчество')
    phone_number = models.CharField(max_length=12, unique=True, blank=True, verbose_name='Номер телефона')
    money = models.IntegerField(default=0, verbose_name='Баланс')
    is_active = models.CharField(max_length=1, choices=STATUS_CHOISES, default='a', verbose_name='Активность')
    money_spend = models.IntegerField(default=0, verbose_name='Количество потраченных денег')
    avatar = models.FileField(upload_to='users/avatars', default='users/avatars/no_image.jpg', verbose_name='Аватар')

    def __str__(self):
        return f'{self.user} {self.money} {self.is_active} '

    class Meta:
        db_table = 'userprofile'
        ordering = ['user']
