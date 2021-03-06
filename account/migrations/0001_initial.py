# Generated by Django 3.0.5 on 2020-04-17 20:01

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('music', '0001_initial'),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=10)),
                ('nickname', models.CharField(blank=True, max_length=30, verbose_name='nickname')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('birthdate', models.DateField(null=True)),
                ('biography', models.CharField(blank=True, max_length=150, null=True, verbose_name='biography')),
                ('interests', models.CharField(blank=True, max_length=30, null=True, verbose_name='interests')),
                ('user_avatar', models.ImageField(blank=True, upload_to='images/')),
                ('spotify_token', models.CharField(blank=True, max_length=700, null=True, verbose_name='spotify token')),
                ('status', models.CharField(blank=True, max_length=10)),
                ('file', models.FileField(blank=True, default=None, upload_to='')),
                ('top_artist', models.CharField(blank=True, max_length=100)),
                ('score', models.CharField(blank=True, default='0', max_length=100000000)),
                ('assigned', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='music.Music')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
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
        migrations.CreateModel(
            name='Suggest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_current_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='s_owner', to=settings.AUTH_USER_MODEL)),
                ('s_users', models.ManyToManyField(blank=True, related_name='s_users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(blank=True, related_name='friends', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='location',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.UserLocation', verbose_name='location'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='music',
            field=models.ManyToManyField(blank=True, to='music.User_top_music'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
