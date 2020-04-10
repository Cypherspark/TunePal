# Generated by Django 3.0.4 on 2020-04-02 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('music_name', models.CharField(max_length=250)),
                ('artist_name', models.CharField(max_length=250)),
                ('genre', models.CharField(max_length=250)),
                ('album', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='User_top_music',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('music_name', models.CharField(max_length=250)),
                ('artist_name', models.CharField(max_length=250)),
                ('genre', models.CharField(max_length=250)),
                ('album', models.CharField(max_length=250)),
                ('music_id', models.CharField(max_length=250)),
            ],
        ),
    ]