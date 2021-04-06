from django.db import models


class Document(models.Model):
    index = models.IntegerField(verbose_name='Индекс')
    url = models.URLField(verbose_name='Ссылка')
    name = models.CharField(max_length=128, verbose_name='Название')
    file = models.FileField(verbose_name='Файл документа')

    def __str__(self):
        return "{} {}".format(self.index, self.name)

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'


class Index(models.Model):
    lemma = models.CharField(max_length=48, verbose_name='Лемма')
    index = models.IntegerField(verbose_name='Индекс')

    def __str__(self):
        return "{} {}".format(self.lemma, self.index)

    class Meta:
        verbose_name = 'Инвертированный индекс'
        verbose_name_plural = 'Инвертированные индексы'
