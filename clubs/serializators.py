from rest_framework import serializers

from clubs.models import Club


class Clubs_Serializer(serializers.ModelSerializer):
    slug = serializers.SlugField(default="")
    class Meta:
        model = Club
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.logo.delete()
        instance.name = validated_data.get('name',instance.name)
        instance.city = validated_data.get('city',instance.city)
        instance.area = validated_data.get('area',instance.area)
        instance.logo = validated_data.get('logo',instance.logo)
        instance.save()
        return instance