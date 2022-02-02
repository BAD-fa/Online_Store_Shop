import uuid
import json

from django.contrib.auth import get_user_model
from django.shortcuts import render,redirect,get_object_or_404
from django.core.cache import caches
from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from decouple import config
from idpay.api import IDPayAPI


from Product.utils import dict_decoder
from .models import GateWaysModel,History
from .forms import WalletCreationForm,WalletUpdateForm


User = get_user_model()

def payment_init():
    base_url = config('BASE_URL', default='http://localhost:8000', cast=str)
    api_key = config('IDPAY_API_KEY', default='1c86dfd5-bb82-4fde-b340-0b33af756e77', cast=str)
    sandbox = config('IDPAY_SANDBOX', default=True, cast=bool)

    return IDPayAPI(api_key, base_url, sandbox)

def payment_start(request):
    if request.method == 'POST':

        order_id = uuid.uuid1()
        amount = request.POST.get('amount')

        payer = {
            'name': request.user.username,
            'phone': request.user.phone_number,
            'email': request.user.email,
            'desc': request.POST.get('desc',""),
        }


        record = GateWaysModel(order_id=order_id, amount=int(amount))
        record.save()
        call_back_url = reverse_lazy("Payment:payment_return")
        idpay_payment = payment_init()
        result = idpay_payment.payment(str(order_id), amount,call_back_url, payer)

        if 'id' in result:
            record.status = 1
            record.payment_id = result['id']
            record.save()

            return redirect(result['link'])

        else:
            txt = result['message']
    else:
        txt = "Bad Request"

    return render(request, 'error.html', {'txt': txt})


@csrf_exempt
def payment_return(request):
    if request.method == 'POST':

        pid = request.POST.get('id')
        status = request.POST.get('status')
        pidtrack = request.POST.get('track_id')
        order_id = request.POST.get('order_id')
        amount = request.POST.get('amount')
        card = request.POST.get('card_no')
        date = request.POST.get('date')

        if GateWaysModel.objects.filter(order_id=order_id, payment_id=pid, amount=amount, status=1).count() == 1:

            idpay_payment = payment_init()

            payment = GateWaysModel.objects.get(payment_id=pid, amount=amount)
            payment.status = status
            payment.date = str(date)
            payment.card_number = card
            payment.idpay_track_id = pidtrack
            payment.save()

            if str(status) == '10':
                result = idpay_payment.verify(pid, payment.order_id)

                if 'status' in result:

                    payment.status = result['status']
                    payment.bank_track_id = result['payment']['track_id']
                    payment.save()

                    redis_cache = caches['default']
                    redis_client = redis_cache.client.get_client()
                    paid_cart = dict_decoder(redis_client.hgetall(request.user.email))
                    keys = list(paid_cart.keys())
                    for key in keys:
                        redis_client.hdel(request.user.email, key)
                    user = get_object_or_404(User, email=request.user.email)
                    history = History.objects.create(customer=user, cart=json.dumps(paid_cart), price=amount,
                                             payment_method="درگاه بانکی",
                                             tracking_code=result['payment']['track_id'])
                    ctx = {
                    'history': history,
                    "paid_cart": paid_cart
                    }
                    return render(request, "payment/order.html", context=ctx)

                else:
                    txt = result['message']

            else:
                txt = "Error Code : " + str(status) + "   |   " + "Description : " + idpay_payment.get_status(status)

        else:
            txt = "Order Not Found"

    else:
        txt = "Bad Request"

    return render(request, 'error.html', {'txt': txt})


def payment_check(request, pk):

    payment = GateWaysModel.objects.get(pk=pk)

    idpay_payment = payment_init()
    result = idpay_payment.inquiry(payment.payment_id, payment.order_id)

    if 'status' in result:

        payment.status = result['status']
        payment.idpay_track_id = result['track_id']
        payment.bank_track_id = result['payment']['track_id']
        payment.card_number = result['payment']['card_no']
        payment.date = str(result['date'])
        payment.save()

    return render(request, 'error.html', {'txt': result['message']})


def show_cart(request):
    return render(request, 'payment/cart.html')


def checkout(request):
    return render(request, 'payment/checkout.html')


@method_decorator(login_required(login_url=reverse_lazy('user:login_register')), name='dispatch')
class WalletCreationView(View):

    def get(self,request):
        form = WalletCreationForm()
        ctx = {"form":form}
        return render(request,"payment/walletcreation.html",ctx)


    def post(self,request):
        form = WalletCreationForm(request.POST)
        if form.is_valid():
            wallet = form.save(commit=False)
            wallet.user = User.objects.get(email=request.user.email)
            wallet.save()
            return redirect("user:profile")
        else :
            return render(request,"payment/walletcreation.html",{"form":form})


class WalletUpdateView(View):

    def get(self,request):
        form = WalletUpdateForm()
        return render(request,"payment/wallet.html",{"form":form})

    def post(self,request):
        form = WalletUpdateForm(request.POST)
        if form.is_valid():
            wallet = User.objects.get(email=request.user.email)
            wallet.save()
            return redirect("user:profile")
        else :
            return render(request,"payment/walletcreation.html",{"form":form})

