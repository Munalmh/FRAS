# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.ForeignKey(User ,on_delete=models.SET_NULL,null=True, blank=True)
    name=models.CharField(max_length=70)
    rollno=models.IntegerField(unique=True)
    phoneno=models.IntegerField()
    address=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    photo = models.ImageField(upload_to='student_photos/',default='none')

def __str__(self):
        return self.name