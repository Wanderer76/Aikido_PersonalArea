from django.db import models


class Club(models.Model):
    name = models.CharField(name="name", max_length=50, unique=True)
    city = models.CharField(name="city", max_length=50)
    area = models.CharField(name="area", max_length=50)
    logo = models.ImageField(name="logo", upload_to='logo_images/')
    slug = models.SlugField(name='slug', max_length=50, unique=True, null=False)

    def __str__(self):
        return self.name
