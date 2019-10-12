from django.http import HttpResponse
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json 

class MyView(View):
    def get(self, request):
        
        result="aligual loco"
        return Response(result,status=status.HTTP_200_OK)
    def post(self,request,format=None):

        return Response("Done",status=status.HTTP_200_OK)
# Create your views here.

class weatherFilters(APIView):
    def get(self, request, format=None):
        """
        Returns the data for the Temperature and Rain filters
        """
        with open('/home/ubuntu/REPOS/Fly-Filter-Backend/FlyFilter/filtersWeather.json') as json_file: # it know its harcoded, and i dont give a shit
            data = json.load(json_file)
        return Response(data, status=status.HTTP_200_OK)
