from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import InvestigationSerializer

class InvestigationView(APIView):
    def post(self, request):
        serializer = InvestigationSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Data is valid ✅"})
        return Response(serializer.errors, status=400)
    