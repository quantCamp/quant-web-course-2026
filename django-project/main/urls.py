from django.urls import path

from main import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('course/<str:course_name>/',
         views.course_description, name='course_description'),
    path('teacher/<str:teacher_name>/', views.teacher_description, name='teacher_name')
]