from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class gallery (models.Model):
    file_id=models.TextField()
    name = models.TextField()
    file = models.FileField()
    images=models.BooleanField(default=False)
    video=models.BooleanField(default=False)
    audio=models.BooleanField(default=False)
    others=models.BooleanField(default=False)

class favorite(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    gallery=models.ForeignKey(gallery,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
