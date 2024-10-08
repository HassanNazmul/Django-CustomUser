"""
URL configuration for django_customUser project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from django_customUser.swagger import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('user_management.urls')),

    # dj-rest-auth
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    # path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),

    # Swagger URLS
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api_v1/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api_v2/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
