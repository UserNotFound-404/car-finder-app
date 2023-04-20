from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView, \
    DestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token

from carFinder.models import Car, Brand, Model, Profile
from .permissions import CurrentUserPermission, CanEditCar
from .serializers import (
    CarSerializer,
    BrandSerializer,
    CarModelSerializer,
    UserRegisterSerializer,
    ProfileSerializer, UserInfoSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from .filters import CarFilter, BrandFilter, ModelFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class CarsOnSaleListView(ListAPIView):
    queryset = Car.objects.filter(on_sale=True)
    serializer_class = CarSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitOffsetPagination

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class CarsListView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = CarFilter
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitOffsetPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class CarRetrieveView(RetrieveUpdateAPIView):
    serializer_class = CarSerializer
    queryset = Car.objects.all()
    permission_classes = (IsAuthenticated, CanEditCar)

    def put(self, request, *args, **kwargs):
        print(request.data)
        return self.update(request, partial=True, *args, **kwargs)


class CarFavoriteView(APIView):
    serializer_class = CarSerializer
    queryset = Car.objects.all()
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk, *args, **kwargs):
        car_instance = Car.objects.get(pk=pk)
        profile_instance = Profile.objects.get(user=request.user)
        if car_instance not in profile_instance.favorite_cars.all():
            profile_instance.favorite_cars.add(car_instance)
            profile_instance.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response({'detail': 'Car already added to favorites.'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        car_instance = self.get_object()
        profile_instance = Profile.objects.get(user=request.user)
        profile_instance.favorite_cars.remove(car_instance)
        profile_instance.save()
        return Response(status=status.HTTP_202_ACCEPTED)


class CarDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, CanEditCar]
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)

    # def get_object(self):
    #     queryset = self.get_queryset()
    #     obj = get_object_or_404(queryset, pk=self.kwargs.get('pk'))
    #     self.check_object_permissions(self.request, obj)
    #     return obj


class CarCreateView(CreateAPIView):
    serializer_class = CarSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BrandListView(ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = BrandFilter
    search_fields = ['name', 'country']
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ModelListView(ListAPIView):
    queryset = Model.objects.all()
    serializer_class = CarModelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ModelFilter
    search_fields = ['name', 'year', 'body_style']
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserCreateView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = ()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
            user_profile = Profile(user=user)
            user_profile.save()
            refresh = RefreshToken.for_user(user)
            token = {"refresh": str(refresh), "access": str(refresh.access_token)}
            return Response(token, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return JsonResponse({'message': 'Logged out successfully'})


class UserLoginView(APIView):
    serializer_class = AuthTokenSerializer
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Logged in successfully',
                'username': user.username, 'id': user.id,
                'email': user.email, 'token': token.key
            })
        return Response({'message': 'Invalid credentials'})


class ProfileView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, CurrentUserPermission]

    def get(self, request, *args, **kwargs):
        profile_instance = Profile.objects.get(user=request.user)
        profile_serializer = self.get_serializer(profile_instance)
        return Response(profile_serializer.data)

    def put(self, request, *args, **kwargs):
        instance = Profile.objects.get(user=request.user)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


