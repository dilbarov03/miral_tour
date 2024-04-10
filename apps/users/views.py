from rest_framework import generics
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.tour.models import Tour
from apps.tour.serializers import TourListSerializer
from apps.users.models import User
from apps.users.serializers import EmailSerializer, VerifyCodeSerializer, UserSerializer, SavedTourSerializer, \
    OrderCreateSerializer
from apps.users.verification import send_code, verify_code_cache


class SendCodeAPIView(generics.GenericAPIView):
    serializer_class = EmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")

        success, message = send_code(email)
        return Response({"success": success, "message": message})


class VerifyCodeAPIView(generics.GenericAPIView):
    serializer_class = VerifyCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        code = request.data.get("code")

        success, message = verify_code_cache(email, code)
        if success:
            user, created = User.objects.get_or_create(email=email)
            refresh = RefreshToken.for_user(user)
            return Response({"access": str(refresh.access_token), "refresh": str(refresh)})

        return Response({"success": success, "message": message}, status=400)


class UserProfileAPIView(generics.RetrieveAPIView, generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user


class SavedTourAPIView(generics.ListAPIView):
    serializer_class = TourListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Tour.objects.filter(saved_tours__user=self.request.user)


class SavedTourCreateView(generics.CreateAPIView):
    serializer_class = SavedTourSerializer
    permission_classes = (IsAuthenticated,)


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, JSONParser)
