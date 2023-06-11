"""View module for handling requests about genres"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Genre, SongGenre

class GenreView(ViewSet):
    """Genre View"""

    def retrieve(self, request, pk):
        """Handle GET requests for single genre

        Returns:
          Reponse - JSON serialized genre
        """
        try:
            genre = Genre.objects.get(pk=pk)
            serializer = GenreSerializer(genre)
            return Response(serializer.data)
        except Genre.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        """Handles GET requests to get all genres

        Returns:
          Reponse - JSON serialized list of genres
        """
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST requests to create a genre

        Returns:
          Response - json serialized genre instance
        """
        genre = Genre.objects.create(
            description = request.data['description']
        )
        serializer = GenreSerializer(genre)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handles PUT requests for a genre

        Returns:
          Response - JSON serialized genre instance
        """
        genre = Genre.objects.get(pk=pk)
        genre.description = request.data['description']
        genre.save()

        serializer = GenreSerializer(genre)
        return Response(serializer.data)

    def destroy(self, request, pk):
        """Handles DELETE requests for a genre

        Returns:
          Reponse - Message confirming delete with 204 status code
        """
        genre = Genre.objects.get(pk=pk)
        genre.delete()
        return Response({'message': 'Genre deleted'}, status=status.HTTP_204_NO_CONTENT)


class SongGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongGenre
        fields = ('song_id', )
        depth = 1


class GenreSerializer(serializers.ModelSerializer):
    """Json serializer for genres
    """
    songs = SongGenreSerializer(many=True, read_only=True)
    class Meta:
        model = Genre
        fields = ('id', 'description', 'songs')
