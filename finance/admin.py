from django.contrib import admin
from .models import SubscriptionPlan, WalletTransaction, UserSubscription

admin.site.register(SubscriptionPlan)
admin.site.register(WalletTransaction)
admin.site.register(UserSubscription)