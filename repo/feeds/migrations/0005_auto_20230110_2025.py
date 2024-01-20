# Generated by Django 3.1.5 on 2023-01-10 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0004_auto_20230109_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='latitude',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='위도'),
        ),
        migrations.AddField(
            model_name='feed',
            name='longitude',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='경도'),
        ),
    ]
