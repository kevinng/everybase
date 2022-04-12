from django.urls import path
from leads import views

app_name = 'applications'
urlpatterns = [
    path('<int:aid>', views.application_detail, name='application_detail'),
]