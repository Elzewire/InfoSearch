from django.db import models


class Document(models.Model):
    index = models.IntegerField(verbose_name='Индекс')
    url = models.URLField(verbose_name='Ссылка')
    name = models.CharField(max_length=128, verbose_name='Название')
    file = models.FileField(verbose_name='Файл документа')

    def __str__(self):
        return "{} {}".format(self.index, self.name)

    class Meta:
        ordering = ['index']
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
