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
    # path('products/', include('products.urls')),

    path('growth/', include('growth.urls')),
    path('leads/', include('leads.urls')),
    path('relationships/', include('relationships.urls')),

    # Cloaked links
    path('i/', include('cloaker.urls')),

    # Landing page
    path('', include('lander.urls')),

    # Django admin, with ofuscated URL
    path('3yJmUVGVJosFPDiZ6LyU4WARUiWXgMxCyfA6/', admin.site.urls),

    # Django Rest Framework login
    path('api-auth/', include('rest_framework.urls'))
]