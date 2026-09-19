from django.contrib import admin
from .models import Category, Video, Like, WatchHistory, Comment

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_type', 'is_premium_only', 'views_count', 'created_at')
    list_filter = ('video_type', 'is_premium_only')
    search_fields = ('title',)

admin.site.register(Category)
admin.site.register(Like)
admin.site.register(WatchHistory)
admin.site.register(Comment)