"""View module for handling requests about artists"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Artist

class ArtistView(ViewSet):
    """Artist View"""

    def retrieve(self, request, pk):
        """Handle GET requests for single artist

        Returns:
          Reponse - JSON serialized artist
        """
        try:
            artist = Artist.objects.get(pk=pk)
            serializer = ArtistSerializer(artist)
            return Response(serializer.data)
        except Artist.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all artists

        Returns:
          Reponse - JSON serialized list of artists
        """
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST requests to create an artist

        Returns:
          Reponse - JSON serialized artist instance
        """
        artist = Artist.objects.create(
            name = request.data['name'],
            age = request.data['age'],
            bio = request.data['bio'],
        )
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handles PUT requests for an artist
        
        Returns:
          Response - JSON serialized artist instance
        """
        
        artist = Artist.objects.get(pk=pk)
        artist.name = request.data['name']
        artist.age = request.data['age']
        artist.bio = request.data['bio']
        artist.save()
        
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)


class ArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for artists
    """
    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio')
        depth = 1
