from rest_framework import serializers
from .models import Comment, Favorite


class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    attraction_name = serializers.CharField(source='attraction.name', read_only=True)
    attraction_id = serializers.IntegerField(source='attraction.id', read_only=True)
    cover_image = serializers.CharField(source='attraction.cover_image', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user_name', 'attraction_name', 'attraction_id', 'cover_image', 'content', 'rating', 'status', 'created_at']


class CommentCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'attraction', 'content', 'rating', 'status']


class FavoriteSerializer(serializers.ModelSerializer):
    attraction_name = serializers.CharField(source='attraction.name', read_only=True)
    attraction_cover = serializers.CharField(source='attraction.cover_image', read_only=True)
    attraction_category = serializers.CharField(source='attraction.category', read_only=True)
    attraction_address = serializers.CharField(source='attraction.address', read_only=True)
    attraction_rating = serializers.DecimalField(source='attraction.rating', max_digits=2, decimal_places=1, read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'attraction', 'attraction_name', 'attraction_cover', 'attraction_category', 'attraction_address', 'attraction_rating', 'created_at']


class FavoriteCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Favorite
        fields = ['id', 'attraction', 'user']
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['user', 'attraction'],
                message='您已收藏过该景点'
            )
        ]
