# from curses import flash
from django.db import models
from django.core.files.storage import FileSystemStorage
from datetime import date


# Create your models here.


def get_upload_path(instance, filename):
    new_filename= f"{instance.roll_no}_{instance.first_name}_{filename}"
    return '{0}/{1}'.format(instance.first_name, new_filename)

def get_upload_paths(instance, filename):
    return '{0}/{1}'.format(instance.stu_name, filename)


class Student(models.Model):
    SEX_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female')
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length = 100)
    roll_no = models.IntegerField(unique=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    age = models.IntegerField(default=0)
    phone_no = models.IntegerField(default = 0)
    email = models.EmailField(blank = True,max_length=256)
    image = models.ImageField(upload_to = get_upload_path, blank = False, null = False)
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class ImageForm(models.Model):
    stu_name = models.CharField(max_length=255)
    image_field = models.FileField(upload_to = get_upload_paths, blank = False, null = False)
    def __str__(self):
        return f"{self.stu_name}"





