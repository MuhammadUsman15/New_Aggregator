from django.db import models

class Article(models.Model):
    title = models.TextField()
    url = models.URLField()
    pub_date = models.DateTimeField()
    website_name = models.CharField(max_length=100, null=True)  # Allow null values
    summary = models.TextField(blank=True)
    image_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title
