from backend.celery import app
from api.serializers import FileSerializer


@app.task(name="handle_uploaded_file")
def handle_uploaded_file(serializer: FileSerializer) -> None:
    file_id = serializer.instance.id
    obj = serializer.Meta.model.objects.filter(id=file_id).first()
    obj.processed = True
    obj.save()
