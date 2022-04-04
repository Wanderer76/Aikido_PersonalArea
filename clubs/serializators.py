from rest_framework import serializers

from clubs.models import Club


class Clubs_Serializer(serializers.ModelSerializer):
    slug = serializers.SlugField(default="")
    class Meta:
        model = Club
        fields = '__all__'