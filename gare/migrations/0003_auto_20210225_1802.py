# Generated by Django 2.0 on 2021-02-25 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gare', '0002_altrifile_lotto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='altrifile',
            name='lotto',
        ),
        migrations.AddField(
            model_name='garapubblica',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='File_gare/%Y/%m/%d', verbose_name='Altri file'),
        ),
    ]
