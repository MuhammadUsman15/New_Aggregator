from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Name of the category

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.TextField()
    url = models.URLField()
    pub_date = models.DateTimeField()
    website_name = models.CharField(max_length=100, null=True)
    summary = models.TextField(blank=True)
    image_url = models.URLField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    categories = models.ManyToManyField(Category)  # Many-to-Many relationship with Category model

    def __str__(self):
        return self.title
