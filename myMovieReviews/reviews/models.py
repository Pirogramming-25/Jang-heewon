from django.db import models

# Create your models here.
class Review (models.Model):
    
    GENRE_CHOICES = [
        ('action', '액션'),
        ('romance', '로맨스'),
        ('comedy', '코미디'),
        ('thriller', '스릴러'),
        ('sf', 'SF'),
        ('drama', '드라마'),
    ]

    
    title = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    actor = models.CharField(max_length=100)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES, default='action')
    star = models.IntegerField()
    time = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    

def __str__(self):
    return self.title