# Generated by Django 3.0.9 on 2020-09-17 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='description',
            field=models.TextField(default='', max_length=255, null=True, verbose_name='Description'),
        ),
    ]
