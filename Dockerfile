# Используем базовый образ Python версии 3.10
FROM python:3.10

# Устанавливаем переменную окружения для работы Python в неинтерактивном режиме
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /code

# Копируем файлы зависимостей и устанавливаем зависимости
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . /code/

# Определяем команду для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
