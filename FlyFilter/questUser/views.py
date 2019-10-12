from django.http import HttpResponse
from django.views.generic import View

class MyView(View):
    def get(self, request):
        
        result="aligual loco"
        return Response(result,status=status.HTTP_200_OK)
    def post(self,request,format=None):

        return Response("Done",status=status.HTTP_200_OK)
# Create your views here.
