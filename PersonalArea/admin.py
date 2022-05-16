from django.contrib import admin
from django.contrib.auth.backends import ModelBackend

from PersonalArea.models import Aikido_Member, Achievements

admin.site.register(Aikido_Member)
admin.site.register(Achievements)


class SettingsBackend(ModelBackend):

    def authenticate(self, request,username=None,password=None,**kwargs):
        try:
            print(username)
            user = Aikido_Member.objects.get(id=username)
        except Aikido_Member.DoesNotExist:
            return None
        if user.password == password and user.is_superuser:
            return user
        return None

    def get_user(self, user_id):
        try:
            return Aikido_Member.objects.get(id=user_id)
        except Aikido_Member.DoesNotExist:
            return None
