from django.db import models
from datetime import datetime


class Document(models.Model):
    objects = None
    name = models.CharField(max_length=100, null=True, blank=True)
    file = models.FileField()


class Doc(models.Model):
    objects = None
    name = models.CharField(max_length=150, verbose_name='Назва', default='file')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')
    link = models.CharField(max_length=150, verbose_name='Посилання', blank=True)
    file = models.FileField(null=True)
    description = models.TextField(blank=True, verbose_name='Текст')
    about_file = models.CharField(max_length=200, verbose_name='Опис', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Doc'
        ordering = ['about_file', 'name', 'updated_at', 'link']


class LineOfDoc(models.Model):
    objects = None
    text = models.CharField(max_length=600, verbose_name='Текст рядка', db_index=True)
    doc = models.ForeignKey(Doc, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.text


class WordOfDoc(models.Model):
    objects = None
    text = models.CharField(max_length=100, verbose_name='Слово')
    line = models.ForeignKey(LineOfDoc, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
