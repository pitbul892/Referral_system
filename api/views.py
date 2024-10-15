from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from referrals.models import ReferralCode
from .serializers import (ReferralCodeSerializer, ReferralSerializer,
                          RegisterWithReferralSerializer)

User = get_user_model()


class ReferralCodeView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=ReferralCodeSerializer,
        responses={
            201: ReferralCodeSerializer,
            400: 'Bad Request',
        }
    )
    def post(self, request):
        user = request.user
        if ReferralCode.objects.filter(user=user).exists():
            return Response(
                {"detail": "You already have a referral code."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ReferralCodeSerializer(data=request.data)
        if serializer.is_valid():
            code = get_random_string(10).upper()
            expiration_date = serializer.validated_data['expiration_date']
            ReferralCode.objects.create(
                user=user, code=code, expiration_date=expiration_date
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        if ReferralCode.objects.filter(user=user).exists():
            user.referral_code.delete()
            return Response(
                {"detail": "Referral code deleted successfully."},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {"detail": "There is no active referral code."},
            status=status.HTTP_400_BAD_REQUEST
        )


class GetByEmailView(APIView):
    @swagger_auto_schema(
        responses={
            200: 'Ok',
            400: 'Bad Request',
        }
    )
    def get(self, request):
        user = request.user
        try:
            code = ReferralCode.objects.get(user=user)
        except ReferralCode.DoesNotExist:
            return Response(
                {"detail": "There is no active referral code."},
                status=status.HTTP_400_BAD_REQUEST
            )
        text = (f'Your referral code: {code.code}.'
                f'The code is valid until: {code.expiration_date}')
        if user.email:
            send_mail(
                subject='Referral code',
                message=text,
                from_email=user.email,
                recipient_list=['to@example.com'],
                fail_silently=True,
            )
            return Response(
                {"detail": "Referral code has been sent to your email."},
                status=status.HTTP_200_OK
            )
        raise ValidationError("User does not have a valid email address.")


class ReferralView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            201: ReferralSerializer,
            400: 'Bad Request',
            404: 'Not found'
        }
    )
    def get(self, request, pk):
        try:
            referrer = User.objects.get(id=pk)
            referrals = referrer.referrals.all()
            serializer = ReferralSerializer(referrals, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {"detail": "Referrer not found."},
                status=status.HTTP_404_NOT_FOUND
            )


class RegisterWithReferralView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=RegisterWithReferralSerializer,
        responses={
            201: 'Created',
            400: 'Bad Request',
        }
    )
    def post(self, request):
        serializer = RegisterWithReferralSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
