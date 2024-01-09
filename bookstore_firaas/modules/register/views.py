from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from bookstore_firaas.modules.register.serializers import RegisterSerializer


@permission_classes((permissions.AllowAny,))
class RegisterViews(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=self.request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": "success"}, status=201)
        else:
            return Response({"status": "failed", "data": serializer.errors}, status=400)