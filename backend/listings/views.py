from rest_framework.request import Request
from rest_framework.response import Response

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import serializers

from listings.models import Listing

# Create your views here.


class ListingsAPI(APIView):
    def get(self, request: Request) -> Response:
        listings = Listing.objects.all()
        return Response(listings.values_list())
