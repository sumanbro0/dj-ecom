from . import views
from django.urls import path


urlpatterns = [
    path("<slug>", views.get_product, name="get_product"),
]
