from django.shortcuts import render
import django_filters
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.views import APIView

from user.models import PlatformAccount


class PlatformAccountFilter(django_filters.FilterSet):
    login = django_filters.CharFilter(lookup_expr="icontains")
    user = django_filters.NumberFilter(field_name="user__id")
    platform = django_filters.NumberFilter(field_name="platform__id")
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = PlatformAccount
        fields = ["login", "user", "platform", "is_active"]


class ParserAccountsAPI(APIView):
    class OutputSerializer(serializers.Serializer):
        login = serializers.CharField()
        password = serializers.CharField()
        user = serializers.IntegerField(source="user_id")
        platform = serializers.IntegerField(source="platform_id")
        is_active = serializers.BooleanField()

    def get(self, request: Request):
        qs = PlatformAccount.objects.all()

        # применяем фильтрацию вручную
        filterset = PlatformAccountFilter(request.GET, queryset=qs)
        if not filterset.is_valid():
            return Response({"errors": filterset.errors}, status=400)

        filtered_qs = filterset.qs
        serializer = self.OutputSerializer(filtered_qs, many=True)
        return Response(serializer.data)
