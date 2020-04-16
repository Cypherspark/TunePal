from rest_framework import serializers
from music.models import User_top_music


class UserTopSongserialize(serializers.ModelSerializer):
    class Meta:
        model = User_top_music
        fields = ['artist_name','music_name','album']
