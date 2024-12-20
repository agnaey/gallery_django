from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class gallery (models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    file_id=models.TextField()
    name = models.TextField()
    file = models.FileField()
    images=models.BooleanField(default=False)
    video=models.BooleanField(default=False)
    audio=models.BooleanField(default=False)
    others=models.BooleanField(default=False)

    def __str__(self):
        return self.name

class favorite(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    gallery=models.ForeignKey(gallery,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
