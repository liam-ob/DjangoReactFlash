from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework import views, response, exceptions, generics, permissions
from django.contrib.auth.models import User
from .serializers import UserSerializer, RegisterSerializer


class UserList(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    authentication_classes = (TokenAuthentication,)
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

    def post(self, request, *args, **kwargs):
        # Add thing token to serializer to make this work please sop the user can log in straight away
        resp = super(RegisterUserAPIView, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=resp.data['token'])
        user = token.user
        resp2 = response.Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username,
        })
        return resp2


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        resp = super(LoginView, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=resp.data['token'])
        user = token.user
        resp2 = response.Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username,
        })
        return resp2


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        request.user.auth_token.delete()
        return response.Response(status=204)


class CheckLogin(views.APIView):
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        print(request.user.is_authenticated)
        # If Authorized, return user
        return response.Response({
            'user_id': request.user.pk,
            'username': request.user.username,
        })

