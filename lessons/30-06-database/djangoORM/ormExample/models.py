from django.db import models

# Create your models here.

class Event(models.Model):
    place = models.CharField(max_length=50)
    date = models.DateTimeField()
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
