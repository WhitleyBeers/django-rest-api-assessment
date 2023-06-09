"""View module for handling requests about songs"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Song, Artist, SongGenre

class SongView(ViewSet):
    """Song view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single song

        Returns:
          Reponse - JSON serialized song
        """
        try:
            song = Song.objects.get(pk=pk)
            serializer = SongSerializer(song)
            return Response(serializer.data)
        except Song.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all songs

        Returns:
          Reponse - JSON serialized list of songs
        """
        songs = Song.objects.all()
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST requests to create a song

        Returns:
          Reponse - JSON serialized song instance
        """
        artist = Artist.objects.get(pk=request.data["artist_id"])

        song = Song.objects.create(
            title = request.data['title'],
            artist_id = artist,
            album = request.data['album'],
            length = request.data['length'],
        )
        serializer = SongSerializer(song)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a song

        Returns:
          Response - JSON serialized song instance
        """

        song = Song.objects.get(pk=pk)
        song.title = request.data['title']
        song.album = request.data['album']
        song.length = request.data['length']
        artist_id = Artist.objects.get(pk=request.data['artist_id'])
        song.artist_id = artist_id
        song.save()

        serializer = SongSerializer(song)
        return Response(serializer.data)

    def destroy(self, request, pk):
        """Handles DELETE requests for a song

        Return:
          Response - Empty body with 204 status code
        """
        song = Song.objects.get(pk=pk)
        song.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class SongGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongGenre
        fields = ('genre_id', )
        depth = 1


class SongSerializer(serializers.ModelSerializer):
    """JSON serializer for songs
    """
    genres = SongGenreSerializer(many=True, read_only=True)
    class Meta:
        model = Song
        fields = ('id', 'title', 'artist_id',
                  'album', 'length', 'genres')
        depth = 1
