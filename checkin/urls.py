from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('login'))),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
     path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('password/', views.change_password, name='password_change'),
    
]
