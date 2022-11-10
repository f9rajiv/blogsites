from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse #reverse from class


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to="profile_pics", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone_no = models.IntegerField(blank=True, null=True)
    facebook = models.CharField(max_length=300, blank=True, null=True)
    instagram = models.CharField(max_length=300, blank=True, null=True)
    linkedin = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return str(self.user)
class Post(models.Model):
    # post_id=models.AutoField(primary_key=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE) #only person has power i.e. create superuser can do all
    title= models.CharField(max_length=200)
    text=models.TextField()
    image = models.ImageField(upload_to="photos", blank=True, null=True)
    # slug=models.CharField(max_length=100)
    created_date=models.DateTimeField(default=timezone.now)
    published_date=models.DateTimeField(blank=True,null=True)

#add method
    def publish(self):
        self.published_date =timezone.now()
        self.save()
    #
    # def approve_comments(self):
    #     return self.approve_comments.filter(approved_comments=True)

    def get_absolute_url(self):
        return reverse('post_detail',kwargs={'pk':self.pk})  #classbasedview refer,where should we go after creating post here it goes to post detail page

    def __str__(self):
        return str(self.author) +  " Blog Title: " + self.title

class Comment(models.Model):
   post=models.ForeignKey('blog.Post',related_name='comments',on_delete=models.CASCADE)
   writer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
   text=models.TextField()
   created_date=models.DateTimeField(default=timezone.now)
   approved_comments=models.BooleanField(default=False)

   def approve(self):
       self.approved_comments=True
       self.save()

   def get_absolute_url(self):
       return reverse('post_list') #return to list of post

   def __str__(self):
       return self.text
