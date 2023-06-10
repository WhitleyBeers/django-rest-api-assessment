"""View module for handling requests about genres"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Genre

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


class GenreSerializer(serializers.ModelSerializer):
    """Json serializer for genres
    """
    class Meta:
        model = Genre
        fields = ('id', 'description')
