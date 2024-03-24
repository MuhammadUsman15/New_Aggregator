from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
# User = get_user_model()
# class Profile(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE)

#     interests = models.CharField()

class Article(models.Model):
    title = models.TextField()
    url = models.URLField()
    pub_date = models.DateTimeField()
    source = models.TextField()
    summary = models.TextField(blank=True)
    image_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title

