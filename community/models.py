# community/models.py

from django.db import models
from django.contrib.auth.models import User

class BoardType(models.TextChoices):
    DEVELOPMENT = 'development', '개발과정'
    FREE = 'free', '시끌시끌'

class Post(models.Model):
    board_type = models.CharField(max_length=20, choices=BoardType.choices)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"[{self.get_board_type_display()}] {self.title}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.content[:20]}"
