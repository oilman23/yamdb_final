from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAdmin
from .serializers import AuthDataSerializer, UserSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    lookup_field = 'username'

    @action(detail=False, methods=['patch', 'get'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        if self.request.method == 'GET':
            data = UserSerializer(self.request.user).data
            return Response(data)
        serializer = UserSerializer(self.request.user, data=request.data,
                                    partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=self.request.user.role)
        return Response(serializer.data)


def email_to_user(user, subject, message):
    send_mail(
        subject,
        message,
        settings.DOMAIN_EMAIL,
        [user.email]
    )


class APIGetConfirmationCodeByEmail(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AuthDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        user = User.objects.get_or_create(email=email, username=username)
        confirmation_code = default_token_generator.make_token(user)
        message = (
            'Используйте:\n'
            f'email: {email}\n'
            f'confirmation code: {confirmation_code}\n'
            'для получения токена.'
        )
        email_to_user(user, 'YaMDb: данные для получения токена', message)

        return Response({'email': serializer.data['email']})


class APIGetToken(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AuthDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data['confirmation_code']

        email = serializer.validated_data['email']
        username = serializer.validated_data['username']

        user = get_object_or_404(User, email=email, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            refresh = RefreshToken.for_user(user)
            return Response({'token': str(refresh.access_token)})
        return Response('Введен неправильный confirmation_code')
