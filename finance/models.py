from django.db import models
from django.conf import settings
from django.utils import timezone


class SubscriptionPlan(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان پلن")
    months = models.PositiveIntegerField(verbose_name="مدت زمان (ماه)")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="قیمت (تومان)")
    is_special = models.BooleanField(default=False, verbose_name="پلن ویژه")
    features = models.TextField(help_text="ویژگی‌ها را با کاما (,) جدا کنید", verbose_name="ویژگی‌ها")

    def __str__(self):
        return self.title

class WalletTransaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'شارژ کیف پول'),
        ('purchase', 'خرید اشتراک'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='finance_transactions')
    title = models.CharField(max_length=255, verbose_name="عنوان تراکنش")
    amount = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="مبلغ (تومان)")
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, default='deposit')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.title} - {self.amount}"

class UserSubscription(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    expires_at = models.DateTimeField(verbose_name="تاریخ انقضا")

    def is_valid(self):
        return self.expires_at > timezone.now()

    def __str__(self):
        return f"{self.user} - تا {self.expires_at.strftime('%Y/%m/%d')}"