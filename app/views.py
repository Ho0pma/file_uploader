from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render
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
                serializer = self.serializer_class(data={'file': uploaded_file})

                # проверка, что файл валидный (через сериализатор)
                if serializer.is_valid():
                    file_obj = serializer.save()
                    file_objs.append(file_obj)

                    # Запускаем асинхронную задачу для обработки файла
                    try:
                        process_file.delay(file_obj.id)
                    except Exception as e:
                        # Удаляем файл, если задача Celery не была запущена
                        file_obj.delete()
                        return Response({'error': 'Ошибка при запуске асинхронной задачи.'},
                                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            serializer = FileSerializer(file_objs, many=True)

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