from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from pin.views import *
from users.views import AccountsView

schema_view = get_schema_view(
   openapi.Info(
      title="PinterestAPI",
      default_version='v1',
      description="Project for final Hackaton",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(AllowAny, ),
)

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('pins', PinViewSet)
router.register('comments', CommentViewSet)
router.register('rating', RatingViewSet)
router.register('likes', LikeViewSet)
router.register('profiles', ProfileViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/docs/', schema_view.with_ui()),
    path('api/account/', include('users.urls')),
    path('api/accounts/', AccountsView.as_view()),
    path('api/', include(router.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
