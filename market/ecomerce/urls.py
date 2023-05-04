from django.urls import path,include
from ecomerce.views import *
urlpatterns = [
    path('assig/login/', logine.as_view()),
    path('assig/register/',Registration.as_view()),


]