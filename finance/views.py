from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import SubscriptionPlan, WalletTransaction, UserSubscription
from .serializers import SubscriptionPlanSerializer, WalletTransactionSerializer
from datetime import timedelta
from django.utils import timezone
from django.core.paginator import Paginator

class WalletDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        plans = SubscriptionPlan.objects.all().order_by('months')
        
        page_number = request.query_params.get('page', 1)
        transactions_qs = WalletTransaction.objects.filter(user=user).order_by('-created_at')
        
        paginator = Paginator(transactions_qs, 5)
        page_obj = paginator.get_page(page_number)

        return Response({
            "balance": f"{int(user.wallet_balance):,}",
            "plans": SubscriptionPlanSerializer(plans, many=True).data,
            "transactions": WalletTransactionSerializer(page_obj.object_list, many=True).data,
            "pagination": {
                "current_page": page_obj.number,
                "total_pages": paginator.num_pages,
                "has_next": page_obj.has_next(),
                "has_previous": page_obj.has_previous()
            }
        })

class WalletDepositView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount')
        try:
            amount = int(amount)
            if amount < 10000:
                return Response({"error": "حداقل مبلغ ۱۰,۰۰۰ تومان است."}, status=status.HTTP_400_BAD_REQUEST)
        except (ValueError, TypeError):
            return Response({"error": "مبلغ نامعتبر است."}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        with transaction.atomic():
            user.wallet_balance += amount
            user.save()

            WalletTransaction.objects.create(
                user=user,
                title="شارژ حساب کاربری",
                amount=amount,
                transaction_type='deposit'
            )

        return Response({
            "message": "کیف پول شارژ شد.",
            "balance": f"{int(user.wallet_balance):,}"
        })

class BuySubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, plan_id):
        try:
            plan = SubscriptionPlan.objects.get(id=plan_id)
        except SubscriptionPlan.DoesNotExist:
            return Response({"error": "پلن یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if user.wallet_balance < plan.price:
            return Response({"error": "موجودی کیف پول کافی نیست. لطفاً ابتدا حساب خود را شارژ کنید."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            user.wallet_balance -= plan.price
            user.save()

            WalletTransaction.objects.create(
                user=user,
                title=f"خرید {plan.title}",
                amount=plan.price,
                transaction_type='purchase'
            )

            now = timezone.now()
            duration_days = plan.months * 30
            sub, created = UserSubscription.objects.get_or_create(
                user=user,
                defaults={'expires_at': now + timedelta(days=duration_days), 'plan': plan}
            )
            if not created:
                start_date = sub.expires_at if sub.expires_at > now else now
                sub.expires_at = start_date + timedelta(days=duration_days)
                sub.plan = plan
                sub.save()

        return Response({
            "message": f"{plan.title} با موفقیت فعال شد.",
            "balance": f"{int(user.wallet_balance):,}"
        })
        
    