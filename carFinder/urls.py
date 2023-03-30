from django.urls import path
from . import views
from django.contrib import admin
from django.contrib.auth.views import LogoutView

urlpatterns = [
	path('', views.index, name='home'),
	path('admin/', admin.site.urls),
	path('user/create/', views.register_request, name='register'),
	path('user/login/', views.login_request, name='login'),
	path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]
