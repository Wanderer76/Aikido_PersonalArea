from django.contrib import admin
from django.urls import path, include
from PersonalArea import views
from PersonalArea.views import LoginAPIView

urlpatterns = [
    path('students/', views.aikido_students_list),
    path('students/<int:pk>/seminars/', views.student_seminars),
    path('auth/', include('djoser.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.urls.authtoken')),

    path('users/login/', LoginAPIView.as_view()),
    path('api/users/login/', LoginAPIView.as_view()),
  #  path('api/v1/accounts/', views.AikidoMemberListView.as_view()),
   # path('api/v1/accounts/<int:pk>', views.AikidoMemberDetailView.as_view()),
    path('api/v1/events/create/', views.create_event),
    path('api/v1/events/makerequest/', views.make_request),
]
