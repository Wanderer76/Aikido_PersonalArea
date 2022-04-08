from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from events import views

urlpatterns = [
    path('create/', csrf_exempt(views.CreateEvent.as_view())),
    path('requests/create/', csrf_exempt(views.CreateRequest.as_view())),
    path('requests/<str:event_name>/', views.TrainerEventRequest.as_view()),
    path('event_list/', views.EventsList.as_view()),
    path('event_statistic/<str:event_name>/', views.EventView.as_view()),
    path('file_job/<str:seminar_url>/', csrf_exempt(views.EventInfoLoad.as_view())),
]
