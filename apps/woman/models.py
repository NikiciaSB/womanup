from __future__ import unicode_literals
from django.db import models
import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class userManager(models.Manager):
	def regValidator(self,postData):
		errors = {}
		if User.objects.filter(email = postData['email']):
            # .filter Returns a new QuerySet containing objects that match the given lookup parameters.
		 	errors['email_exists'] = "An account associated with that email address already exists."
		if len(postData['first_name']) < 3 or not postData['first_name'].isalpha():
            # The method isalpha() checks whether the string consists of alphabetic characters only.
			errors['first_name'] = "First name must be at least 3 characters long, and use only alphabetical characters."
		if len(postData['last_name']) < 3 or not postData['last_name'].isalpha():
			errors['last_name'] = "Last name must be at least 3 characters long, and use only alphabetical characters."
		if EMAIL_REGEX.match(postData['email']) == None:
			errors['email_format'] = "Email must be in valid email format."
            # the email has to match the format that is specified in the post data if not it will flag errors
		if len(postData['password']) < 8:
			errors['pword_length'] = "Password must be at least 8 characters long."
		if postData['password'] != postData['pwconf']:
			errors['pwconf'] = "Password confirmation must match password."
		print(errors)
		return errors

	def loginValidator(self,postData):
		user = User.objects.filter(email = postData['login_email'])
		errors = {}
		if not user:
			errors['email'] = "You are not a user, please register your account"
		if user and not bcrypt.checkpw(postData['login_password'].encode('utf8'), user[0].password.encode('utf8')):
			errors['password'] = "Invalid password."
		return errors
    
	def updateGValidator(self,postData):
		badList=["bitch","bitches","bitchs","bitchfit","bitch fit","cunt","whore","slut","ho","hoe","skank","cow","hussy","wench","broad","harpy","virago","dame","harridan","chick","pussy","pus","hag","dyke","fag","filly"]
		errors = {}
		toAudit = postData['update_group_title'].split()
		toAudit += postData['update_group_desc'].split()
		for word in toAudit:
			word = re.sub(r'[^\w\s]','',word).lower()
			if word in badList:
				print("Found a bad list word in group")
				errors['post']="We do not allow such derogatory language towards women on our site. Please change your rhetoric to be more respectful to voice your unique opinion"
		return errors

	def updatePValidator(self,postData):
		badList=["bitch","bitches","bitchs","bitchfit","bitch fit","cunt","whore","slut","ho","hoe","skank","cow","hussy","wench","broad","harpy","virago","dame","harridan","chick","pussy","pus","hag","dyke","fag","filly"]
		errors = {}
		toCorrect = postData['update_post_title'].split()
		toCorrect += postData['update_post'].split()
		for word in toCorrect:
			word = re.sub(r'[^\w\s]','',word).lower()
			if word in badList:
				print("Found a bad list word in group")
				errors['post']="We do not allow such derogatory language towards women on our site. Please change your rhetoric to be more respectful to voice your unique opinion"
		return errors

	def postValidator(self,postData):
		print("validating post...")
		badList=["bitch","bitches","bitchs","bitchfit","bitch fit","cunt","whore","slut","ho","hoe","skank","cow","hussy","wench","broad","harpy","virago","dame","harridan","chick","pussy","pus","hag","dyke","fag","filly"]
		errors = {}
		toCheck = postData['post'].split()
		toCheck += postData['post_title'].split()
		for word in toCheck:
			word = re.sub(r'[^\w\s]','',word).lower()
			if word in badList:
				print("Found a bad list word in post")
				errors['post']="We do not allow such derogatory language towards women on our site. Please change your rhetoric to be more respectful to voice your unique opinion"
		return errors

	def commentValidator(self,postData):
		print("validating comment...")
		badList=["bitch","bitches","bitchs","bitchfit","bitch fit","cunt","whore","slut","ho","hoe","skank","cow","hussy","wench","broad","harpy","virago","dame","harridan","chick","hag","pus","pussy","dyke","fag","filly"]
		errors = {}
		toCheck = postData['comment'].split()
		for word in toCheck:
			word = re.sub(r'[^\w\s]','',word).lower()
			if word in badList:
				print("Found a bad list word in comment")
				errors['post']="We do not allow such derogatory language towards women on our site. Please change your rhetoric to be more respectful to voice your unique opinion"
		return errors

	def groupValidator(self,postData):
		print("validating group...")
		badList=["bitch","cunt","bitches","bitchs","bitchfit","bitch fit","whore","slut","ho","hoe","skank","cow","hussy","wench","broad","harpy","virago","dame","harridan","chick","dyke","pussy","pus","hag","fag","filly"]
		errors = {}
		print(postData)
		for key in postData:
			print(key)
		toAudit = postData['group_title'].split()
		toAudit += postData['group_desc'].split()
		for word in toAudit:
			word = re.sub(r'[^\w\s]','',word).lower()
			if word in badList:
				print("Found a bad list word in group")
				errors['post']="We do not allow such derogatory language towards women on our site. Please change your rhetoric to be more respectful to voice your unique opinion"
		return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = userManager()

class Group(models.Model):
    group_title = models.CharField(max_length = 100)
    group_desc = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    likes = models.ManyToManyField(User, related_name = "liked")
    created_by = models.ForeignKey(User, related_name = "creator")
    objects = userManager()

class Post(models.Model):
    post = models.TextField()
    post_title = models.CharField(max_length = 255)
    added_by = models.ForeignKey(User, related_name = "uploader")
    liked_by = models.ManyToManyField(User, related_name = "likes")
    groups = models.ForeignKey(Group, related_name="g_posts") 
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = userManager()

class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    group = models.ForeignKey(Group, related_name='g_comments')
    user = models.ForeignKey(User, related_name='u_comments')
    post = models.ForeignKey(Post, related_name='p_comments')
    objects = userManager()