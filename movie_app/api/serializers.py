from rest_framework import serializers
from movie_app.models import Movie

class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer for the Movie model.

    Replaces the original movie file URL with the 1080p HLS playlist URL.
    """
    movie_url = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'

    def get_movie_url(self, obj):
        request = self.context.get('request')
        if obj.movie_url:
            url = obj.movie_url.url.replace("original.mp4", "1080p.m3u8")
            return request.build_absolute_uri(url)
        return None

class TrailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

 
        