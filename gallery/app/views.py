from django.shortcuts import render,redirect,get_object_or_404
from .models import gallery
import os
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

def login_user(req):
    if 'user' in req.session:
        return redirect('index')
    else:
        if req.method == 'POST':
            username = req.POST.get('username')
            password = req.POST.get('password')
            data=authenticate(username=username,password=password)
            if data:
                login(req,data)
                req.session['user'] = username
                return redirect('index')
            else:
                messages.info(req,'invalid credentials')
            return redirect('login')
    return render(req,'login.html')

def logout_user(req):
    logout(req)
    req.session.flush()
    return redirect('login')

def register(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        email = req.POST.get('email')
        password = req.POST.get('password')
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return redirect('login')
        except Exception as e:
            messages.info(req, 'Invalid details, user may already exist')
            return redirect('/register')
    return render(req, 'register.html')
# ------------------user-------------------------
def index(request):
    images = gallery.objects.filter(images=True)
    videos = gallery.objects.filter(video=True)
    audios = gallery.objects.filter(audio=True)
    others = gallery.objects.filter(others=True)

    context = {
        'images': images,
        'videos': videos,
        'audios': audios,
        'others': others,
    }
    return render(request, 'user/index.html',context)
def delete(request,id):
    image = gallery.objects.get(id=id)
    if os.path.exists(image.file.path):
        os.remove(image.file.path)
    image.delete()
    return redirect('index')


def picture(request, id):
    media_file = get_object_or_404(gallery, id=id)
    url = media_file.file.url

    
    return render(request, "user/picture.html", {"url": url})

def favorite(request,id):
    return render(request, 'user/favorite.html')

def view_all(req):
    return render(req,'user/view_all.html')

def add(request):
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        name = request.POST.get('name')
        file = request.FILES.get('file')
        category = request.POST.get('gallery')

        
        images = False
        video = False
        audio = False
        others = False

        # Set the correct Boolean field based on the category
        if category == 'Image':
            images = True
        elif category == 'Video':
            video = True
        elif category == 'Audio':
            audio = True
        elif category == 'Others':
            others = True

        if file_id and name and file and category:
            gallery.objects.create(
                file_id=file_id,
                name=name,
                file=file,
                images=images,
                video=video,
                audio=audio,
                others=others
            )
            return render(request, 'user/add.html', {'success': True})

    return render(request, 'user/add.html')

    