from rest_framework import serializers
from .models import Video, Category, Comment, Like, WatchHistory

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CommentSerializer(serializers.ModelSerializer):
    user_phone = serializers.CharField(source='user.phone_number', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user_phone', 'text', 'created_at']

class VideoSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    
    is_liked = serializers.SerializerMethodField()
    is_watched = serializers.SerializerMethodField()
    has_commented = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = [
            'id', 'title', 'video_type', 'categories', 'cover_path', 
            'video_file_url', 'is_premium_only', 'likes_count', 
            'comments_count', 'views_count', 'is_liked', 'is_watched', 'has_commented'
        ]

    def _get_user(self):
        request = self.context.get('request')
        if not request:
            return None
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            return user
        
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            try:
                from rest_framework_simplejwt.authentication import JWTAuthentication
                validated_token = JWTAuthentication().get_validated_token(auth_header.split(' ')[1])
                return JWTAuthentication().get_user(validated_token)
            except Exception:
                pass
        return None

    def get_is_liked(self, obj):
        user = self._get_user()
        return obj.likes.filter(user=user).exists() if user else False

    def get_is_watched(self, obj):
        user = self._get_user()
        return WatchHistory.objects.filter(user=user, video=obj).exists() if user else False

    def get_has_commented(self, obj):
        user = self._get_user()
        return obj.comments.filter(user=user).exists() if user else False
    
class WatchHistorySerializer(serializers.ModelSerializer):
    video = VideoSerializer(read_only=True)
    class Meta:
        model = WatchHistory
        fields = ['id', 'video', 'watched_at']