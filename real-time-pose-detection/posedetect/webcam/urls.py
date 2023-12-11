from django.urls import path
from . import views

urlpatterns = [
    # path('',views.camera,name='camera'),
    path('',views.SignupPage,name='signup'),
    path('receive_landmark_data', views.receive_landmark_data, name='receive_landmark_data'),
    path('login',views.LoginPage,name='login'),
    path('camera',views.HomePage,name='home'),
    path('logout',views.LogoutPage,name='logout'),
    path('about',views.AboutPage,name='about'),
    path('image',views.ImagePage,name='image')

]