from django.db import models


class Document(models.Model):
    objects = None
    name = models.CharField(max_length=100, null=True, blank=True)
    file = models.FileField()


class Doc(models.Model):
    objects = None
    name = models.CharField(max_length=150, verbose_name='Назва')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')
    link = models.CharField(max_length=150, verbose_name='Посилання')
    file = models.FileField(null=True)
    description = models.TextField(blank=True, verbose_name='Текст')
    about_file = models.CharField(max_length=200, verbose_name='Опис', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Doc'
        ordering = ['about_file', 'name', 'updated_at', 'link']
