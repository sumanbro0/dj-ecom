from . import views
from django.urls import path


urlpatterns = [path("verify/<username>", views.verify, name="verify")]
