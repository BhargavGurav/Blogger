from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AppUser(models.Model):
    user = models.OneToOneField(User,  on_delete=models.CASCADE)
    profile_pic = models.FileField(upload_to='Profile_Pics')

    def __str__(self):
        return self.user.email
    

class Blogs(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    heading = models.CharField(max_length=255)
    # user_id = models.IntegerField()

    data = models.TextField()
    picture = models.FileField(upload_to='Blogs_Images')

    
