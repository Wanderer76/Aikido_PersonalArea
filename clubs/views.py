from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from PersonalArea.serializations import Clubs_Serializer
from clubs.models import Club
from pytils.translit import slugify


class CreateClub(APIView):
    permission_classes = (permissions.IsAdminUser,)

    @transaction.atomic
    def post(self, request):
        serializer = Clubs_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['slug'] = slugify(serializer.validated_data['name'])
            serializer.save()
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

        club_data = JSONParser().parse(request)
        serializer = Clubs_Serializer(club, data=club_data, partial=True)

        if serializer.is_valid():
            Club.objects.filter(slug=slug).update(**club_data)
            serializer.validated_data['slug'] = slugify(serializer.validated_data['name'])
            serializer.save()
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
        return JsonResponse(serializer.data)


class GetClubs(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        serializer = Clubs_Serializer(Club.objects.all(), many=True)
        return JsonResponse(serializer.data, safe=False)




