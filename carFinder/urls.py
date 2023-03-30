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
	path('cars/', views.car_list, name='car_list'),
	path('models/', views.model_list, name='model_list'),
	path('brands/', views.brand_list, name='brand_list'),
	path('cars/all', views.all_cars, name='all_cars'),
]
