from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from bookstore_firaas.utils.pagination import CustomPagination
from .models import User
from .serializers import UserSerializer


@permission_classes((permissions.IsAdminUser,)) 
# @permission_classes((permissions.AllowAny,))
class UserViews(APIView, CustomPagination):

    def get(self, request, id=None):
        if id:
            try:
                result = User.objects.get(id=id)

                if result.deleted_at is not None:
                    return Response({'success': 'success', "data": "data not found"}, status=404)
                
                serializer = UserSerializer(result)
                return Response({'success': 'success', "data": serializer.data}, status=200) #harusnya serializers pake s atau engga?
            except ObjectDoesNotExist:
                return Response({'success': 'success', "data": "data not found"}, status=404)
            
        result = User.objects.filter(deleted_at=None)
        self.page_size = request.GET['page_size']
        result_page = self.paginate_queryset(result, request)
        serializer = UserSerializer(result_page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)
    
    def post(self, request):
        request.data['create_user_id'] = request.user.id

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, id):
        result = User.objects.get(id=id)
        request.data['update_user_id'] = request.user.id

        serializer = UserSerializer(result, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "success", "data": serializer.data})
        else:
            return Response({"success": "error", "data": serializer.errors})
    
    def delete(self, request, id=None):
        try:
            result = User.objects.get(id=id)
            result.soft_delete()
            return Response({"success": "success", "data": "Record Deleted"})
        except ObjectDoesNotExist:
            return Response({"success": "success", "data": "data not found"}, status=404)