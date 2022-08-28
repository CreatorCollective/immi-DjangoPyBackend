from django.db import models

# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.CharField(max_length=256, null=True, blank=True)

class Counters(models.Model):
    counter_name = models.CharField(max_length=256)
    total_views = models.BigIntegerField()