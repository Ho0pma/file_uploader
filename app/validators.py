from django.core.exceptions import ValidationError

def validate_file(uploaded_file):
    MAX_FILE_SIZE = 10485760 # 10 MB
    ALLOWED_FILE_TYPES = ['txt', 'pdf', 'png', 'jpg', 'jpeg']

    if uploaded_file.size > MAX_FILE_SIZE:
        raise ValidationError(f"Файл {uploaded_file.name} слишком большой. Максимальный размер: 10 MB.")

    if not uploaded_file.name.split('.')[-1].lower() in ALLOWED_FILE_TYPES:
        raise ValidationError(f"Недопустимый тип файла: {uploaded_file.name}. Разрешенные типы: {', '.join(ALLOWED_FILE_TYPES)}.")
