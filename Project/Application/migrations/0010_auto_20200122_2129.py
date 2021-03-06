# Generated by Django 3.0.1 on 2020-01-22 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0009_auto_20200121_2105'),
    ]

    operations = [
        migrations.AddField(
            model_name='userseed',
            name='emailto',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AddField(
            model_name='userseed',
            name='forwardto',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AddField(
            model_name='userseed',
            name='port',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AddField(
            model_name='userseed',
            name='proxypass',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AddField(
            model_name='userseed',
            name='proxyuser',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AddField(
            model_name='userseed',
            name='seedlog',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AddField(
            model_name='userseed',
            name='tasklog',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AddField(
            model_name='userseed',
            name='taskprofile',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AddField(
            model_name='userseed',
            name='team',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
