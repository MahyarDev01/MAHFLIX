from django.urls import path
from .views import VideoListView, VideoSearchView, VideoLikeToggleView,CategoryListView, VideoWatchView , ContentStatsView , VideoCommentListCreateView, UserWatchHistoryView

urlpatterns = [
    path('list/', VideoListView.as_view(), name='video-list'),
    path('search/', VideoSearchView.as_view(), name='video-search'),
    path('<int:video_id>/like/', VideoLikeToggleView.as_view(), name='video-like-toggle'),
    path('<int:video_id>/watch/', VideoWatchView.as_view(), name='video-watch'),
    path('stats/', ContentStatsView.as_view(), name='content-stats'),
    path('<int:video_id>/comments/', VideoCommentListCreateView.as_view(), name='video-comments'),
    path('history/', UserWatchHistoryView.as_view(), name='user_watch_history'), 
    path('categories/', CategoryListView.as_view(), name='category-list'),
]