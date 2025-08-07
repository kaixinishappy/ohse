from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ReportingFormSerializer

    
class ReportingFormView(APIView):
    def post(self, request):
        serializer = ReportingFormSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Data is valid ✅"})
        return Response(serializer.errors, status= 400)
    
