from django.urls import path
from .views import WalletDashboardView, WalletDepositView, BuySubscriptionView, CancelSubscriptionView

urlpatterns = [
    path('dashboard/', WalletDashboardView.as_view(), name='wallet-dashboard'),
    path('deposit/', WalletDepositView.as_view(), name='wallet-deposit'),
    path('buy-plan/<int:plan_id>/', BuySubscriptionView.as_view(), name='wallet-buy-plan'),
    path('subscription/cancel/', CancelSubscriptionView.as_view(), name='cancel_subscription'), 
]