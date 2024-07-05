from django.db import models

class File(models.Model):
    file = models.FileField(
        upload_to='files/%Y',
        default=False,
        blank=True,
        null=True,
        verbose_name='File'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.file.name} - {self.uploaded_at} - Processed: {self.processed}'
