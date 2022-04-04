from django.db import models


class Club(models.Model):
    name = models.CharField(name="name", max_length=50, primary_key=True)
    city = models.CharField(name="city", max_length=50)
    area = models.CharField(name="area", max_length=50)
    #main_trainers = models.ForeignKey(related_name="main_trainers", to="PersonalArea.Aikido_Member", to_field='id',
    #                                  on_delete=models.CASCADE, null=True)
    logo = models.ImageField(name="logo", upload_to='logo_images/')
    slug = models.SlugField(name='slug', max_length=50, unique=True, null=False)
