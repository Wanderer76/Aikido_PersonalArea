from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from PersonalArea import views

urlpatterns = [
    path('students/', views.aikido_students_list),
    path('api/v1/account/login/', csrf_exempt(views.LoginAPIView.as_view())),
    path('api/v1/account/admin/login/', csrf_exempt(views.AdminLoginAPIView.as_view())),
    path('api/v1/seminar/<str:seminar_name>/', views.DownloadRequests.as_view()),
    path('api/v1/events/create/', csrf_exempt(views.CreateEvent.as_view())),
    path('api/v1/events/requests/create/', csrf_exempt(views.CreateRequest.as_view())),
    path('api/v1/events/requests/<str:event_name>/', views.TrainerEventRequest.as_view()),
    path('api/v1/account/profile/', csrf_exempt(views.StudentInfo.as_view())),
    path('api/v1/admin/seminar_statistic/', views.EventsList.as_view()),
    path('api/v1/admin/seminar/<str:event_name>/', views.SeminarStatistic.as_view()),
]
