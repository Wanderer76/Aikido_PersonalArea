from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from events import views

urlpatterns = [
    path('create/', csrf_exempt(views.CreateEvent.as_view())),
    path('update/<str:event_slug>/', csrf_exempt(views.UpdateEvent.as_view())),
    path('delete/<str:event_slug>/', csrf_exempt(views.DeleteEvent.as_view())),
    path('requests/create/', csrf_exempt(views.CreateRequest.as_view())),
    path('trainer/requests/<str:event_slug>/', views.TrainerEventRequest.as_view()),
    path('event_list/', views.EventsList.as_view()),
    path('upcoming_list/', views.UpcomingList.as_view()),
    path('base_for_trainer/<str:event_slug>/', views.BaseInfoForTrainer.as_view()),
    path('event_statistic/<str:event_slug>/', views.EventView.as_view()),
    path('file/upload/<str:seminar_url>/', csrf_exempt(views.EventInfoLoad.as_view())),
    path('file/download/<str:seminar_url>/', csrf_exempt(views.EventInfoLoad.as_view())),
]
