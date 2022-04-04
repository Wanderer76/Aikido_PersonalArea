from django.db import transaction
from django.http import JsonResponse
from pytils.translit import slugify
from rest_framework import status, permissions
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from clubs.utils import *

from PersonalArea.serializations import Clubs_Serializer
from clubs.models import Club


class CreateClub(APIView):
    permission_classes = (permissions.IsAdminUser,)

    @transaction.atomic
    def post(self, request):

        main_trainers = get_main_trainers(request.data)
        serializer = Clubs_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['slug'] = slugify(serializer.validated_data['name'])
            set_main_trainers(main_trainers, serializer.save())

            return Response(status=status.HTTP_201_CREATED, data={'content': 'created'})
        else:
            print(serializer.validated_data)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=serializer.errors)


class UpdateClub(APIView):
    permission_classes = (permissions.IsAdminUser,)

    @transaction.atomic
    def patch(self, request, slug):
        try:
            club = Club.objects.get(slug=slug)
        except Club.DoesNotExist:
            return JsonResponse({'message': 'The club does not exist'}, status=status.HTTP_404_NOT_FOUND)

        main_trainers = get_main_trainers(request.data)
        club_data = JSONParser().parse(request)

        serializer = Clubs_Serializer(club, data=request.data, partial=True)

        if serializer.is_valid():
            Club.objects.filter(slug=slug).update(**club_data)
            serializer.validated_data['slug'] = slugify(serializer.validated_data['name'])
            set_main_trainers(main_trainers, serializer.save())
            return Response(status=status.HTTP_200_OK, data={'content': 'updated'})
        else:
            print(serializer.validated_data)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=serializer.errors)


class GetClub(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, slug):
        try:
            club = Club.objects.get(slug=slug)
        except Club.DoesNotExist:
            return JsonResponse({'message': 'The club does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = Clubs_Serializer(club)
        return JsonResponse(get_club_info(club))


class GetClubs(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        serializer = Clubs_Serializer(Club.objects.all(), many=True)
        clubs = Club.objects.all()
        res = [get_club_info(i) for i in clubs]

        return JsonResponse(res, safe=False)


class DeleteClub(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def delete(self, request, slug):
        try:
            club = Club.objects.get(slug=slug)
        except Club.DoesNotExist:
            return JsonResponse({'message': 'The club does not exist'}, status=status.HTTP_404_NOT_FOUND)

        club.delete()
        return JsonResponse({'message': 'Club was deleted successfully!!!!!!'}, status=status.HTTP_204_NO_CONTENT)
