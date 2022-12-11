from django.db import models


class Checks(models.Model):
    objects = None
    name = models.CharField(max_length=150, verbose_name='Назва принтера')
    api_key = models.CharField(max_length=150, verbose_name='Ключ доступу до API')
    check_type = models.BooleanField(max_length=150, verbose_name='Чек для клієнта ?', blank=True)
    point_id = models.IntegerField(verbose_name='ID Принтера')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Checks'
        ordering = ['api_key', 'name', 'check_type', 'point_id']
