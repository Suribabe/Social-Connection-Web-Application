from django import forms
from django.contrib.auth.models import User
from grumblr.models import *
import re

# class UserNameForm(forms.ModelForm):
# 	"""docstring for UserForm"""
# 	class Meta:
# 		"""docstring for Meta"""
# 		model=User
# 		fields=('first_name', 'last_name')
# 	def clean(self):
# 		cleaned_data=super(UserNameForm,self).clean()
# 		firstname=cleaned_data.get("first_name")
# 		lastname=cleaned_data.get("last_name")
# 		if firstname=="" or lastname=="":
# 			raise forms.ValidationError("firstname and lastname can't be empty")
# 		return cleaned_data

class ProfileForm(forms.ModelForm):
	"""docstring for UserForm"""
	class Meta:
		"""docstring for Meta"""
		model=Profile
		fields=('firstname','lastname','bio','age','picture')
		widget={'picture' : forms.FileInput()}
	def clean(self):
		cleaned_data=super(ProfileForm,self).clean()
		firstname=cleaned_data.get("first_name")
		lastname=cleaned_data.get("last_name")
		if firstname=="" or lastname=="":
			raise forms.ValidationError("firstname and lastname can't be empty")
		return cleaned_data

	def cleaned_age(self):
		age= self.cleaned_data.get("age")
		if age:
			raise forms.ValidationError("age is not valid")
		return age
		

class PostForm(forms.ModelForm):
	"""docstring for PostForm"""
	class Meta:
		model=Post
		# exclude=("time","profile",)
		# widget={
		# 	"text":forms.TextInput
		# }
		fields=['text']
	def clean_text(self):
		text=self.cleaned_data.get('text')
		if not text or len(text)==0:
			raise forms.ValidationError("post can't be empty")
		return text


class CommentForm(forms.ModelForm):
	"""docstring for PostForm"""
	class Meta:
		model=Comment
		exclude=("time","profile",)

		fields=['text']
	def clean_text(self):
		text=self.cleaned_data.get('text')
		if not text or len(text)==0:
			raise forms.ValidationError("comment can't be empty")
		return text
		
class RegistrationForm(forms.ModelForm):
	username=forms.CharField(max_length=20)
	# email=forms.CharField(max_length=100)
	# firstname=forms.CharField(max_length=20)
	# lastname=forms.CharField(max_length=20)
	password1=forms.CharField(max_length=200,
							widget=forms.PasswordInput())
	password2=forms.CharField(max_length=200,
							widget=forms.PasswordInput())
	# password2=forms.CharField(max_length=20,widget=forms.PasswordInput())
	class Meta:
		"""docstring for Meta"""
		model=Profile
		fields=('firstname','lastname','email')


	def clean(self):
		cleaned_data=super(RegistrationForm,self).clean()
		password1=cleaned_data.get("password1")
		password2=cleaned_data.get("password2")
		if password1!=password2:
			raise forms.ValidationError("password does not match")
		return cleaned_data


	def clean_username(self):
		username=self.cleaned_data.get('username')
		if User.objects.filter(username__exact=username):
			raise forms.ValidationError("Username already exist.")
		return username		
	def clean_email(self):
		email=self.cleaned_data.get('email')
		if not re.match(r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$' ,email):
			raise forms.ValidationError("Please Check your Email Format")
		if Profile.objects.filter(email__exact=email):
			raise forms.ValidationError("Email already exist.")
		return email

class PasswordForm(forms.Form):
	# current_Password=forms.CharField(max_length=200,
	# 						widget=forms.PasswordInput())
	new_Password=forms.CharField(max_length=200,
							widget=forms.PasswordInput())
	confirm_Password=forms.CharField(max_length=200,
							widget=forms.PasswordInput())

	def clean(self):
		cleaned_data=super(PasswordForm,self).clean()

		# current_Password=cleaned_data.get('current_Password')
		new_Password=cleaned_data.get('new_Password')
		confirm_Password=cleaned_data.get('confirm_Password')
		if new_Password!=confirm_Password:
			raise forms.ValidationError("password does not match")
		return cleaned_data																												

# class RegistrationForm(forms.Form):
			
# 	username=forms.CharField(max_length=20)
# 	email=forms.CharField(max_length=20)
# 	firstname=forms.CharField(max_length=20)
# 	lastname=forms.CharField(max_length=20)
# 	password1=forms.CharField(max_length=200,
# 							label='Password',
# 							widget=forms.PasswordInput())
# 	password2=forms.CharField(max_length=200,
# 							label='Password',
# 							widget=forms.PasswordInput())

# 	def clean(self):
# 		cleaned_data = super(RegistrationForm, self).clean()
# 		password1=cleaned_data.get('password1')
# 		password2=cleaned_data.get('password2')
# 		if password1 and password2 and password1!=password2:
# 			raise forms.ValidationError("Passwords did not match.")
# 		return cleaned_data
		
# 	def clean_username(self):
# 		username=self.cleaned_data.get('username')
# 		if User.objects.filter(username__exact=username):
# 			raise forms.ValidationError("Username already exist.")
# 		return username

# class ClassName(object):
# 	"""docstring for ClassName"""
# 	def __init__(self, arg):
# 		super(ClassName, self).__init__()
# 		self.arg = arg
# 		