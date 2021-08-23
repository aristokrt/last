from django.contrib.auth import get_user_model
from rest_framework import views, status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from pin.models import Profile
from pin.serializers import ProfileSerializer
from .serializers import *
from .utils import send_activation_code
from .permissions import IsNotAuthenticated

User = get_user_model()


class RegisterView(views.APIView):
	def post(self, request):
		data = request.data
		serializer = RegisterSerializer(data=data)

		if serializer.is_valid(raise_exception=True):
			serializer.save()
			return Response('Successfully registered', status.HTTP_200_OK)


class LogoutView(GenericAPIView):
	serializer_class = LogoutSerializer
	permission_classes = [IsAuthenticated]

	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response('Successfully logged out', status.HTTP_200_OK)


class ActivationView(views.APIView):
	def get(self, request, activation_code):
		user = User.objects.filter(activation_code=activation_code).first()

		if not user:
			return Response('This user does not exist', status.HTTP_400_BAD_REQUEST)
		user.activation_code = ''
		user.is_active = True
		user.save()
		return Response('Account successfully activated.', status.HTTP_200_OK)


class ResetPasswordView(APIView):
	permission_classes = [IsNotAuthenticated]

	def get(self, request):
		email = request.query_params.get('email')
		user = get_object_or_404(User, email=email)
		user.is_active = False
		user.create_activation_code()
		user.save()
		send_activation_code(user.email, user.activation_code, 'reset_password')
		return Response('Activation code was sent to your email.', status.HTTP_200_OK)


class CompleteResetPassword(APIView):
	def post(self, request):
		serializer = ResetPasswordSerializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			serializer.save()
			return Response('You have successfully recovered your password', status.HTTP_200_OK)


class AccountsView(APIView):
	def get(self, request):
		queryset = CustomUser.objects.all()
		serializer = AccountsSerializer(queryset, many=True)
		return Response(serializer.data)


class FollowView(APIView):
	pass


class UnFollowView(APIView):
	pass