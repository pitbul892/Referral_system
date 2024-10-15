from django.contrib.auth import get_user_model
from rest_framework import serializers

from referrals.models import Referral, ReferralCode

User = get_user_model()


class ReferralCodeSerializer(serializers.ModelSerializer):
    """Сериалайзер реферального кода."""

    expiration_date = serializers.DateField(required=True)

    class Meta:
        model = ReferralCode
        fields = ['user', 'code', 'expiration_date']
        read_only_fields = ['user', 'code']


class ReferralSerializer(serializers.ModelSerializer):
    """Сериалайзер реферала."""

    referred_user = serializers.StringRelatedField()

    class Meta:
        model = Referral
        fields = ['referred_user']


class RegisterWithReferralSerializer(serializers.ModelSerializer):
    """Сериалайзер для регистрации по реферальному коду."""

    referral_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'referral_code']

    def create(self, validated_data):
        referral_code = validated_data.pop('referral_code')
        username = validated_data.get('username')
        password = validated_data.get('password')

        try:
            referral = ReferralCode.objects.get(code=referral_code)
            if not referral.is_valid():
                raise serializers.ValidationError("Referral code has expired.")
            user = User.objects.create_user(
                username=username, password=password
            )
            Referral.objects.create(referrer=referral.user, referred_user=user)
            return user
        except ReferralCode.DoesNotExist:
            raise serializers.ValidationError("Invalid referral code.")
