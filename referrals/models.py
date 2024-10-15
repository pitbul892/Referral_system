from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class ReferralCode(models.Model):
    """Модель реф. кода."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="referral_code"
    )
    code = models.CharField(max_length=10, unique=True)
    expiration_date = models.DateTimeField()

    def is_valid(self):
        return self.expiration_date > timezone.now()

    class Meta:
        verbose_name = 'Реферальный код'
        verbose_name_plural = 'Реферальные коды'

    def __str__(self):
        """Имя."""
        return self.user.username


class Referral(models.Model):
    referrer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="referrals"
    )
    referred_user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="referred_by"
    )

    def __str__(self):
        return f"{self.user} referred by {self.referrer}"
