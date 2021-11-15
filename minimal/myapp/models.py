from django.db import models
from django.dispatch import receiver
import os


class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    uploaded = models.DateTimeField(auto_now_add=True)
    is_special = models.BooleanField(default=False)
    
    def filename(self):
        return self.docfile.name.split('/')[-1]
    
@receiver(models.signals.post_delete, sender=Document)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.docfile:
        if os.path.isfile(instance.docfile.path):
            os.remove(instance.docfile.path)
