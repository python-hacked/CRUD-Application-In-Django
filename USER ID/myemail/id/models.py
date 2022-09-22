from django.db import models
# SIGNAL hear 
from django.contrib.auth.models import User
from PIL import Image
 


# Create your models here.
# create SIGNAL models
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
 
    def __str__(self):
        return f'{self.user.username} Profile'

# create person class Model
class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    Company_name =models.CharField(max_length=200)
    Email_name =models.CharField(max_length=200) 
    Phone_number =models.CharField(max_length=10)
    Subject_name =models.CharField(max_length=100)
    Password =models.CharField(max_length=500,blank=True,null=True)
    address = models.TextField()
    is_active=models.BooleanField(default=True)






