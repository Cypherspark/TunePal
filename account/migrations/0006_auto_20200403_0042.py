# Generated by Django 3.0.4 on 2020-04-03 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
        ('account', '0005_auto_20200402_2340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='friends',
            field=models.ManyToManyField(blank=True, null=True, to='account.Friends'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='music',
            field=models.ManyToManyField(blank=True, null=True, to='music.User_top_music'),
        ),
    ]
