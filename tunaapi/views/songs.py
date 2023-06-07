"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Song, Artist

class SongView(ViewSet):
    """Song view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single song

        Returns:
          Reponse - JSON serialized song type
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


class SongSerializer(serializers.ModelSerializer):
    """JSON serializer for songs
    """
    class Meta:
        model = Song
        fields = ('id', 'title', 'artist_id',
                  'album', 'length')
        depth = 1
