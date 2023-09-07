from rest_framework import views, response, exceptions, generics, permissions, authentication
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .authentication import create_token, CustomUserAuthentication
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer



class UserDetailAPI(views.APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self,request,*args,**kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return response.Response(serializer.data)


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer





class UserList(generics.ListAPIView, generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class UserDetail(generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [CustomUserAuthentication]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLogin(views.APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        user = User.objects.filter(email=request.data['email']).first()
        user = authenticate(request, username=user.username, password=request.data['password'])
        if user is None:
            raise exceptions.AuthenticationFailed('Invalid Credentials')


        resp = response.Response()
        resp.set_cookie(key='jwt', value=create_token(user_id=request.user.id), httponly=True)

        return resp


class UserLogout(views.APIView):
    authentication_classes = (CustomUserAuthentication,)  # requires authentication
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        resp = response.Response()

        resp.delete_cookie("jwt")

        resp.data = {"message": f"Goodbye {request.user.username}!"}

        return resp

