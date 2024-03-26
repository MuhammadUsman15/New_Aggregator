from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.TextField()
    url = models.URLField()
    pub_date = models.DateTimeField()
    website_name = models.CharField(max_length=100, null=True)  # Allow null values
    summary = models.TextField(blank=True)
    image_url = models.URLField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True)  # ForeignKey relationship with User model

    def __str__(self):
        return self.title
