from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm
from .models import Payment_Account, Payment_order


@login_required
def index(request):
    return render(request, "home.html")


def login_view(request):
    if request.method == 'POST':

        user_phone = request.POST['user_phone']
        password = request.POST['password']
        user = authenticate(request, user_phone=user_phone, password=password)
        if user is not None:
            login(request, user)
            print("登陆")
            return redirect('home')
        else:
            return render(request, 'login.html', {"error": "手机号或者密码错误"})
    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        data = request.POST.dict()
        check_username = Payment_Account.objects.filter(username=data["username"])
        if check_username.exists():
            err = "手机或邮箱或身份证已存在"
            return render(request, 'register.html', {"error": err})
        check_unique = Payment_Account.objects.filter(
            Q(user_phone=data["user_phone"]) | Q(user_email=data["user_email"]) | Q(
                user_id_number=data["user_id_number"]))
        if check_unique.exists():
            err = "手机或邮箱或身份证已存在"
            return render(request, 'register.html', {"error": err})
        del data["csrfmiddlewaretoken"]
        user = Payment_Account.objects.create_user(**data)
        login(request, user)
        return redirect("home")

    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def deposit(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        user = request.user

        # 更新当前余额
        Payment_Account.objects.filter(user_id=user.user_id).update(balance=F('balance') + amount)
        Payment_order.objects.create(user_id=user, invoice_description="存款", Price=amount, status=0, type="存款")
        return redirect('deposit')

    return render(request, 'deposit.html')


@login_required
def transfer(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        name = request.POST.get('name')
        amount = int(request.POST.get('amount'))
        remark = request.POST.get('remark')
        sender = request.user

        # 查找接收者对象并验证手机号码和姓名是否匹配
        receiver = get_object_or_404(Payment_Account, user_phone=phone, name=name)

        if sender.balance < amount:  # 验证余额是否充足
            return render(request, 'transfer.html', {'error': '余额不足'})

        # 更新发送者余额和接收者余额
        Payment_Account.objects.filter(user_id=sender.user_id).update(balance=sender.balance - amount)
        Payment_Account.objects.filter(user_id=receiver.user_id).update(balance=receiver.balance + amount)
        Payment_order.objects.create(user_id=sender, invoice_description=remark, Price=amount, status=0, type="转出")
        Payment_order.objects.create(user_id=receiver, invoice_description=remark, Price=amount, status=0, type="转入")
        return redirect('transfer')

    return render(request, 'transfer.html')


@login_required
def payment_order_list(request):
    orders = Payment_order.objects.all().order_by('-invoice_time')
    search = request.GET.get('search')
    if search:
        orders = orders.filter(invoice_description__icontains=search)
    sort = request.GET.get('sort')
    if sort == 'oldest':
        orders = orders.order_by('invoice_time')
    elif sort == 'latest':
        orders = orders.order_by('-invoice_time')
    paginator = Paginator(orders, 12)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    return render(request, 'order.html', {'orders': page, 'search': search, 'sort': sort})


def pay(request):
    try:
        order_id = int(request.GET.get('order_id'))
        amount = float(request.GET.get('amount'))
    except Exception as r:
        return render(request, 'pay.html', {'error': "请传入订单ID和金额"})
    payment_url = 'http://127.0.0.1:8000/payments/?id={}&amount={}'.format(order_id, amount)
    return render(request, 'pay.html', {'payment_url': payment_url, 'amount': amount})


def payments(request):
    return HttpResponse("支付成功")
