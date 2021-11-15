from django.db import models


class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    uploaded = models.DateTimeField(auto_now_add=True)
    is_special = models.BooleanField(default=False)
    
    def filename(self):
        return self.docfile.name.split('/')[-1]
