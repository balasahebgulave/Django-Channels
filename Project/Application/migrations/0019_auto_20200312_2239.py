# Generated by Django 3.0.1 on 2020-03-12 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0018_auto_20200227_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userseed',
            name='username',
            field=models.CharField(default='None', max_length=100),
        ),
    ]