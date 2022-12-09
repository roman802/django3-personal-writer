from django.db import models
from django.contrib.auth.models import User



class Blog(models.Model):
    title = models.CharField(max_length=100, blank=True)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    detecompleted = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title

class Diskus(models.Model):
    title = models.CharField(max_length=100, blank=True)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    detecompleted = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title