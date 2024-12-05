from django.urls import path
from . import views

urlpatterns = [

    # path('',views.login,name='login'),
    # path('register',views.register),

# -------------------user-------------------------

    path("", views.index, name="index"),
    path("picture", views.picture, name="picture"),
    path("favorite", views.favorite, name="favorite"),
    path('add',views.add),
    path('view_all',views.view_all)
]