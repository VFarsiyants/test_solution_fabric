from django.contrib import admin
from rest_framework import permissions
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Post service api",
      default_version='v1'
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('post_order.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0)),
]
