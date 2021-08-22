from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .views import *

urlpatterns = [
	path('register/', RegisterView.as_view()),
	path('activate/<str:activation_code>/', ActivationView.as_view(), name='activate'),
	path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('logout/', csrf_exempt(LogoutView.as_view()), name='logout'),
	path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('reset-password/', ResetPasswordView.as_view()),
	path('reset-password/complete/', CompleteResetPassword.as_view()),
	path('follow/', FollowView.as_view()),
	path('unfollow/', UnFollowView.as_view())
]
