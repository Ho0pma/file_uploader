from django.shortcuts import render
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import File
from .serializers import FileSerializer
from .tasks import process_file

class FileViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    @action(detail=False, methods=['post', 'get'])
    def upload(self, request):
        if request.method == 'POST':
            files = request.FILES.getlist('file')
            file_objs = []

            for uploaded_file in files:
                # Валидация загружаемого файла
                self.validate_file(uploaded_file)

                # Создаем и сохраняем объект File для каждого файла
                file_obj = File(file=uploaded_file)
                file_obj.save()
                file_objs.append(file_obj)

                # Запускаем асинхронную задачу для обработки файла
                try:
                    process_file.delay(file_obj.id)

                except Exception as e:
                    # Удаляем файл, если задача Celery не была запущена
                    file_obj.delete()
                    return Response({'error': 'Ошибка при запуске асинхронной задачи.'},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            serializer = FileSerializer(file_objs, many=True)

            # первый вар вывода:
            response_data = {
                'files': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

            # второй вар через шаблон:
            # return render(
            #     request=request,
            #     template_name='app/success.html',
            #     status=status.HTTP_201_CREATED,
            #     context={'uploaded_files': serializer.data, 'status': status.HTTP_201_CREATED},
            # )

        elif request.method == 'GET':
            # Возвращаем HTML-форму для загрузки файлов
            return render(request, 'app/upload_form.html')

    def validate_file(self, uploaded_file):
        # Пример валидации типа и размера файла
        MAX_FILE_SIZE = 10485760  # 10 MB
        ALLOWED_FILE_TYPES = ['txt', 'pdf', 'png', 'jpg', 'jpeg']

        if uploaded_file.size > MAX_FILE_SIZE:
            raise ValidationError(f"Файл {uploaded_file.name} слишком большой. Максимальный размер: 10 MB.")

        if not uploaded_file.name.split('.')[-1] in ALLOWED_FILE_TYPES:
            raise ValidationError(
                f"Недопустимый тип файла: {uploaded_file.name}. Разрешенные типы: {', '.join(ALLOWED_FILE_TYPES)}.")