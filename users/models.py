from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from music.models import Genre


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(blank=True)
    favourite_genres = models.ManyToManyField(Genre)
    view_count = models.PositiveIntegerField(default=0)
    last_viewed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Library(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='library')
    saved_songs = models.ManyToManyField('music.Song', related_name='saved_in_library', blank=True)
    saved_albums = models.ManyToManyField('music.Album', related_name='saved_in_library', blank=True)
    favorite_artists = models.ManyToManyField('music.Artist', related_name='favorite_in_library', blank=True)
    created_playlists = models.ManyToManyField('music.Playlist', related_name='created_in_library', blank=True)
    saved_playlists = models.ManyToManyField('music.Playlist', related_name='saved_in_library', blank=True)
    recently_played = models.ManyToManyField('music.Song', related_name='played_by_users', blank=True,
                                             through='ListeningHistory')

    class Meta:
        db_table = 'profile_user_library'

    def __str__(self):
        return f"Library of {self.profile.user.username}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Favourites(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.user.username} liked {self.content_object}"


class ListeningHistory(models.Model):
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user_library = models.ForeignKey(Library, on_delete=models.CASCADE)
    song = models.ForeignKey('music.Song', on_delete=models.CASCADE)
    album = models.ForeignKey('music.album', on_delete=models.CASCADE)
    listened_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'profile_listening_history'

    def __str__(self):
        return f"{self.song.title} listened at {self.listened_at}"


class Settings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=20, default='light', choices=[('light', 'Light'), ('dark', 'Dark')], help_text='Choose app theme')
    notifications_enabled = models.BooleanField(default=True, help_text='Enable notifications')
    auto_play_enabled = models.BooleanField(default=False, help_text='Enable auto-play feature')
    repeat_mode = models.CharField(max_length=20, default='none', choices=[('none', 'None'), ('all', 'All'), ('one', 'One')], help_text='Set repeat mode')
    language = models.CharField(max_length=20, default='en', help_text='Choose app language')
    download_quality = models.CharField(max_length=20, default='standard', choices=[('standard', 'Standard'), ('high', 'High'), ('lossless', 'Lossless')], help_text='Set download quality')
    streaming_quality = models.CharField(max_length=20, default='medium', choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], help_text='Set streaming quality')
    equalizer_enabled = models.BooleanField(default=False, help_text='Enable equalizer')
    local_files_access = models.BooleanField(default=False, help_text='Enable access to local files')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Settings for {self.user.username}'

