from django.urls import path
from account import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('login/', views.Login.as_view(), name="login"),
    path('registration/', views.Registration.as_view(), name="registration"),
    path('student/', views.Student.as_view(), name="student"),
]

