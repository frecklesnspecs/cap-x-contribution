from django.urls import path

from . import views

app_name = "bug"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.InfoView.as_view(), name="info"),
    # ex: /bug/new/
    path("new/", views.new, name="new"),
    # ex: /bug/save/
    path("save/", views.save, name="save")
]
