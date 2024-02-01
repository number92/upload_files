from rest_framework import mixins, status, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from upload_file.models import File
from upload_file.tasks import handle_uploaded_file


from .serializers import FileListSerializer, FileSerializer


class UploadFileView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = (FormParser, MultiPartParser)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            file_id = serializer.instance.id
            handle_uploaded_file.delay(file_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = File.objects.all()
    serializer_class = FileListSerializer
