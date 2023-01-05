from django.db import models


class File(models.Model):
    name = models.CharField(max_length=150, default='file', null=True)
    file = models.FileField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'File'
        ordering = ['name', 'file']


class Doc(models.Model):
    name = models.CharField(max_length=100, verbose_name='Назва', null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')
    link = models.CharField(max_length=150, verbose_name='Посилання', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Doc'
        ordering = ['name', 'updated_at', 'link']


class LineOfDoc(models.Model):
    line_number = models.IntegerField(verbose_name='Номер ряду')
    text = models.CharField(max_length=600, verbose_name='Текст рядка')
    doc = models.ForeignKey(Doc, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.text


class WordOfDoc(models.Model):
    text = models.CharField(max_length=100, verbose_name='Слово', db_index=True)
    line = models.ForeignKey(LineOfDoc, on_delete=models.CASCADE, null=True)
    doc = models.ForeignKey(Doc, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.text

