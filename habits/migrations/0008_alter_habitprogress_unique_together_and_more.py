# Generated by Django 5.2.1 on 2025-06-18 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0007_habitprogress_points_earned'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='habitprogress',
            unique_together={('habit', 'date')},
        ),
        migrations.RemoveField(
            model_name='reward',
            name='effect_value',
        ),
        migrations.AlterField(
            model_name='habit',
            name='emoji',
            field=models.CharField(default='🌱', max_length=10),
        ),
        migrations.AlterField(
            model_name='reward',
            name='reward_type',
            field=models.CharField(choices=[('daily_break', 'Día de Descanso'), ('streak_booster', 'Impulso de Racha'), ('theme', 'Tema Especial')], default=None, max_length=20),
        ),
        migrations.RemoveField(
            model_name='habitprogress',
            name='points_earned',
        ),
    ]
