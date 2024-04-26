# Generated by Django 4.1.5 on 2024-02-13 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mathapp', '0002_mathstatistics_count10_correct_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mathstatistics',
            name='correct_answers',
        ),
        migrations.RemoveField(
            model_name='mathstatistics',
            name='exercise_type',
        ),
        migrations.RemoveField(
            model_name='mathstatistics',
            name='wrong_answers',
        ),
        migrations.AddField(
            model_name='mathstatistics',
            name='timer',
            field=models.IntegerField(default=None, verbose_name='timer'),
        ),
        migrations.AlterField(
            model_name='mathstatistics',
            name='total',
            field=models.IntegerField(default=None, verbose_name='Всего'),
        ),
    ]