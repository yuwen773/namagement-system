from rest_framework import serializers
from .models import Comment, Favorite


class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    attraction_name = serializers.CharField(source='attraction.name', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user_name', 'attraction_name', 'content', 'rating', 'status', 'created_at']


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['attraction', 'content', 'rating']


class FavoriteSerializer(serializers.ModelSerializer):
    attraction_name = serializers.CharField(source='attraction.name', read_only=True)
    attraction_cover = serializers.ImageField(source='attraction.cover_image', read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'attraction', 'attraction_name', 'attraction_cover', 'created_at']


class FavoriteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['attraction']
