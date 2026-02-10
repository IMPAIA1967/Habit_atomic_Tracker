from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('habits.urls')),
    path('api/auth/', include('djoser.urls')),           # регистрация
    path('api/auth/', include('djoser.urls.jwt')),       # JWT токены
]