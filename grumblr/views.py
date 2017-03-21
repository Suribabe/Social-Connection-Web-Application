from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import transaction
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from django.http import HttpResponse, Http404
from grumblr.models import *
from grumblr.forms import *

from django.contrib.auth.tokens import default_token_generator

#used to send mail from within Django
from django.core.mail import send_mail

#Helper function to guess a MIME type from a file name
from mimetypes import guess_type
from django.core import serializers
import requests
import json
import time
from django.utils.timezone import localtime
from django.utils.formats import get_format
from django.utils.dateformat import DateFormat
current_milli_time = lambda: int(round(time.time() * 1000))
# Create your views here.
context={}


@login_required
def home(request):	
	context={}

	# context['form'] = PostForm()

	posts=Post.objects.order_by("-time")
	comments=Comment.objects.all()
	comments=comments.order_by("-time")
	try:
		last_post_id=Post.objects.latest('id').id
	except ObjectDoesNotExist:
		last_post_id =0
	context={'posts':posts,
	'comments':comments,
	"last_post_id":last_post_id,
	'form':PostForm()
	}
	return render(request,'main.html',context)

# def login(request):
# 	error=[]
# 	if not 'username' in request.POST or not request.POST['username']:
# 		error.append('please enter your username')
# 	elif not 'password' in request.POST or not request.POST['password']:
# 		error.append('please enter your password')
# 	else:
# 		if Users.objects.filter(user_name=request.POST['username']).count()==0:
# 			error.append('please check your username')
# 		elif Users.objects.filter(user_name=request.POST['username'],
# 			password=request.POST['password']).count()==0:
# 			error.append('please check your password')
# 	context={'errors':error}
# 	return render(request,'login.html',context)


# 	return render(request,'login.html',context)

@login_required
def getProfile(request, profileid):	
	profile1=Profile.objects.get(id=profileid)
	user=User.objects.get(profile=profile1)
	# user1=User.objects.get(username=user)
	if profile1.user==request.user:
		exist='me'
	else:
		if request.user.profile.follows.all().filter(user=user):
			exist='followed'
		else:
			exist='unfollow'
	posts=Post.objects.filter(profile=profile1)
	posts=posts.order_by("-time")
	comments=Comment.objects.order_by()
	comments=comments.order_by("-time")
	context={'posts':posts, 'exist':exist,'userProfile':profile1,'comments':comments}
	
	return render(request, 'profile.html',context)

def getFollows(request):
	# user1=User.objects.get(username=request.user)
	posts=[]
	follows=request.user.profile.follows.values('user')

	posts=Post.objects.filter(profile__in=follows)
	posts=posts.order_by("-time")
	context={'posts':posts, 'follows':follows,'currentUser':request.user}
	return render(request,'follows.html',context)

@login_required
def getPhoto(request,id):
	profile=get_object_or_404(Profile, id=id)
	if not profile.picture:
		raise Http404
	content_type = guess_type(profile.picture.name)
	return HttpResponse(profile.picture, content_type)

@login_required
def follow(request,id):
	messages=[]
	profilenow=Profile.objects.get(id=id)
	user1=User.objects.get(profile=profilenow)
	user2=User.objects.get(username=request.user) #user you want to follow
	
	posts=Post.objects.filter(profile=profilenow)
	posts=posts.order_by("-time")

	profile1 = Profile.objects.get(user=user1)
	profile2=request.user.profile
	profile1.save()
	profile2.save()
	profile2.follows.add(profile1)

	follows=profile2.follows.all()
	if request.user.profile.follows.all().filter(user=user1): 
		exist='followed'
	else:
		exist='unfollow'
	messages.append('it has been follow')
	comments=Comment.objects.order_by()
	comments=comments.order_by("-time")
	context={'posts':posts, 'follows':follows,'messages':messages,'userProfile':profile1,'exist':exist,'comments':comments}
	return render(request, 'follows.html',context)

