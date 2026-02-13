from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet
from .views_auth import register_user, CustomTokenObtainPairView

router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habit')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register_user, name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
