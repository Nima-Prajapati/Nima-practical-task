import os
from rest_framework.response import Response
from cord4_task.category.models import Category
from cord4_task.category.serializers import CategorySerializer, FileUploadSerializer
from rest_framework import status, viewsets, permissions
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from django.conf import settings
from cord4_task.utils.permission import IsAdminOrReadOnly, IsReadAction
from .tasks import process_category_json


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_deleted=False)
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated, IsReadAction | IsAdminUser,)
    ordering_fields = ('created',)


class CategoryUploadView(APIView):
    """JSON file uploads and triggers Celery task."""
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']

            # Save file temporary
            file_path = os.path.join(settings.MEDIA_ROOT, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # Trigger Celery task
            process_category_json.delay(file_path)

            return Response({'message': 'File uploaded successfully. Processing in background.'},
                            status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
