# Generated by Django 3.0.4 on 2020-03-29 21:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(blank=True, null=True, verbose_name='latitude')),
                ('longitude', models.FloatField(blank=True, null=True, verbose_name='longitude')),
                ('country', models.CharField(blank=True, max_length=30, verbose_name='country')),
                ('province', models.CharField(blank=True, max_length=30, verbose_name='province')),
                ('neighbourhood', models.CharField(blank=True, max_length=30, verbose_name='neighbourhood')),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='location',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.UserLocation', verbose_name='location'),
        ),
    ]
