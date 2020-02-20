from django.urls import path
from . import views

urlpatterns = [
	path('',views.index),
	path('register', views.register),
	path('login_process', views.login_process),
	path('success', views.success),
	path('logout', views.logout),
]