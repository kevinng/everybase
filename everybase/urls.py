"""everybase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, path
from django.conf.urls import include

urlpatterns = [
    # path('', include('lander.urls')),
    # path('', include('accounts.urls')),
    # path('documents/', include('documents.urls')),
    # path('materials/', include('materials.urls')),
    path('', include('lander.urls')),
    path('3yJmUVGVJosFPDiZ6LyU4WARUiWXgMxCyfA6/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls'))
]