from django.urls import path

from . import views
from .views import register, login, search_by_name, search_by_phone_number


urlpatterns = [
    path("", views.index, name="index"),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('protected/', views.protected_route, name='protected_route'),
    path('search/name/', search_by_name, name='search_by_name'),
    path('search/phone_number/', search_by_phone_number, name='search_by_phone_number'),
    path('report_spam/', views.report_spam, name='report_spam'),
   
]