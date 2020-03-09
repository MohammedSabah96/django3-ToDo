from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tasks(models.Model):
    title=models.CharField(max_length=25)
    memo=models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    dateCompleted=models.DateTimeField(blank=True,null=True)
    importand = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.title