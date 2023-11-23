from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import views, response, exceptions, generics, permissions
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate, get_user_model
from .serializers import UserSerializer, RegisterSerializer


class UserList(generics.ListAPIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def delete(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs['pk'])
        if user != request.user:
            raise exceptions.PermissionDenied("You can't delete another user.")
        return super(UserDetail, self).delete(request, *args, **kwargs)


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        return user


class LoginView(ObtainAuthToken):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    def post(self, request, *args, **kwargs):
        resp = super(LoginView, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=resp.data['token'])
        user = token.user
        login(request, user)
        resp2 = response.Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
        })
        return resp2


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return response.Response(status=204)


class CheckLogin(views.APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request):
        if not request.user.is_authenticated:
            raise exceptions.PermissionDenied("You are not logged in.")
        # If Authorized, return user
        login(request, request.user)
        return response.Response({
            'user_id': request.user.pk,
            'username': request.user.username,
        })

