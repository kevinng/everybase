from django.urls import path
from relationships import views

app_name = 'alerts'
urlpatterns = [
    path('', views.alert_list, name='alert_list'),
    path('<int:id>', views.alert_detail, name='alert_detail'),
    path('<int:id>/edit', views.alert_edit, name='alert_edit'),
    path('<int:id>/delete', views.alert_delete, name='alert_delete'),
    path('create', views.alert_create, name='alert_create'),
]