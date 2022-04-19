from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from PersonalArea import views

urlpatterns = [
    path('students/', views.aikido_students_list),
    path('login/', csrf_exempt(views.LoginAPIView.as_view())),
    path('profile/', csrf_exempt(views.StudentInfo.as_view())),
    path('trainers/', views.TrainserSet.as_view()),
    path('candidates/trainers/', views.CandidatesToTrainer.as_view()),
    path('trainers/base/<int:id>/', views.TrainerBaseInfo.as_view()),
    path('trainer/students/', csrf_exempt(views.TrainerHasbiks.as_view())),
    path('admin/event/<str:event_name>/', views.SeminarStatistic.as_view()),
    path('admin/members_info/', csrf_exempt(views.AikidoMembersInfo.as_view())),
    path('create_trainer/<int:id>/', csrf_exempt(views.CreateTrainer.as_view())),
    path('create_trainer/', csrf_exempt(views.CreateTrainer.as_view())),
    path('modificate_trainer/<int:id>/', csrf_exempt(views.Modificate_Trainer.as_view())),
]
