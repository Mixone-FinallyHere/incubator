# Generated by Django 3.0.9 on 2020-08-07 00:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='completed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='completed_tasks', to=settings.AUTH_USER_MODEL, verbose_name='Réalisé par'),
        ),
        migrations.AddField(
            model_name='task',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='projects.Project', verbose_name='Projet'),
        ),
        migrations.AddField(
            model_name='task',
            name='proposed_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='proposed_tasks', to=settings.AUTH_USER_MODEL, verbose_name='Proposé par'),
        ),
        migrations.AddField(
            model_name='project',
            name='dependencies',
            field=models.ManyToManyField(blank=True, related_name='_project_dependencies_+', to='projects.Project', verbose_name='Dépendences'),
        ),
        migrations.AddField(
            model_name='project',
            name='maintainer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='maintained_projects', to=settings.AUTH_USER_MODEL, verbose_name='Mainteneur'),
        ),
        migrations.AddField(
            model_name='project',
            name='participants',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
