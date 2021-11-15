from django.shortcuts import redirect, render
from .models import Document
from .forms import DocumentForm
import os
from django.conf import settings
from django.http import HttpResponse, Http404
import zipfile
from django.utils import timezone
from datetime import datetime
import shutil

class Usage:
    used = None
    total = None
    
    def __init__(self, used, total):
        self.used, self.total = used, total
    
    def __add__(self, o):
        self.used += o.used
        return self

def get_size(start_path='.', exclude=[]):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        dirnames[:] = [d for d in dirnames if d not in exclude]
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return Usage(total_size, 512 * 1024 * 1024)

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(
                os.path.join(root, file),
                os.path.relpath(
                    os.path.join(root, file),
                    os.path.join(path, '..'))
                )

def my_view(request):
    message = 'Upload as many files as you want!'
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            extention = newdoc.docfile.name.split('.')[-1]
            newdoc.docfile.name = f'{request.POST["name"]}_{request.POST["surename"]}_{request.POST["classe"]}.{extention}'.lower()
            newdoc.save()

            # Redirect to the document list after POST
            return redirect('my-view')
        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = DocumentForm()  # An empty, unbound form

    context = {'form': form, 'message': message}
    return render(request, 'list.html', context)

def download(request):
    raise NotImplementedError
    zipf = zipfile.ZipFile('minimal/media/all_videos.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('minimal/media/documents/', zipf)
    zipf.close()
    
    newdoc = Document()
    newdoc.docfile.name = 'all_videos.zip'
    newdoc.save()
    
    response = HttpResponse(newdoc.docfile, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=all_videos.zip'

    return response

def videos(request):
    # documents = Document.objects.filter(is_special=True)
    # for doc in documents:
    #     doc.delete()
    
    # disk_usage = get_size(os.path.expanduser("~"))
    disk_usage = get_size(settings.MEDIA_ROOT) + DISK_USED
    # disk_usage = shutil.disk_usage(os.path.expanduser("~"))
    # disk_usage = shutil.disk_usage(settings.MEDIA_ROOT)
    disk_usage_perc = int(disk_usage.used / disk_usage.total * 100) 
    
    # filename = datetime.strftime(timezone.now(), 'all_videos_%Y%m%d_%H%M%S.zip')
    # zipf = zipfile.ZipFile(os.path.join(settings.MEDIA_ROOT, filename), 'w', zipfile.ZIP_DEFLATED)
    # zipdir(os.path.join(settings.MEDIA_ROOT, 'documents'), zipf)
    # zipf.close()
    
    # newdoc = Document()
    # newdoc.docfile.name = filename
    # newdoc.is_special = True
    # newdoc.save()
    
    documents = Document.objects.filter(is_special=False)
    context = {'documents': documents, 'disk_usage':disk_usage, 'disk_usage_perc':disk_usage_perc}
    return render(request, 'videos.html', context)

print('Loading disk usage...')
DISK_USED = get_size(os.path.expanduser("~"), exclude=[settings.MEDIA_ROOT])