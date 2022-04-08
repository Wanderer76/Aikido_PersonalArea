from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from PersonalArea import views

urlpatterns = [
    path('students/', views.aikido_students_list),
    path('api/v1/account/login/', csrf_exempt(views.LoginAPIView.as_view())),
    path('api/v1/account/profile/', csrf_exempt(views.StudentInfo.as_view())),
    path('api/v1/account/trainer_students/', csrf_exempt(views.TrainerHasbiks.as_view())),
    path('api/v1/admin/seminar/<str:event_name>/', views.SeminarStatistic.as_view()),
    path('api/v1/admin/members_info/', csrf_exempt(views.AikidoMembersInfo.as_view())),
]


