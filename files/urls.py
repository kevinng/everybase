from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'files'
urlpatterns = [
    path('<str:uuid>', views.get_file, name='get_file')

    # path('read/', views.ReadOnlyPresignedURLView.as_view()),
    # path('write/', views.WriteOnlyPresignedURLView.as_view()),
    # path('file/', views.FileList.as_view()),
    # path('file/<int:pk>', views.FileDetail.as_view())
]
urlpatterns = format_suffix_patterns(urlpatterns)