from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
# User = get_user_model()
# class Profile(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE)

#     interests = models.CharField()

class Article(models.Model):
    title = models.CharField()
    url = models.URLField()
    pub_date = models.DateTimeField()
    source = models.CharField()
    summary = models.TextField(blank=True)

    def __str__(self):
        return self.title
