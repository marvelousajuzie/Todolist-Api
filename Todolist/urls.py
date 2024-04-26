from django.urls import path, include
from .views import CustomUserRegister, CustomUserLogin,TodoView
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter


# router = DefaultRouter()
# router.register(r'todo', TodoView, basename= 'Todoist')
# router.register(r'register', CustomUserRegister, basename= 'register')
# router.register(r'login', CustomUserLogin, basename= 'login')
# router.register(r'token', obtain_auth_token, basename= 'obtain')


urlpatterns = [
    path('listproduct/', TodoView.as_view({'get': 'list'})),
    path('createproduct/', TodoView.as_view({'get': 'create'})),
    path('updateproduct/', TodoView.as_view({'get': 'update'})),
    path('destroyproduct/', TodoView.as_view({'get': 'destroy'})),


    path('register/', CustomUserRegister.as_view({'get': 'create'})),
    path('login/', CustomUserLogin.as_view({'get': 'create'})),

    # path('', include(router.urls)),
]
