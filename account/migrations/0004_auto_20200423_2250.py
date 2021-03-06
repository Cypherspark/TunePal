# Generated by Django 3.0.5 on 2020-04-23 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_auto_20200423_2250'),
        ('account', '0003_auto_20200423_2250'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='artists',
            field=models.ManyToManyField(blank=True, default=None, to='music.Artist'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='tracks',
            field=models.ManyToManyField(blank=True, to='music.Music'),
        ),
    ]
