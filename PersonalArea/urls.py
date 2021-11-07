from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from PersonalArea import views
from PersonalArea.views import LoginAPIView

urlpatterns = [
    path('students/', views.aikido_students_list),
    path('students/<int:pk>/seminars/', views.student_seminars),
    path('api/v1/seminar/<str:seminar_name>/', views.DownloadRequests.as_view()),
    path('api/v1/events/create/', csrf_exempt(views.CreateEvent.as_view())),
    path('api/v1/events/makerequest/', csrf_exempt(views.CreateRequest.as_view())),

]
