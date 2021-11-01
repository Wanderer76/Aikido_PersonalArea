from django.contrib import admin
from django.urls import path, include
from PersonalArea import views

urlpatterns = [
    path('students/', views.aikido_students_list),
    path('students/<int:pk>/seminars/', views.student_seminars),
    path('api/v1/events/create/', views.create_event),
    path('api/v1/events/makerequest/', views.make_request),
]
