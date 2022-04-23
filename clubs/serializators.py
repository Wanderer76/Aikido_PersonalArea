from pytils.translit import slugify
from rest_framework import serializers

from clubs.models import Club


class Clubs_Serializer(serializers.ModelSerializer):
    slug = serializers.SlugField(default="")

    class Meta:
        model = Club
        exclude = ['id', ]

    def update(self, instance: Club, validated_data):
        if validated_data.__contains__('logo') and validated_data.get('logo') != 'undefined':
            instance.logo.delete()
            instance.logo = validated_data.get('logo')

        instance.name = validated_data.get('name', instance.name)
        instance.city = validated_data.get('city', instance.city)
        instance.area = validated_data.get('area', instance.area)
        instance.slug = slugify(instance.name)
        instance.save()
        return instance


class ClubName_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ['name']
