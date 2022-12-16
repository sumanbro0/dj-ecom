from . import views
from django.urls import path


urlpatterns = [
    path("", views.index, name="index"),
    path("track/", views.track, name="track"),
    path("search/", views.search, name="search"),
    path("change/", views.change, name="change"),
    path("change_pwd/<uid>/", views.change_pwd, name="change_pwd"),
    path("change_name/<id>/", views.change_name, name="change_name"),
]
