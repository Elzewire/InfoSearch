# Generated by Django 3.1.7 on 2021-04-05 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='document',
            options={'verbose_name': 'Документ', 'verbose_name_plural': 'Документы'},
        ),
        migrations.AddField(
            model_name='document',
            name='name',
            field=models.CharField(default='name', max_length=128, verbose_name='Название'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(upload_to='', verbose_name='Файл документа'),
        ),
        migrations.AlterField(
            model_name='document',
            name='index',
            field=models.IntegerField(verbose_name='Индекс'),
        ),
        migrations.AlterField(
            model_name='document',
            name='url',
            field=models.URLField(verbose_name='Ссылка'),
        ),
    ]