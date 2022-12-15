from . import views
from django.urls import path


urlpatterns = [
    path("<slug>", views.get_product, name="get_product"),
    path("add_product/", views.add_product, name="add_product"),
]
