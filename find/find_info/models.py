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
    name = models.CharField(max_length=100, verbose_name='Name', null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    link = models.CharField(max_length=150, verbose_name='Storage location', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'About document'
        ordering = ['name', 'updated_at', 'link']


class LineOfDoc(models.Model):
    line_number = models.IntegerField(verbose_name='Line number')
    text = models.CharField(max_length=600, verbose_name='Line text')
    doc = models.ForeignKey(Doc, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.text


class WordOfDoc(models.Model):
    text = models.CharField(max_length=100, verbose_name='Word', db_index=True)
    line = models.ForeignKey(LineOfDoc, on_delete=models.CASCADE, null=True)
    doc = models.ForeignKey(Doc, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.text


class Checkbox(models.Model):
    user = models.CharField(max_length=100, verbose_name='User')
    session = models.TextField(blank=True)

