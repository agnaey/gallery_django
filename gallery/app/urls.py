from django.urls import path
from . import views

urlpatterns = [

    path('',views.login_user,name='login'),
    path('logout',views.logout_user,name='logout'),
    path('register',views.register),

# -------------------user-------------------------

    path("index", views.index, name="index"),
    path('delete/<id>',views.delete),
    path('delete_file/<id>',views.delete_file),
    path("picture/<id>", views.picture, name="picture"),
    path("fav/<id>", views.favorite, name="favorite"),
    path('add',views.add),

    path('view_all_file',views.view_all_file),
]