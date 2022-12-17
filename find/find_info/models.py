from django.db import models


class Document(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    file = models.FileField()


class Doc(models.Model):
    objects = None
    name = models.CharField(max_length=150, verbose_name='Назва')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')
    link = models.CharField(max_length=150, verbose_name='Посилання')
    file = models.FileField(null=True)
    description = models.CharField(max_length=150, verbose_name='Опис')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Doc'
        ordering = ['description', 'name', 'updated_at', 'link']
