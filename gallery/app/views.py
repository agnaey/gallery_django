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
            username = req.POST['username']
            password = req.POST['password']
            data=authenticate(username=username,password=password)
            if data:
                login(req,data)
                req.session['user'] = username
                return redirect('index')
            else:
                messages.info(req,'invalid username or password')
            return redirect(login_user)
    return render(req,'login.html')

def logout_user(req):
    logout(req)
    req.session.flush()
    return redirect(login_user)

def register(req):
    if req.method == 'POST':
        username = req.POST['username']
        email = req.POST['email']
        password = req.POST['password']
        try:
            user = User.objects.create_user(first_name=username,username=email, email=email, password=password)
            user.save()
            messages.success(req, 'Account created successfully')
            return redirect('login')
        except:
            messages.info(req, 'Invalid details, user may already exist')
            return redirect('/register')
    return render(req, 'register.html')
# ------------------user-------------------------
def index(request):
    log_user=User.objects.get(username=request.session['user'])
    images = gallery.objects.filter(images=True , user=log_user)
    videos = gallery.objects.filter(video=True, user=log_user)
    audios = gallery.objects.filter(audio=True, user=log_user)
    others = gallery.objects.filter(others=True, user=log_user)
    print(images)

    context = {
        'images': images,
        'videos': videos,
        'audios': audios,
        'others': others,
    }
    try:
        fav1=favorite.objects.get(context=context,user=log_user)
    except:
        fav1=None
        print(fav1)
    return render(request, 'user_side/index.html',context,)

def delete(request,id):
    data=gallery.objects.get(pk=id)
    data.delete()
    return redirect(index)

def delete_file(request, id):
    data=gallery.objects.get(pk=id)
    data.delete()
    return redirect(see_more,a='default')



def picture(request, id):
    media_file = get_object_or_404(gallery, id=id)
    url = media_file.file.url

    return render(request, "user_side/picture.html", {"url": url})



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
    return render(req, 'user_side/see_more.html', context)


def see_more(req,a=None):
    log_user=User.objects.get(username=req.session['user'])
    if a is None:
        a='default'
    file_type = req.GET.get('type', a) 
    if file_type == 'videos':
        files = gallery.objects.filter(video=True, user=log_user)
    elif file_type == 'audios':
        files = gallery.objects.filter(audio=True, user=log_user)
    elif file_type == 'others':
        files = gallery.objects.filter(others=True, user=log_user)
    else:
        files = gallery.objects.filter(images=True, user=log_user)

    context = {'files': files,'file_type': file_type,}
    return render(req,'user_side/see_more.html',context)

# def view_all_vid(req):
#     return render(req,'user_side/view_all_video.html')

# def view_all_audio(req):
#     return render(req,'user_side/view_all_audio.html')

# def view_others(req):
#     return render(req,'user_side/view_others.html')

def add(request):
    log_user=User.objects.get(username=request.session['user'])
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
                user=log_user,
                file_id=file_id,
                name=name,
                file=file,
                images=images,
                video=video,
                audio=audio,
                others=others
            )
            return render(request, 'user_side/add.html', {'success': True})

    return render(request, 'user_side/add.html')

def favorites_page(request):
    user =User.objects.get(username=request.user.username)
    favorites = favorite.objects.filter( user=user)[::-1]
    return render(request, 'user_side/favorite.html' , {'favorites': favorites})


def add_to_fav(request,id):
    gallerys=gallery.objects.get(id=id)
    user =User.objects.get(username=request.session['user'])
    data=favorite.objects.create(user=user,gallery=gallerys)
    data.save()
    return redirect(favorites_page)

def fav_delete(req,id):
    data=gallery.objects.get(pk=id)
    data.delete()
    return redirect(favorites_page)

def remove_fav(req,id):
    data=favorite.objects.get(pk=id)
    data.delete()
    return redirect(favorites_page)

 
