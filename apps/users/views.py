import stripe
from django.utils import timezone
from django.utils.translation import gettext as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.tour.models import Tour
from apps.tour.serializers import TourListSerializer
from apps.users.models import User, Order
from apps.users.serializers import EmailSerializer, VerifyCodeSerializer, UserSerializer, SavedTourSerializer, \
    OrderCreateSerializer, UserOrderSerializer
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


class UserDeleteAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        user = request.user
        if user.orders.filter(status="success", tour__from_date__gte=timezone.now().date()).exists():
            return Response({"success": False, "message": _("У вас есть активные заказы. Удаление невозможно.")},
                            status=400)
        request.user.delete()
        return Response({"success": True})


class UserOrdersAPIView(generics.ListAPIView):
    serializer_class = UserOrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.orders.all()


class CreateStripeCheckoutSession(APIView):
    permission_classes = (IsAuthenticated,)

    order_id = openapi.Parameter("order_id", in_=openapi.IN_BODY, type=openapi.TYPE_INTEGER,
                                 required=True)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "order_id": openapi.Schema(type=openapi.TYPE_INTEGER)
        }
    ))
    def post(self, request):
        data = request.data
        order = get_object_or_404(Order, id=data.get("order_id"))
        if order.user != request.user:
            return Response({"success": False, "message": _("Заказ не найден")}, status=404)

        return Response({"checkout_url": "https://example.com/"})

        # checkout_session = stripe.checkout.Session.create(
        #     payment_method_types=["card"],
        #     line_items=[
        #         {
        #             "price_data": {
        #                 "currency": "usd",
        #                 "product_data": {
        #                     "name": order.tarif.title,
        #                 },
        #                 "unit_amount": int(order.tarif.price * 100),
        #             },
        #             "quantity": 1,
        #         },
        #     ],
        #     mode="payment",
        #     success_url="https://example.com/success",
        #     cancel_url="https://example.com/cancel",
        # )
        # return Response({"checkout_url": checkout_session.url})
