from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from bookstore_firaas.utils.pagination import CustomPagination
from .models import Admin
from .serializers import AdminSerializer


@permission_classes((permissions.IsAdminUser,))
# @permission_classes((permissions.AllowAny,))
class AdminViews(APIView, CustomPagination):

    def get(self, request, id=None):
        if id:
            try:
                result = Admin.objects.get(id=id)

                if result.deleted_at is not None:
                    return Response({'success': 'success', "data": "data not found"}, status=404)
                
                serializer = AdminSerializer(result)
                return Response({'success': 'success', "data": serializer.data}, status=200)
            except ObjectDoesNotExist:
                return Response({'success': 'success', "data": "data not found"}, status=404)
            
        result = Admin.objects.filter(deleted_at=None)
        self.page_size = request.GET['page_size']
        result_page = self.paginate_queryset(result, request)
        serializer = AdminSerializer(result_page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)
    
    def post(self, request):
        request.data['create_user_id'] = request.user.id

        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, id):
        result = Admin.objects.get(id=id)
        request.data['update_user_id'] = request.user.id

        serializer = AdminSerializer(result, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "success", "data": serializer.data})
        else:
            return Response({"success": "error", "data": serializer.errors})
    
    def delete(self, request, id=None):
        try:
            result = Admin.objects.get(id=id)
            result.soft_delete()
            return Response({"success": "success", "data": "Record Deleted"})
        except ObjectDoesNotExist:
            return Response({"success": "success", "data": "data not found"}, status=404)