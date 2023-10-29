from django.urls import path

from . import views

app_name = "bug"
urlpatterns = [
    # ex: /bug/
    path("", views.index, name="index"),
    # ex: /bug/5/
    path("<int:bug_id>/", views.info, name="info"),
    # ex: /bug/new/
    path("new/", views.new, name="new"),
    # ex: /bug/save/
    path("save/", views.save, name="save")
]
