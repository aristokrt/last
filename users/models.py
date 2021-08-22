from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string


class CustomUserManager(BaseUserManager):

	def create_user(self, email, username, password, **extra_fields):
		email = self.normalize_email(email)
		user = CustomUser(email=email, username=username, **extra_fields)
		user.set_password(password)
		user.create_activation_code()
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password, **extra_fields):
		email = self.normalize_email(email)
		user = self.model(email=email, username=username, **extra_fields)
		user.set_password(password)
		user.is_staff = True
		user.is_superuser = True
		user.is_active = True
		user.save(using=self._db)
		return user


class CustomUser(AbstractUser):
	username = models.CharField(max_length=50, unique=True, null=False, blank=False)
	email = models.EmailField(unique=True, null=False, blank=False)
	is_active = models.BooleanField(default=False)
	activation_code = models.CharField(max_length=8, blank=True)

	objects = CustomUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	def __str__(self):
		return f'{self.username} | ID: {self.id}'

	def create_activation_code(self):
		code = get_random_string(8, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
		self.activation_code = code
