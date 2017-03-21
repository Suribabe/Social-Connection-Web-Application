from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime
import uuid
class Profile(models.Model):
	"""docstring for User"""
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	firstname=models.CharField(max_length=50, default='')
	lastname=models.CharField(max_length=50,default='')
	bio=models.TextField(max_length=420,blank=True)
	age=models.CharField(max_length=10,blank=True)
	picture = models.ImageField(upload_to="profile-photos",blank=True)
	activeToken=models.CharField(max_length=500, blank=True)
	follows=models.ManyToManyField('Profile',related_name='followed_by',symmetrical=False)
	email= models.EmailField(default='')

class Post(models.Model):
	"""docstring for Post"""
	text=models.TextField(max_length=42)
	time=models.DateTimeField(auto_now_add=True)
	profile=models.ForeignKey(Profile,null=True)

	def __unicode__(self):
		return self.text

class Comment(models.Model):
	"""docstring for comment"""
	text=models.TextField(max_length=42)
	time=models.DateTimeField(auto_now_add=True)
	profile=models.ForeignKey(Profile,null=True)
	post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True)
	def __unicode__(self):
		return self.text
	def __str__():
		return self.created_date	

