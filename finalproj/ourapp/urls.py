from django.contrib import admin
from django.urls import path
from ourapp.views import (
    StudentCreateView,
    StudentListView, 
    
    StudentUpdateView, 
    StudentDeleteView,
    viewattendance,
    trainmodel,
    takeattendance,
    moreimages, 
    exportattendance

)
app_name = "ourapp"

urlpatterns = [
     path('',StudentListView.as_view(), name = "student-list"),
     path("student_create/",StudentCreateView.as_view(), name = "student-create"),
     path('<int:pk>/update/', StudentUpdateView.as_view(), name = "student-update"), 
     path("<int:pk>/delete/", StudentDeleteView.as_view(), name = "student-delete"), 
     path("takeattendance/", takeattendance, name = "take-attendance"),
     path('viewattendance/',viewattendance, name = "view-attendance"),
     path("trainmodel/", trainmodel, name = "trainmodel"),
     path("<int:pk>/moreimage",moreimages, name = "moreimages"),
     path("exportcsv/",exportattendance, name = "exportattendance"),
     #path('img_upload/', StudentImage.as_view(), name = "image-upload"), 
]




