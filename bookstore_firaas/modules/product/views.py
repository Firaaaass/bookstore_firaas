from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookstore_firaas.utils.decorators import method_permission_classes
from bookstore_firaas.utils.pagination import CustomPagination
from .models import Product
from .serializers import ProductSerializer


class ProductViews(APIView, CustomPagination):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)  # used for default APIView endpoints

    def get(self, request, id=None):
        if id:
            try:
                result = Product.objects.get(id=id)

                if result.deleted_at is not None:
                    return Response({'success': 'success', "data": "data not found"}, status=404)

                serializers = ProductSerializer(result, context={'request': request})
                return Response({'success': 'success', "data": serializers.data}, status=200)
            except ObjectDoesNotExist:
                return Response({'success': 'success', "data": "data not found"}, status=404)

        result = Product.objects.filter(deleted_at=None)
        self.page_size = request.GET['page_size']
        result_page = self.paginate_queryset(result, request)
        serializer = ProductSerializer(result_page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

    @method_permission_classes((permissions.IsAdminUser,))
    def post(self, request):
        print(request.user.id)
        request.data._mutable=True
        request.data['create_user_id'] = request.user.id
        print("masuk")
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @method_permission_classes((permissions.IsAdminUser,))
    def patch(self, request, id):
        result = Product.objects.get(id=id)
        request.data['update_user_id'] = request.user.id

        serializer = ProductSerializer(result, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

    @method_permission_classes((permissions.IsAdminUser,))
    def delete(self, request, id=None):
        try:
            result = Product.objects.get(id=id)
            result.soft_delete()
            return Response({"status": "success", "data": "Record Deleted"})
        except ObjectDoesNotExist:
            return Response({'success': 'success', "data": "data not found"}, status=404)
