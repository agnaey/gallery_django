from django.shortcuts import render,redirect,get_object_or_404
from .models import gallery,favorite
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
            return redirect(login_user)
    return render(req,'login.html')

def logout_user(req):
    logout(req)
    req.session.flush()
    return redirect(login_user)

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
    print(images,videos,audios)

    context = {
        'images': images,
        'videos': videos,
        'audios': audios,
        'others': others,
    }
    return render(request, 'user/index.html',context)
def delete(request,id):
    data=gallery.objects.get(pk=id)
    data.delete()
    return redirect(index)

def delete_file(request, id):

    return redirect('view_all_file')




def picture(request, id):
    media_file = get_object_or_404(gallery, id=id)
    url = media_file.file.url

    return render(request, "user/picture.html", {"url": url})

def favorites(request,id):
    return render(request, 'user/favorite.html')

    # images=gallery.objects.filter(images=True)
def view_all_file(req):
    file_type = req.GET.get('type', 'images') 
    if file_type == 'videos':
        files = gallery.objects.filter(video=True)
    elif file_type == 'audios':
        files = gallery.objects.filter(audio=True)
    elif file_type == 'others':
        files = gallery.objects.filter(others=True)
    else:
        files = gallery.objects.filter(images=True)

    context = {
        'files': files,
        'file_type': file_type,
    }
    return render(req, 'user/view_all_file.html', context)

    # return render(req,'user/view_all_img.html',{'images':images})

def see_more(req,a):
    file_type = req.GET.get('type', a) 
    if file_type == 'videos':
        files = gallery.objects.filter(video=True)
    elif file_type == 'audios':
        files = gallery.objects.filter(audio=True)
    elif file_type == 'others':
        files = gallery.objects.filter(others=True)
    else:
        files = gallery.objects.filter(images=True)

    context = {
        'files': files,
        'file_type': file_type,
    }
    return render(req,'user/see_more.html',context)

# def view_all_vid(req):
#     return render(req,'user/view_all_video.html')

# def view_all_audio(req):
#     return render(req,'user/view_all_audio.html')

# def view_others(req):
#     return render(req,'user/view_others.html')

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

def favorites_page(request):
    user =User.objects.get(username=request.user.username)
    favorites = favorite.objects.filter( user=user)[::-1]
    return render(request, 'user/favorite.html' , {'favorites': favorites})


def add_to_fav(request,id):
    gallerys=gallery.objects.get(id=id)
    user =User.objects.get(username=request.session['user'])
    data=favorite.objects.create(user=user,gallery=gallerys)
    data.save()
    return redirect('fav')

def fav_delete(req,id):
    data=favorite.objects.get(pk=id)
    data.delete()
    return redirect(favorites_page)