from django.db import models

# Create your models here.

class Review(models.Model):
    reviewText = models.CharField(max_length=200)
    location = models.CharField(default="",max_length=200)
    author = models.CharField('Author',max_length=200)
