from django.contrib.auth import get_user_model
import logging
import json
from django.shortcuts import render, get_object_or_404,redirect
from django.core.cache import caches
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.views.generic import View

from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException

from Product.utils import dict_decoder
from .models import History,Wallet
from .forms import WalletForm


User = get_user_model()


def go_to_gateway_view(request, amount, flag):
    
    # خواندن مبلغ از هر جایی که مد نظر است
    amount = amount
    # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
    user_mobile_number = '+989112221234'  # اختیاری

    factory = bankfactories.BankFactory()
    try:
        bank = factory.auto_create()  # or factory.create(bank_models.BankType.BMI) or set identifier
        bank.set_request(request)
        bank.set_amount(amount)
        # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
        bank.set_client_callback_url(reverse('Payment:callback-gateway', kwargs={"amount": amount,"flag":flag}))
        bank.set_mobile_number(user_mobile_number)  # اختیاری

        # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
        # پرداخت برقرار کنید.
        bank_record = bank.ready()

        # هدایت کاربر به درگاه بانک
        return bank.redirect_gateway()
    except AZBankGatewaysException as e:
        logging.critical(e)
        # TODO: redirect to failed page.
        raise e


def callback_gateway_view(request, amount,flag):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
        print(bank_record)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        if flag =="wallet":
            wallet_holding = Wallet.objects.get(user__email=request.user.email).holding
            wallet_holding+=amount
            Wallet.objects.filter(user__email=request.user.email).update(holding=wallet_holding)
            return redirect("Payment:wallet")
            
        elif flag=="cart":
            redis_cache = caches['default']
            redis_client = redis_cache.client.get_client()
            paid_cart = dict_decoder(redis_client.hgetall(request.user.email))
            keys = list(paid_cart.keys())
            for key in keys:
                redis_client.hdel(request.user.email, key)
            user = get_object_or_404(User, email=request.user.email)
            history = History.objects.create(customer=user, cart=json.dumps(paid_cart), price=amount,
                                payment_method="درگاه بانکی",
                                tracking_code=tracking_code)
            ctx = {
                'history': history,
                "paid_cart": paid_cart
            }
            return render(request, "payment/order.html", context=ctx)

    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    return HttpResponse(
        "پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.")


factory = bankfactories.BankFactory()

# # غیر فعال کردن رکورد های قدیمی
bank_models.Bank.objects.update_expire_records()

# # مشخص کردن رکوردهایی که باید تعیین وضعیت شوند
for item in bank_models.Bank.objects.filter_return_from_bank():
    bank = factory.create(bank_type=item.bank_type, identifier=item.bank_choose_identifier)
    bank.verify(item.tracking_code)
    bank_record = bank_models.Bank.objects.get(tracking_code=item.tracking_code)
    if bank_record.is_success:
        logging.debug("This record is verify now.", extra={'pk': bank_record.pk})


def show_cart(request):
    return render(request, 'payment/cart.html')


def checkout(request):
    return render(request, 'payment/checkout.html')


class WalletView(View):

    def get(self,request):
        wallet_holding = Wallet.objects.get(user__email=request.user.email).holding
        form = WalletForm()
        ctx = {"holding":wallet_holding,"form":form}
        return render(request,"payment/wallet.html",ctx)

    def post(self,request):
        form = WalletForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data.get("amount")
            return redirect("Payment:gateway",amount= amount, flag="wallet")
