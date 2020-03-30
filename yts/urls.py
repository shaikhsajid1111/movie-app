from django.contrib import admin
from django.urls import path
from .views import homeView,detailView,searchView,nextPage 
from. import views
urlpatterns = [
    path('', homeView.as_view(),name = "home_page"),
    path('detail/<ids>/',detailView.as_view(),name = "detail"),
    path("search/",searchView.as_view(),name = "search"),
    path('search/detail/<ids>/',detailView.as_view()),
    path("page=<page_number>",nextPage.as_view()),
]
