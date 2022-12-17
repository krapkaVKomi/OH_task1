from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='post_list'),
    path("test/", views.document_save, name='document_save'),
]
