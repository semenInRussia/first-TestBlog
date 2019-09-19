from django.db import models

from django.shortcuts import reverse
# # Create your models here.
class Tag(models.Model):
    name = models.CharField('Название', max_length=30, unique=True)
    slug = models.SlugField('URL', unique=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE,)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ["name"]
class MyArticles(models.Model):
    colors = {
        "success":'green',
        'warning':"yellow",
        'danger':"red" ,  
        'dark': "black" ,
        'light': 'white',
        'info': 'blue',
   }

    name = models.CharField('Название', max_length=60, unique=True,)
    author = models.ForeignKey('auth.User', on_delete = models.CASCADE,)
    text = models.TextField('Tекст',)
    slug = models.SlugField(verbose_name='URL', max_length=50,)
    data = models.DateTimeField('Дата', auto_now_add=True,)
    color = models.CharField('Цвет',max_length=10, choices=colors.items(), default='green')
    tag = models.ForeignKey(Tag, on_delete = models.CASCADE,verbose_name='тег',blank=True)

    def get_absolute_url(self):
        return reverse('main:detail', args=(self.slug,))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-name"]
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'