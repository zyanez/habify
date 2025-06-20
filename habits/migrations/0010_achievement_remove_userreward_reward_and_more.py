# Generated by Django 5.2.1 on 2025-06-18 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0009_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('condition', models.CharField(max_length=50)),
                ('badge_value', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='userreward',
            name='reward',
        ),
        migrations.RemoveField(
            model_name='userreward',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='achievements',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='theme',
            field=models.CharField(choices=[('light', 'Claro'), ('dark', 'Oscuro')], default='light', max_length=20),
        ),
        migrations.DeleteModel(
            name='Reward',
        ),
        migrations.DeleteModel(
            name='UserReward',
        ),
    ]
