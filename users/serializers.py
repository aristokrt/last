from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .utils import send_activation_code, create_profile


class RegisterSerializer(serializers.ModelSerializer):
	password = serializers.CharField(min_length=8, required=True, write_only=True)
	password_confirmation = serializers.CharField(min_length=8, required=True, write_only=True)

	class Meta:
		model = CustomUser
		fields = ['username', 'email', 'password', 'password_confirmation']

	def validate(self, attrs):
		password = attrs.get('password')
		password_confirmation = attrs.pop('password_confirmation')

		if password != password_confirmation:
			raise serializers.ValidationError('Passwords do not match')
		return attrs

	def create(self, validated_data):
		user = CustomUser.objects.create_user(**validated_data)
		send_activation_code(user.email, user.activation_code, 'register')
		return user

	def save(self, **kwargs):
		user = super().save()
		create_profile(user)
		return user


class LogoutSerializer(serializers.Serializer):
	refresh = serializers.CharField()

	def validate(self, attrs):
		self.token = attrs.get('refresh')
		return attrs

	def save(self, **kwargs):
		try:
			RefreshToken(self.token).blacklist()
		except TokenError:
			self.fail('Incorrect token')


class ResetPasswordSerializer(serializers.Serializer):
	email = serializers.EmailField()
	activation_code = serializers.CharField(max_length=8, required=True)
	password = serializers.CharField(min_length=8, required=True)
	password_confirmation = serializers.CharField(min_length=8, required=True)

	def validate_email(self, email):
		if not CustomUser.objects.filter(email=email).exists():
			raise serializers.ValidationError('User is not found')
		return email

	def validate_activation_code(self, act_code):
		if not CustomUser.objects.filter(activation_code=act_code, is_active=False).exists():
			raise serializers.ValidationError('Invalid activation code')
		return act_code

	def validate(self, attrs):
		password = attrs.get('password')
		password_confirmation = attrs.pop('password_confirmation')

		if password != password_confirmation:
			raise serializers.ValidationError('Passwords do not match')
		return attrs

	def save(self, **kwargs):
		data = self.validated_data
		email = data.get('email')
		activation_code = data.get('activation_code')
		password = data.get('password')

		try:
			user = CustomUser.objects.get(email=email, activation_code=activation_code, is_active=False)
		except CustomUser.DoesNotExist:
			raise serializers.ValidationError('User is not found')

		user.is_active = True
		user.activation_code = ''
		user.set_password(password)
		user.save()
		return user


class AccountsSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomUser
		fields = ['id', 'username', 'email']

	def to_representation(self, instance):
		representation = super().to_representation(instance)
		representation['followers'] = instance.followers.count()
		representation['followings'] = instance.followings.count()
		return representation
