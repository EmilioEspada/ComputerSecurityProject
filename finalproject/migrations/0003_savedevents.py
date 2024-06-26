# Generated by Django 4.2.7 on 2023-11-30 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finalproject', '0002_userprofile_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedEvents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=64)),
                ('image', models.CharField(default='', max_length=64)),
                ('date', models.CharField(default='', max_length=64)),
                ('time', models.CharField(default='', max_length=64)),
                ('venue', models.CharField(default='', max_length=64)),
                ('city', models.CharField(default='', max_length=64)),
                ('state', models.CharField(default='', max_length=64)),
                ('address', models.CharField(default='', max_length=64)),
                ('link', models.CharField(default='', max_length=128)),
            ],
        ),
    ]
