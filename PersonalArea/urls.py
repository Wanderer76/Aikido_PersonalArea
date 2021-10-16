from django.contrib import admin
from django.urls import path, include
from PersonalArea import views

urlpatterns = [
    path('students/', views.aikido_students_list),
    path('students/<int:pk>/seminars/', views.student_seminars),
]