@login_required
def unfollow(request, id):
	messages=[]
	profilenow=Profile.objects.get(id=id)
	user1=User.objects.get(profile=profilenow)
	user2=User.objects.get(username=request.user) #user you want to follow

	posts=Post.objects.filter(profile=profilenow)
	posts=posts.order_by("-time")

	profile1 = Profile.objects.get(user=user1)
	profile2=request.user.profile
	profile1.save()
	profile2.save()
	profile2.follows.remove(profile1)
	follows=profile2.follows.all()
	if request.user.profile.follows.all().filter(user=user1): 
		exist='followed'
	else:
		exist='unfollow'
	messages.append('it has been unfollow')
	comments=Comment.objects.order_by()
	comments=comments.order_by("-time")
	context={'posts':posts, 'follows':follows,'messages':messages,'userProfile':profile1,'exist':exist,'comments':comments}
	return render(request, 'follows.html',context)

# us=user
# 	user1=User.objects.get(username=us)
# 	if request.user.profile.follows.all().filter(user=user1):
# 		errors.append('INININ')
# 	posts=Post.objects.filter(user=user1)
# 	posts=posts.order_by("-time")
# 	context={'posts':posts, 'errors':errors,'userProfile':user1,'users':user1}

@login_required
def changePassword(request):
	messages=[]
	context={}
	if request.method=='GET':
		context['passwordForm']=PasswordForm()
		return render(request, 'password.html',context)
	
	passwordForm=PasswordForm(request.POST)
	context['passwordForm']=PasswordForm(request.POST)
	
	if not passwordForm.is_valid():
		return render(request,'password.html',context)

	userChange=User.objects.get(username=request.user)
	# if passwordForm.cleaned_data['current_Password']!=userChange.password:
	# 	messages.append("Current password is wrong")
	# 	context['messages']=messages
	# 	return render(request,'password.html',context)
	userChange.set_password(passwordForm.cleaned_data['new_Password'])
	userChange.save()
	messages.append("password updated")
	context['messages']=messages
	context['userChange']=userChange
	return render(request,'password.html',context)

@login_required
def update(request):
	messages=[]
	context={}
	if request.method=='GET':		
		context['profileform']=ProfileForm()
		return render(request,'update.html',context)
	# try:
	# 	profile=request.user.profile
	# except Profile.DoesNotExist:
	# 	profile = Profile(user=request.user)
	profile=request.user.profile
	# nameform=UserNameForm(request.POST,instance=request.user)
	profileform=ProfileForm(request.POST, request.FILES, instance=profile)
	
	if not profileform.is_valid():
		context={'profileform':profileform}
		return render(request,'update.html',context)

	profileform.save()
	messages.append('it has been updated')
	context={'profileform':profileform, 'messages':messages,'currentUser':request.user}
	return render(request,'update.html',context)

@login_required
def main(request):
	return render(request,'main.html',context)

@login_required
def profile(request):
	return render(request,'profile.html',context)

@login_required
def create_comment(request,post_id):
	context={}
	messages=[]
	if not 'commentArea' in request.POST or not request.POST['commentArea']:
		context=json.dumps({"message":"error"})
		return HttpResponse(context, content_type='application/json')	
	post = Post.objects.get(id=post_id)
	new_comment=Comment(profile=request.user.profile, post=post, text=request.POST['commentArea'])
	new_comment.save()
	
	# profiles.add(Profile.objects.get(user=post.profile.user))
	profile=Profile.objects.get(user=request.user)
	# profileJson = serializers.serialize("json",profiles)

	df = DateFormat(localtime(new_comment.time))
  	date=df.format(get_format('DATE_FORMAT'))
  	time=df.format('f a')
  	timestamp=date+", "+time
  	firstname = profile.firstname
  	lastname=profile.lastname
  	profileid=profile.id
	context=json.dumps({"commentText":request.POST['commentArea'],"firstname":firstname,"time":timestamp,
		"lastname":lastname,"profileid":profileid})
  	
	return HttpResponse(context,content_type='application/json')

