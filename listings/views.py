from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.


class ListingsAPI(APIView):

    def get(self, request: HttpRequest):
        return HttpResponse("penis")
