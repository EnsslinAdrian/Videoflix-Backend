from rest_framework import serializers
from movie_app.models import Movie

class MovieSerializer(serializers.ModelSerializer):
    movie_url = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'

    def get_movie_url(self, obj):
        request = self.context.get('request')
        if obj.movie_url:
            # Verwende richtigen .m3u8-Dateinamen (hier: 720p.m3u8)
            url = obj.movie_url.url.replace("original.mp4", "1080p.m3u8")
            return request.build_absolute_uri(url)
        return None

class TrailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

 
        