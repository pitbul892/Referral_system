from django.urls import path

from .views import GetByEmailView, ReferralCodeView, ReferralView

urlpatterns = [

    path('referral-code/', ReferralCodeView.as_view(), name='referral_code'),
    path('referral-code/email/', GetByEmailView.as_view(),
         name='referral_code_email'),
    path('referrals/<int:pk>/', ReferralView.as_view(),
         name='detail_referral_code'),
]
