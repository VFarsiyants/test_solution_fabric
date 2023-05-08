
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import ClientViewSet, PostOrderViewSet

router = DefaultRouter()
router.register('client', ClientViewSet)
router.register('post_order', PostOrderViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls'))
]