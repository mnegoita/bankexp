from django.urls import path
from django.contrib.auth import views as auth_views
from users import views as users_views

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login_form.html'), name='login'),
    path('logout/', users_views.logout_view, name='logout'),
]

 
 
 

