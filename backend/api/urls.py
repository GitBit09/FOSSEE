from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DatasetViewSet, user_login, user_register, user_logout, user_status

router = DefaultRouter()
router.register(r'datasets', DatasetViewSet, basename='dataset')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', user_login, name='login'),
    path('auth/register/', user_register, name='register'),
    path('auth/logout/', user_logout, name='logout'),
    path('auth/status/', user_status, name='status'),
]
