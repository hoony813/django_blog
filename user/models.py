from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=128, verbose_name='ID')
    email = models.EmailField(max_length=128, verbose_name='E-mail')
    password = models.CharField(max_length=128, verbose_name='비밀번호')
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='등록일')

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'
        verbose_name = '사용자'
        verbose_name_plural = '사용자'