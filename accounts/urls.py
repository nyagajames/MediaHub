from django.urls import path 
'''django auths view : to give access to configured
authenication operations in django'''
from django.contrib.auth import views as auth_views
'''import the custom views functionalities'''
from . import views
## give a label for the routes : 'accounts:login'
app_name = 'accounts'
## register the urls paths by mapping to appropriate
## view method 
urlpatterns = [
    path('register/', views.register_view, 
    name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view,
     name='profile'),
    # path followed on request for reset process
     path('password-reset/',
     views.CustomPasswordResetView.as_view(),
     name='password_reset'),
    # django inbuilt path to check if the user exists 
    # and whether email can be changed 
     path('password-reset/done/',
     auth_views.PasswordChangeDoneView.as_view(
     template_name='accounts/password_reset_done.html'
     ), name='password_reset_done'),
     ## this is the path that confirms password has 
     ## been changed 
     path('password-reset-confirm/<uidb64>/<token>/',
     views.CustomPasswordResetConfirmView.as_view(),
     name='password_reset_confirm'),
     ## path to indicate the completion of reset process
     path('password-reset-complete', 
     auth_views.PasswordResetCompleteView.as_view(
     template_name='accounts/password_reset_complete.html'
     ), name='password_reset_complete')

]

