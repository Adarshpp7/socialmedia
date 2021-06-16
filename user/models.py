from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.utils.datetime_safe import datetime
from django.utils import timezone

# Create your models here.

class User_Profile(AbstractUser):
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    image = models.ImageField( default='profile_pic.png', upload_to='user_image/')
    bio = models.CharField(max_length=300, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10)
    followings = models.ManyToManyField("self", blank=True)
    followers = models.ManyToManyField("self", blank=True)
    friends = models.ManyToManyField("self", blank=True)
    country = models.CharField(max_length=50, blank=True)
    block_status = models.BooleanField(default=False)


 

class Post(models.Model):
    description = models.CharField(max_length=255, blank=True)
    pic = models.ImageField(upload_to='media/',blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User_Profile, on_delete=models.CASCADE)
    tags = models.CharField(max_length=100, blank=True) 
    likes_count = models.PositiveIntegerField(default=0, null=True)
    comments_count = models.PositiveIntegerField(default=0, null=True)


class Comments(models.Model):
	post = models.ForeignKey(Post, related_name='details', on_delete=models.CASCADE)
	user = models.ForeignKey(User_Profile, related_name='details', on_delete=models.CASCADE)
	comment = models.CharField(max_length=255)
	comment_date = models.DateTimeField(default=timezone.now)

class Like(models.Model):
	user = models.ForeignKey(User_Profile, related_name='likes', on_delete=models.CASCADE)
	post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)


class Followings(models.Model):
	to_user = models.ForeignKey(User_Profile, related_name='to_user', on_delete=models.CASCADE)
	from_user = models.ForeignKey(User_Profile, related_name='from_user', on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)

 
class Followers(models.Model):
	to_user = models.ForeignKey(User_Profile, related_name='user_to', on_delete=models.CASCADE)
	from_user = models.ForeignKey(User_Profile, related_name='user_from', on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)

class Users_Room(models.Model):
    user1 = models.ForeignKey(User_Profile,on_delete=models.CASCADE,related_name='%(class)s_requests_created')
    user2 = models.ForeignKey(User_Profile,on_delete=models.CASCADE,related_name='%(class)s_requests_reciever') 
    room_name = models.CharField(max_length=100)
    
class Messages(models.Model):
    sender = models.ForeignKey(User_Profile,on_delete=models.CASCADE,related_name='%(class)s_requests_sender')
    receiver = models.ForeignKey(User_Profile, on_delete=models.CASCADE,related_name='%(class)s_requests_reciever')
    users_room = models.ForeignKey(Users_Room, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    msg_type = models.CharField(max_length=15,null=True)
    upload_file = models.FileField(upload_to='files',null=True,default='')
    
    @property
    def getfile(self):
        if self.msg_type == 'image' or self.msg_type == 'video' or self.msg_type == 'audio':
            url = self.upload_file.url
        else:
            url = ''
        return url


    