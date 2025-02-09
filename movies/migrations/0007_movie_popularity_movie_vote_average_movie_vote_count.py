# Generated by Django 5.1.5 on 2025-02-09 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_remove_movie_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='popularity',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='movie',
            name='vote_average',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='movie',
            name='vote_count',
            field=models.IntegerField(default=0),
        ),
    ]
