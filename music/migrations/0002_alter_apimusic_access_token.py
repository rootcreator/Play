# Generated by Django 5.0.2 on 2024-02-22 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apimusic',
            name='access_token',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
