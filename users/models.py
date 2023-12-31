from django.db import models
from django.contrib.auth.models import User
from music.models import Song, Artist, Playlist, Album  # Importing models from the music app


# Model representing additional profile information for a user
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')  # One-to-one relationship with the User model
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)  # Field to store profile pictures
    bio = models.TextField(blank=True)  # Field to store user biography information

    # Other fields as needed for user-specific data

    # Method to create a user profile when a User instance is created
    def create_user_profile(cls, sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    class Meta:
        db_table = 'profile_user_profile'  # Custom table name for the UserProfile model

    def __str__(self):
        return self.user.username  # String representation of the UserProfile instance


# Model representing a user's library
class UserLibrary(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='library')  # One-to-one relationship with UserProfile
    saved_songs = models.ManyToManyField(Song, related_name='saved_in_libraries', blank=True)  # Many-to-many relationship with Song model for saved songs
    saved_albums = models.ManyToManyField(Album, related_name='saved_in_libraries', blank=True)  # Many-to-many relationship with Album model for saved albums
    favorite_artists = models.ManyToManyField(Artist, related_name='favorited_in_libraries', blank=True)  # Many-to-many relationship with Artist model for favorite artists
    created_playlists = models.ManyToManyField(Playlist, related_name='created_in_libraries', blank=True)  # Many-to-many relationship with Playlist model for created playlists

    # Add other fields or relationships as needed for the user's library

    class Meta:
        db_table = 'profile_user_library'  # Custom table name for the UserLibrary model

    def __str__(self):
        return f"Library of {self.user_profile.user.username}"  # String representation of the UserLibrary instance


# Model representing the views of a user's profile
class UserProfileView(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='profile_views')  # One-to-one relationship with UserProfile
    view_count = models.PositiveIntegerField(default=0)  # Field to store the count of profile views
    last_viewed = models.DateTimeField(auto_now=True)  # Field to store the timestamp of the last view

    class Meta:
        db_table = 'profile_user_profile_view'  # Custom table name for the UserProfileView model

    def __str__(self):
        return f"Profile views of {self.user_profile.user.username}"  # String representation of the UserProfileView instance
