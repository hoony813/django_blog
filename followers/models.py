from django.db import models

# Create your models here.

class Followers(models.Model):
    follower = models.OneToOneField('user.User',on_delete=models.CASCADE, verbose_name='Follower', related_name='follower')
    followee = models.ManyToManyField('user.User', verbose_name='followee',related_name='followee')

    class Meta:
        db_table = 'followers'
        verbose_name = 'followers'
        verbose_name_plural = 'followers'