from django.db import models

# Create your models here.

class Follwers(models.Model):
    follower = models.OneToOneField('user.User',on_delete=models.CASCADE, verbose_name='Follower')
    followee = models.ManyToManyField('user.User', verbose_name='followee')

    class Meta:
        db_table = 'follower'
        verbose_name = 'follower'
        verbose_name_plural = 'follower'