from django.db import models

# Create your models here.
 
class News(models.Model):
    author = models.CharField(max_length=255,null=True)
    title = models.CharField(max_length=255,null=True)
    country = models.CharField(max_length=255,null=True)
    category = models.CharField(max_length=255,null=True)
    query = models.CharField(max_length=255,null=True)
    description = models.TextField(null=True)
    url = models.URLField(null=True)
    published_at = models.DateTimeField(null=True)
    content = models.TextField(null=True)
    
 