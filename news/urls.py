from django.urls import path
from .views import *

urlpatterns = [
    path('news/',NewsList.as_view()),
     
]
