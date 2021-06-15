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
    path('common/', include('common.urls')),
    path('files/', include('files.urls')),
    path('growth/', include('growth.urls')),
    path('chat/', include('chat.urls')),
    path('', include('chat.urls_root')),

    # Django admin, with obfuscated URL
    path('3yJmUVGVJosFPDiZ6LyU4WARUiWXgMxCyfA6/', admin.site.urls),

    # Django Rest Framework login
    path('api-auth/', include('rest_framework.urls'))
]

admin.site.site_header = "Everybase Admin"
admin.site.site_title = "" # No title
admin.site.index_title = "Welcome to Everybase Admin Portal"