@login_required
def create_post(request, last_post):
	global time
	context={}	
	messages=[]
	# user=get_object_or_404()
	if request.method=='GET':
		context['form'] = PostForm()
		return render(request,'main.html',context)
	form = PostForm(request.POST)
  # 	if not 'postArea' in request.POST or not request.POST['postArea']:
		# context=json.dumps({"message":"error"})
		# return HttpResponse(context, content_type='application/json')	
	if not form.is_valid():
		context['form'] = form
		return render(request, 'main.html',context)
  	new_post=Post(text=form.cleaned_data['text'], profile=request.user.profile)
  	new_post.save()
  	last_post=int(last_post)

  	posts=Post.objects.filter(id__gt = last_post).order_by("-time")
  	
  	profiles=set()
  	for post in posts:
  		profiles.add(Profile.objects.get(user=post.profile.user))

  	postJson = serializers.serialize("json",posts)
  	profileJson = serializers.serialize("json",profiles)

  	timestamp={}
  	for post in posts:
  		df = DateFormat(localtime(post.time))
  		date=df.format(get_format('DATE_FORMAT'))
  		time=df.format('f a')
  		datetime=date+", "+time
  		timestamp[post.id]=datetime

  	last_post_id = Post.objects.latest('id').id
  	context=json.dumps({"posts":postJson, "profile":profileJson, "time":timestamp,
  		"last_post_id":last_post_id,
  		})
  	return HttpResponse(context, content_type='application/json')
	
def get_update(request,last_post):
	last_post=int(last_post)
	posts=Post.objects.filter(pk__gt = last_post).order_by("-time")
	profiles=set()
  	for post in posts:
  		profiles.add(Profile.objects.get(user=post.profile.user))

  	postJson = serializers.serialize("json",posts)
  	profileJson = serializers.serialize("json",profiles)

  	timestamp={}
  	for post in posts:
  		df = DateFormat(localtime(post.time))
  		date=df.format(get_format('DATE_FORMAT'))
  		time=df.format('f a')
  		datetime=date+", "+time
  		timestamp[post.id]=datetime

  	last_post_id = Post.objects.latest('id').id
  	# last_post_id=Post.objects.order_by('id')[0].id;
  	context=json.dumps({"posts":postJson, "profile":profileJson, "time":timestamp,
  		"last_post_id":last_post_id,
  		})
  	return HttpResponse(context, content_type='application/json')


def create_user(request):
	context={}
	messages=[]
	if request.method=='GET':
		context['form'] = RegistrationForm()
		return render(request,'register.html',context)

	form = RegistrationForm(request.POST)
	
	if not form.is_valid():
		context={'form':form}
		return render(request,'register.html',context)

	username=form.cleaned_data['username']
	new_user=User.objects.create_user(username=form.cleaned_data['username'],			
			password=form.cleaned_data['password1'],
			)
	new_user.is_active=False
	new_user.save()
	

 	token = default_token_generator.make_token(new_user)
 	email_body = """
 	Welcome to grumblr. Please check the link below to verify your email
 	address
 	http://%s%s
 	""" %(request.get_host(), reverse('confirm', args=(username, token)))	

 	profile=Profile(user=new_user,
			firstname= form.cleaned_data['firstname'],
			lastname= form.cleaned_data['lastname'],
			email=form.cleaned_data['email'],
			activeToken=token)
	profile.save()
 	send_mail(subject='Verify your email address',
 			  message=email_body,
 			  from_email='sjingjsq@gmail.com',
 			  recipient_list=[form.cleaned_data['email']])
		

	if not new_user.is_active:
		return redirect('/')
	new_user=authenticate(username=form.cleaned_data.get("username"),
		password=form.cleaned_data.get("password1")) 
	

	login(request, new_user)
	return redirect('/')

	# messages.append('user has been added')
	# context={'form':form,'messages':messages,'email':form.cleaned_data['email']}
	# users=User.objects.filter(username=form.cleaned_data.get("username"))
	# # passwords=User.objects.filter('password')
	# context['users']=new_user.username
	# context['passwords']=new_user.password
	# return render(request,'signup.html',context)


def confirm_registration(request, username, token):
	try :
		user = User.objects.get(username=username)
		profile = Profile.objects.get(user=user)
	except ObjectDoesNotExist:
		return redirect('/')

	if profile.activeToken==token:
		user.is_active=True
		user.save()
		profile.activeToken=""
		profile.save()

		login(request, user)
		return redirect(('/'))
	else:
		return redirect('/grumblr/login')

	