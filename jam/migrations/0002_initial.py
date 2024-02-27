# Generated by Django 5.0.2 on 2024-02-26 10:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('jam', '0001_initial'),
        ('music', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feeds',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
        migrations.AddField(
            model_name='recommended',
            name='albums',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.album'),
        ),
        migrations.AddField(
            model_name='recommended',
            name='favourite',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='jam.favourites'),
        ),
        migrations.AddField(
            model_name='recommended',
            name='genres',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.genre'),
        ),
        migrations.AddField(
            model_name='recommended',
            name='history',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.listeninghistory'),
        ),
        migrations.AddField(
            model_name='recommended',
            name='library',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.library'),
        ),
        migrations.AddField(
            model_name='recommended',
            name='like',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.like'),
        ),
        migrations.AddField(
            model_name='recommended',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
        migrations.AddField(
            model_name='recommended',
            name='songs',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.song'),
        ),
        migrations.AddField(
            model_name='recommendedplaylists',
            name='listeninghistory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.listeninghistory'),
        ),
        migrations.AddField(
            model_name='recommendedplaylists',
            name='playlists',
            field=models.ManyToManyField(to='music.playlist'),
        ),
        migrations.AddField(
            model_name='recommendedplaylists',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.song'),
        ),
        migrations.AddField(
            model_name='recommendedplaylists',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
        migrations.AddField(
            model_name='recommended',
            name='recommededplaylist',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='jam.recommendedplaylists'),
        ),
        migrations.AddField(
            model_name='similarreleases',
            name='albums',
            field=models.ManyToManyField(to='music.album'),
        ),
        migrations.AddField(
            model_name='similarreleases',
            name='songs',
            field=models.ManyToManyField(to='music.song'),
        ),
        migrations.AddField(
            model_name='recommended',
            name='similarreleases',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='jam.similarreleases'),
        ),
    ]
