from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Idea(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='ideas/')
    content = models.TextField()
    interest = models.IntegerField(default=0)
    devtools = models.ManyToManyField('tools.DevTool', related_name='ideas')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class IdeaStar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='stars')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'idea')  

    def __str__(self):
        return f"{self.user.username} - {self.idea.title}"