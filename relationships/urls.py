from django.urls import path
from relationships import views

app_name = 'users'
urlpatterns = [
    path('upload_status_file/<int:user_id>/',
        views.upload_status_file,
        name='upload_status_file'),
    path('delete_status_file/<int:user_id>/',
        views.delete_status_file,
        name='delete_status_file'),
    path('delete_orphan_files/<int:user_id>/',
        views.delete_orphan_files,
        name='delete_orphan_files')
]