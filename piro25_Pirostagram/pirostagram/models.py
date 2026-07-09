from django.db import models
from django.contrib.auth.models import User

# 1. 게시글 
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='posts/images/') 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(User, related_name='like_posts', blank=True)

    def __str__(self):
        return f"{self.author.username}의 게시글 - {self.id}"

# 2. 댓글 
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}의 댓글: {self.content[:10]}"

# 3. 좋아요
class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_posts')

    class Meta:
        # 한 유저가 하나의 게시글에 좋아요를 중복으로 누르는 것을 방지
        unique_together = ('post', 'user')

# 4. 팔로우
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f"{self.follower.username} 가 {self.following.username}을 팔로우함"
    
# 5. 스토리
class Story(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    image = models.ImageField(upload_to='stories/images/')
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.author.username}의 스토리 - {self.id}"