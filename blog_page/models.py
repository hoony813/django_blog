from django.db import models
from datetime import datetime
# Create your models here.

def upload_to(instance, filename):

    return 'images/%s/%s' % (instance.writer.username, filename)

class Blog(models.Model):
    title = models.CharField(max_length=255, verbose_name='제목')
    contents = models.TextField(verbose_name='내용')
    thumbnails = models.ImageField(blank=True,upload_to=upload_to)
    writer = models.ForeignKey('user.User',on_delete=models.CASCADE,verbose_name='작성자')
    tags = models.ManyToManyField('tag.Tag',verbose_name='태그')
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')


    def __str__(self):
        return self.title

    class Meta:
        db_table = 'blog'
        verbose_name = '게시글'
        verbose_name_plural = '게시글'