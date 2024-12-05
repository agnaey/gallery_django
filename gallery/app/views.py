from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os


# Create your views here.

# def login(req):
#     return render(req,'login.html')

# def register(req):
#     return render(req,'register.html')

# ------------------user-------------------------
def index(request):
    return render(request, 'user/index.html')

def picture(request):
    return render(request, 'user/picture.html')

def favorite(request):
    return render(request, 'user/favorite.html')

def view_all(req):
    return render(req,'user/view_all.html')

def add(req):
    if req.method=='POST':
        file_id=req.POST['file_id']
        name=req.POST.get['name']
        file=req.FILES.get('file')

        category=req.POST.get('gallery')
        
        if category == 'image':
            process_images(file,name)

        elif category == 'video':
            process_video(file,name)

        elif category == 'audio':
            process_audio(file,name)

        elif category == 'oyhers':
            process_others(file,name)

    return render(req,'user/add.html')

def process_images(file, name):
    save_file(file,'media/images',name)

def process_video(file, name):
    save_file(file,'media/video',name)

def process_audio(file, name):
    save_file(file,'media/audio',name)

def process_others(file, name):
    save_file(file,'media/others',name)

def save_file(file, subdirectory, name):
    fs=FileSystemStorage('media',location=subdirectory)
    if not os.path.exists(subdirectory):
        os.makedirs(subdirectory)
        #save
    fs.save(name,file)
    print(f"file saves to{subdirectory}/{name}")
    