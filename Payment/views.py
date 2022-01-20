from django.shortcuts import render
import logging
from django.urls import reverse
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.core.cache import caches
from Product.utils import dict_decoder
from .models import History
import json
def go_to_gateway_view(request,cart_price):
     # خواندن مبلغ از هر جایی که مد نظر است
    amount = cart_price
     # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
    user_mobile_number = '+989112221234'  # اختیاری

    factory = bankfactories.BankFactory()
    try:
        bank = factory.auto_create() # or factory.create(bank_models.BankType.BMI) or set identifier
        bank.set_request(request)
        bank.set_amount(amount)
        # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
        bank.set_client_callback_url(reverse('Payment:callback-gateway',kwargs={"cart_price":cart_price}))
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



def callback_gateway_view(request,cart_price):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        redis_cache = caches['default']
        redis_client = redis_cache.client.get_client()
        paid_cart = redis_client.hgetall(request.user.email)
        redis_client.hdel(request.user.email)
        History.objects.create(customer=request.user,cart=paid_cart,price=cart_price,payment_method="درگاه بانکی",tracking_code=tracking_code)
        return render(request,"order.html",{"paid_cart":dict_decoder(paid_cart)})

    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    return HttpResponse("پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.")

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
