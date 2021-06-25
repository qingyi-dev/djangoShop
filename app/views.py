import json

from django.contrib import auth
# from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from app.forms import UserForm
from app.models import User, Goods, Cart


def hello(request):
    return HttpResponse('hello world!')


# /register 用户注册页面
def register(request):
    if request.method == 'GET':
        # 显示页面
        return render(request, 'register.html')

    else:
        # 检验数据
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        repwd = request.POST.get('repassword')
        if not all([username, pwd, repwd]):
            # 有数据为空
            return render(request, 'register.html', {'msg': '数据输入不完整'})
        else:
            if pwd != repwd:
                return render(request, 'register.html', {'msg': '两次密码输入不一致'})

        # 判断用户名是否已存在
        if User.objects.filter(name=username).first():
            return render(request, 'register.html', {'msg': '用户名已存在'})
        # 一切无误，保存数据
        user = User()
        user.name = username
        user.password = pwd
        user.save()
        return render(request, 'login.html')


# 使用model form校验注册
def register1(request):
    if request.method == "GET":
        form = UserForm()
        return render(request, 'register1.html', {'form': form})
    else:
        form = UserForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'register1.html', {'form': form})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        # 验证数据
        # 从表单中拿数据
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        repwd = request.POST.get('repassword')
        if not all([username, pwd, repwd]):
            # 有数据为空
            return render(request, 'login.html', {'msg': '数据输入不完整'})
        if pwd != repwd:
            return render(request, 'login.html', {'msg': '两次密码输入不一致'})
        user = User.objects.filter(name=username).first()
        # 判断账户
        if not user:
            return render(request, 'login.html', {'msg': '账户不存在'})
        elif user.password != pwd:
            return render(request, 'login.html', {'msg': '密码错误'})
        # 存入缓存
        request.session['uid'] = user.id
        # return render(request, 'index.html', {'user': user})
        return redirect('index')


# 商品首页
def index(request):
    goods = Goods.objects.all()
    uid = request.session.get('uid')
    carts = Cart.objects.filter(user_id=uid).all()
    if not uid:
        return render(request, 'index.html')
    user = User.objects.get(id=uid)
    # print(type(goods))
    paginator = Paginator(goods, 1)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    # {'goods': goods, 'user': user, 'uid': uid}
    return render(request, 'index.html', locals())


# 用户登出
def logout(request):
    # uid = request.session['uid']
    # user = User.objects.filter('uid').first()
    request.session.clear()
    auth.logout(request)
    return redirect('index')


# 用户收藏模块
def userlove(request):
    gid = request.GET.get('gid', 1)  # 接受商品ID
    uid = request.session.get('uid')
    print(gid)
    if not uid:
        return render(request, 'login.html', {'msg': '用户尚未登录，请登录后在进行操作！'})
    user = User.objects.get(id=uid)
    good = Goods.objects.get(pk=gid)
    good.user_loved = user.id
    good.save()
    data = {'status': 'ok', 'msg': 'success'}
    return HttpResponse(json.dumps(data))
    # return HttpResponse(json.dumps(data), content_type='application/json')


# 购物车模块
def cart(request):
    # 若是用户未登录，跳转到登录页面
    if not request.session.get('uid'):
        render(request, 'login.html', {'msg': '请先登录！'})
    gid = request.GET.get('gid', 1)
    print(gid)  # None  <class 'NoneType'>
    # print(type(gid))  # str
    gid = int(gid)
    uid = request.session.get('uid')
    user = User.objects.filter(id=uid).first()
    good = Goods.objects.filter(id=gid).first()
    carts = Cart.objects.all()
    cart_good_list = []
    for cart2 in carts:
        cart_good_list.append(cart2.goods.id)
    if good.id in cart_good_list:
        cart3 = Cart.objects.filter(goods_id=gid).first()
        # print(cart3.count)
        cart3.count += 1
        # print(cart3.count)
        cart3.save()
    else:
        a = Cart.objects.create(user_id=user.id, goods_id=good.id)
        # print(a)
    return JsonResponse({'status': 'ok', 'count': cart3.count})


# 购物车详情 右上角
def cart1(request):
    goods = Goods.objects.all()
    uid = request.session.get('uid')
    # 显示该用户的购物车
    carts = Cart.objects.filter(user_id=uid)
    if not uid:
        return render(request, 'index.html')
    user = User.objects.get(id=uid)
    # print(type(goods))

    return render(request, 'cart.html', locals())


# 商品数量减少
def countsub(request):
    # cid = request.GET.get('cid')
    # print(cid)
    cid = request.GET.get('gid')
    print(cid)
    cart = Cart.objects.filter(id=cid).first()
    cart.count -= 1
    cart.save()
    return JsonResponse({'status': 'ok', 'count': cart.count})


# 商品数量增加
def countadd(request):
    # cid = request.GET.get('cid')
    # print(cid)
    cid = request.GET.get('gid')
    print(cid)
    cart = Cart.objects.filter(id=cid).first()
    cart.count += 1
    cart.save()
    return JsonResponse({'status': 'ok', 'count': cart.count, 'cid': cid})  # bug这里总价未改变
