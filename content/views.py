from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAuthenticatedOrReadOnly
from django.db.models import Q, F , Sum
from .models import Video, Like, WatchHistory ,Comment , Category
from .serializers import VideoSerializer ,CommentSerializer , WatchHistorySerializer , CategorySerializer


class VideoListView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        videos = Video.objects.all().order_by('-created_at')
        serializer = VideoSerializer(videos, many=True, context={'request': request})
        return Response(serializer.data)

class VideoSearchView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        query = request.query_params.get('q', '')
        if query:
            videos = Video.objects.filter(Q(title__icontains=query) | Q(categories__name__icontains=query)).distinct()
        else:
            videos = Video.objects.none()
        serializer = VideoSerializer(videos, many=True, context={'request': request})
        return Response(serializer.data)

class VideoLikeToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, video_id):
        try:
            video = Video.objects.get(id=video_id)
        except Video.DoesNotExist:
            return Response({"error": "ویدیو یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        like_obj = Like.objects.filter(user=request.user, video=video).first()
        if like_obj:
            like_obj.delete()
            liked = False
        else:
            Like.objects.create(user=request.user, video=video)
            liked = True

        return Response({"liked": liked, "likes_count": video.likes_count})

class VideoWatchView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, video_id):
        try:
            video = Video.objects.get(id=video_id)
        except Video.DoesNotExist:
            return Response({"error": "ویدیو یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if not user or not user.is_authenticated:
            auth_header = request.headers.get('Authorization', '')
            if auth_header.startswith('Bearer '):
                try:
                    from rest_framework_simplejwt.authentication import JWTAuthentication
                    validated_token = JWTAuthentication().get_validated_token(auth_header.split(' ')[1])
                    user = JWTAuthentication().get_user(validated_token)
                except Exception:
                    user = None
        if video.is_premium_only:
            if not user or not user.is_authenticated or not getattr(user, 'is_premium', False):
                return Response(
                    {"error": "این محتوا مخصوص کاربران ویژه است. لطفاً ابتدا اشتراک تهیه کنید.", "is_premium_required": True},
                    status=status.HTTP_403_FORBIDDEN
                )
        Video.objects.filter(id=video_id).update(views_count=F('views_count') + 1)
        video.refresh_from_db()

        if user and user.is_authenticated:
            WatchHistory.objects.update_or_create(user=user, video=video)

        return Response({
            "views_count": video.views_count,
            "video_url": video.video_file_url
        })
    
class ContentStatsView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        user_likes_count = 0
        user_comments_count = 0
        user_watched_count = 0

        token = request.headers.get('Authorization', None)
        if token:
            try:
                from rest_framework_simplejwt.authentication import JWTAuthentication
                auth = JWTAuthentication()
                validated_token = auth.get_validated_token(token.replace('Bearer ', ''))
                user = auth.get_user(validated_token)
                
                user_likes_count = Like.objects.filter(user=user).count()
                user_comments_count = Comment.objects.filter(user=user).count()
                user_watched_count = WatchHistory.objects.filter(user=user).count()
            except Exception:
                pass

        return Response({
            "user_likes": user_likes_count,
            "user_comments": user_comments_count,
            "user_watched": user_watched_count
        })

class VideoCommentListCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, video_id):
        comments = Comment.objects.filter(video_id=video_id).order_by('-created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, video_id):
        text = request.data.get('text', '').strip()
        if not text:
            return Response({"error": "متن نظر نمی‌تواند خالی باشد."}, status=status.HTTP_400_BAD_REQUEST)

        comment = Comment.objects.create(user=request.user, video_id=video_id, text=text)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# views_C.py
class UserWatchHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        history = WatchHistory.objects.filter(user=request.user).order_by('-id')
        serializer = WatchHistorySerializer(history, many=True, context={'request': request})
        return Response(serializer.data)

class CategoryListView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)