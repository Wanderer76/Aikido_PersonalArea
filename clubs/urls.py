from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from clubs import views

urlpatterns = [
    path('create_club/', csrf_exempt(views.CreateClub.as_view())),
    path('update_club/<str:slug>/', csrf_exempt(views.UpdateClub.as_view())),
    path('get_club/<str:slug>/', csrf_exempt(views.GetClub.as_view())),
    path('get_clubs/', csrf_exempt(views.GetClubs.as_view())),
    path('delete_club/<str:slug>/', csrf_exempt(views.DeleteClub.as_view())),
]
