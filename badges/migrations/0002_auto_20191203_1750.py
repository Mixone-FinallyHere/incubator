# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-12-03 16:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('badges', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='badge',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='badgewear',
            name='action_counter',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='badgewear',
            name='attributor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributed', to=settings.AUTH_USER_MODEL, verbose_name='Attributeur'),
        ),
        migrations.AlterField(
            model_name='badgewear',
            name='level',
            field=models.CharField(choices=[('RAC', 'Raclure de bidet'), ('INI', 'Initié'), ('DIS', 'Disciple'), ('MAI', 'Maître')], default='INI', max_length=3),
        ),
        migrations.AlterUniqueTogether(
            name='badgewear',
            unique_together=set([('user', 'badge')]),
        ),
    ]
