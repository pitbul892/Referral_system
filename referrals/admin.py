from django.contrib import admin

from .models import Referral, ReferralCode

admin.site.register(ReferralCode)
admin.site.register(Referral)
