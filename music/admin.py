from django.contrib import admin
from .models import Genre, Artist, Album, Song, Playlist, UserProfile, UserLibrary, AudioFile
import ffmpeg

# Register your models here
admin.site.register(Genre)
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Playlist)
admin.site.register(UserProfile)
admin.site.register(UserLibrary)


# Convert to mp3

def convert_to_mp3(modeladmin, request, queryset):
    for audio_file in queryset:
        input_file_path = audio_file.audio.path
        output_file_path = f'{input_file_path[:-4]}.mp3'  # Generate output file path

        try:
            ffmpeg.input(input_file_path).output(output_file_path, codec='libmp3lame', bitrate='320k').run()
        except Exception as e:
            modeladmin.message_user(request, f'Error during audio conversion: {str(e)}', level='ERROR')
        else:
            modeladmin.message_user(request, f'{audio_file.title} has been successfully converted to MP3.')


convert_to_mp3.short_description = 'Convert selected audio files to MP3'


class AudioFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'audio_file')
    actions = [convert_to_mp3]


if not admin.site.is_registered(AudioFile):
    admin.site.register(AudioFile, AudioFileAdmin)
