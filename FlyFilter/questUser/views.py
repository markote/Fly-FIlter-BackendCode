from django.http import HttpResponse
from django.views.generic import View
from rest_framework.permissions import IsAuthenticated, AllowAny

from questUser.models import respuestasUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import ast
import json
import logging

from questUser.serializer import SerializerForm, SerializerFormSelector
logger = logging.getLogger(__name__)

class finalFilter(APIView):
    permission_classes = (AllowAny, )

    def post(self,request,format=None):
        in_data = SerializerFormSelector(data=request.data)
        in_data.is_valid(raise_exception=True)

        user_id   = in_data.validated_data.get('user_id')

        resp=respuestasUser.objects.filter(idResp=user_id)
        if resp:
            return Response(ast.literal_eval(resp[0].resp),status=status.HTTP_200_OK)

        else:
            return Response({"error": 'Not Found'},status=status.HTTP_404_NOT_FOUND)


class initialFilter(APIView):
    permission_classes = (AllowAny, )

    def post(self,request,format=None):
        """
        Saves the json with the client id
        """
        in_data = SerializerForm(data=request.data)
        in_data.is_valid(raise_exception=True)

        form_response   = in_data.validated_data.get('form_response')

        idpreg = form_response["hidden"]["user_id"]

        resp=respuestasUser(idResp=idpreg,resp=str(form_response["answers"]) )
        #resp.idresp=idpreg
        #resp.resp=str(request.data["form_response"]["answers"])
        resp.save()
        #result="id_user:"+idpreg+" saved in the DB. And here is the data:"+resp.resp

        return Response({"error": 0},status=status.HTTP_200_OK)
# Create your views here.

class weatherFilters(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, format=None):
        """
        Returns the data for the Temperature and Rain filters
        """
        with open('/home/ubuntu/REPOS/Fly-Filter-Backend/FlyFilter/filtersWeather.json') as json_file: # it know its harcoded, and i dont give a shit
            data = json.load(json_file)
        return Response(data, status=status.HTTP_200_OK)

class citiesInfo(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, format=None):
        """
        Returns the data for the Temperature and Rain filters
        """

        with open('/home/ubuntu/REPOS/Fly-Filter-Backend/FlyFilter/citiesCompleteInfo.json') as json_file: # it know its harcoded, and i dont give a shit
            data = json.load(json_file)
        return Response(data, status=status.HTTP_200_OK)
