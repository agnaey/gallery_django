from django.urls import path
from . import views

urlpatterns = [

    path('',views.login_user),
    path('logout',views.logout_user,name='logout'),
    path('register',views.register),

# -------------------user-------------------------

    path("index", views.index, name="index"),
    path('delete/<id>',views.delete),
    path('delete_file/<id>',views.delete_file),
    path("picture/<id>", views.picture, name="picture"),
    path("fav/<id>", views.favorites),
    path('add_fav/<id>',views.add_to_fav),
    path('remove_fav/<id>',views.fav_delete),
    path('add',views.add),
    path('fav',views.favorites_page),

    path('view_all_file',views.view_all_file),

    path('see_more/<a>',views.see_more)

]
