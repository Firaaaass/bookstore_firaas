from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from bookstore_firaas.modules.user.models import User
from bookstore_firaas.modules.user.serializers import UserSerializer

@permission_classes((permissions.IsAuthenticated,))
class MeViews(APIView):

    def get(self, request):
        serializers = UserSerializer(request.user)
        return Response({'status': 'success', "data": serializers.data}, status=200)
    
    def post(self, request):
        result = User.objects.get(id=request.user.id)

        serializer = UserSerializer(result, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})