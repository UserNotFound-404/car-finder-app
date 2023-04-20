# from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
	path('cars/', CarsOnSaleListView.as_view(), name="cars_on_sale"),
	path('cars/all/', CarsListView.as_view(), name="car_list"),
	path('cars/<int:pk>/', CarRetrieveView.as_view(), name="car_by_id"),
	path('cars/create/', CarCreateView.as_view(), name="create_car"),
	path('brands/', BrandListView.as_view(), name="brand_list"),
	path('models/', ModelListView.as_view(), name="model_list"),
	path('user/create/', UserCreateView.as_view(), name="create_user"),
	path('user/login/', UserLoginView.as_view(), name="login_user"),
	path('user/logout/',  UserLogoutView.as_view(), name='logout'),
	path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
	path('user/myprofile/', ProfileView.as_view(), name='user_profile'),
	path('cars/<int:pk>/fav', CarFavoriteView.as_view(), name='favorited_car'),
	path('cars/<int:pk>/delete', CarDeleteView.as_view(), name='delete_car'),
]
