from rest_framework import serializers
from .models import File
from .validators import validate_file

class FileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(validators=[validate_file])

    class Meta:
        model = File
        fields = ('id', 'file', 'uploaded_at', 'processed')
