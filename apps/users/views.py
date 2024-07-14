from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

import logging

from apps.tour.models import Tour
from apps.tour.serializers import TourListSerializer
from apps.users.models import User, Order, Payment
from apps.users.payment_serializers import PayzeWebhookSerializer
from apps.users.serializers import EmailSerializer, VerifyCodeSerializer, UserSerializer, SavedTourSerializer, \
    OrderCreateSerializer, UserOrderSerializer, OrderUpdateSerializer
from apps.users.utils import generate_paylink, get_payment_data
from apps.users.verification import send_code, verify_code_cache

logger = logging.getLogger(__name__)


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


class OrderUpdateView(generics.UpdateAPIView):
    serializer_class = OrderUpdateSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, JSONParser)

    def get_queryset(self):
        return self.request.user.orders.all()


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


class CreatePayzeCheckoutSession(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "order_id": openapi.Schema(type=openapi.TYPE_INTEGER),
        }
    ))
    def post(self, request):
        data = request.data
        order = get_object_or_404(Order, id=data.get("order_id"))
        if order.user != request.user:
            return Response({"success": False, "message": _("Заказ не найден")}, status=404)
        if order.status == Order.OrderStatus.SUCCESS:
            return Response({"success": False, "message": _("Заказ уже оплачен")}, status=400)
        elif order.status == Order.OrderStatus.MODERATION:
            return Response({"success": False, "message": _("Заказ на модерации")}, status=400)

        response = generate_paylink(order)
        return Response(response)


class PayzeWebhookAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = PayzeWebhookSerializer(data=request.data)

        print(request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            payment_data = get_payment_data(request.data)
            payment_status = validated_data["PaymentStatus"]

            order_id = validated_data["Metadata"]["Order"]["OrderId"]

            logger.info(f"Order {order_id} is in {payment_status} status.")

            try:
                with transaction.atomic():

                    if payment_status == "Captured":
                        order = Order.objects.filter(id=order_id).first()
                        if order:
                            order.status = Order.OrderStatus.SUCCESS
                            order.save()
                            Payment.objects.create(
                                user=order.user, order=order,
                                **payment_data
                            )
                        else:
                            logger.warning(f"Order {order_id} not found.")

            except Exception as e:
                logger.error(f"Error processing webhook: {e}")
                return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"message": "Webhook received successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
