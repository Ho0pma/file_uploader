from celery import shared_task
from app.models import File


# example
@shared_task
def bar():
    return 'Hello!'


@shared_task
def process_file(file_id):
    try:
        file_obj = File.objects.get(id=file_id)
        file_obj.processed = True
        file_obj.save()

    except File.DoesNotExist:
        return 'FileDoesNotExist'
