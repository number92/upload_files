from backend.celery import app

from .models import File


@app.task(name="handle_uploaded_file")
def handle_uploaded_file(file_id: int) -> None:
    obj = File.objects.get(id=file_id)
    obj.processed = True
    obj.save()
