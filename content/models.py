from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام دسته‌بندی")

    def __str__(self):
        return self.name

class Video(models.Model):
    TYPE_CHOICES = (
        ('movie', 'فیلم'),
        ('series', 'سریال'),
    )
    title = models.CharField(max_length=255, verbose_name="عنوان")
    video_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='movie', verbose_name="نوع")
    categories = models.ManyToManyField(Category, related_name='videos', blank=True, verbose_name="دسته‌بندی‌ها")
    cover_path = models.CharField(max_length=255, default='image/movies/m1.jpeg', verbose_name="مسیر کاور در استاتیک")
    
    video_file_url = models.URLField(blank=True, null=True, verbose_name="لینک فایل ویدیو")
    is_premium_only = models.BooleanField(default=False, verbose_name="مخصوص کاربران ویژه")
    views_count = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def likes_count(self):
        return self.likes.count()
    
    @property
    def comments_count(self):
        return self.comments.count()

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'video')

class WatchHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='watch_history')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='watched_by')
    watched_at = models.DateTimeField(auto_now=True)
    

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(verbose_name="متن نظر")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.video.title}"