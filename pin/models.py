from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
	slug = models.SlugField(max_length=100, primary_key=True)
	title = models.CharField(max_length=100, unique=True)

	class Meta:
		ordering = ['slug']

	def __str__(self):
		return self.title


class Pin(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pins')
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='pins')
	title = models.CharField(max_length=100)
	text = models.TextField(null=True, blank=True)
	hashtags = models.TextField(null=True, blank=True)
	image = models.ImageField(upload_to='pins', blank=True, null=True)
	link = models.CharField(max_length=200, null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['created']

	def __str__(self):
		return self.title


class Comment(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
	pin = models.ForeignKey(Pin, on_delete=models.CASCADE, related_name='comments')
	text = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['created']

	def __str__(self):
		return self.author.username


class Rating(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
	pin = models.ForeignKey(Pin, on_delete=models.CASCADE, related_name='ratings')
	rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])

	class Meta:
		ordering = ['id']

	def __str__(self):
		return f'{self.author}: {self.pin} - {self.rating}'


class Like(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
	pin = models.ForeignKey(Pin, on_delete=models.CASCADE, related_name='likes')

	class Meta:
		ordering = ['id']


class Profile(models.Model):
	GENDER_CHOICES = [
		('female', 'Female'),
		('male', 'Male')
	]

	author = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
	first_name = models.CharField(max_length=50, null=True, blank=True)
	last_name = models.CharField(max_length=50, null=True, blank=True)
	date_of_birth = models.DateField(null=True, blank=True)
	gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)
	country = models.CharField(max_length=50, null=True, blank=True)
	city = models.CharField(max_length=50, null=True, blank=True)
	followers = models.ManyToManyField(User, related_name='followers', blank=True)
	followings = models.ManyToManyField(User, related_name='followings', blank=True)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['created']

	def __str__(self):
		return self.author.email
