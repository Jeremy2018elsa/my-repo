import json

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *

# Create your views here.
def index_views(request):
    return render(request,'index.html')

# /login 对应的视图
def login_views(request):
    url = '/'
    if request.method == 'GET':
        #获取session
        # id = request.session.get('uid',0)
        # uphone = request.session.get('uphone',0)

        if 'uid' in request.session and 'uphone' in request.session:
        #session中有值
            return redirect(url)
        else:
            #session中没有值
            #查询cookie，是否曾经记住密码，cookie中是否有uid和uphone
            if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
                #cookie中有登录信息
                #从cookie中取出数据保存进session
                uid = request.COOKIES['uid']
                uphone = request.COOKIES['uphone']
                request.session['uid'] = uid
                request.session['uid'] = uphone
                return redirect(url)
            else:
                #cookie中没有登录信息
                #去往登录页面
                form = LoginForm()
                return render(request,'login.html',locals())
    else:
        #post流程
        form = LoginForm(request.POST)

        if form.is_valid():
            uphone = form.cleaned_data['uphone']

            upwd = form.cleaned_data['upwd']
            userList = Users.objects.filter(uphone=uphone,upwd=upwd)
            if userList:
                id = Users.objects.filter(uphone=uphone)[0].id
                request.session['uid'] = id
                request.session['uphone'] = uphone

                resp = redirect(url)
                if 'isSaved' in request.POST:
                    #保持登录信息cookie

                    resp.set_cookie('uid',id,60*60*24)
                    resp.set_cookie('uphone',uphone,60*60*24)
                return resp

            else:
                form = LoginForm()
                errMsg = '手机号或密码不正确'
                return render(request, 'login.html', locals())


# /register 对应的视图
def register_views(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        uphone = request.POST['uphone']
        upwd = request.POST['upwd']
        uname = request.POST['uname']
        uemail = request.POST['uemail']
        Users.objects.create(uphone=uphone,upwd=upwd,uname=uname,uemail=uemail)
        id = Users.objects.filter(uphone=uphone)[0].id
        request.session['uid'] = id
        request.session['uphone'] = uphone

        return redirect('/')

def checkphone_views(request):
    phone = request.GET['phone']

    phoneList = Users.objects.filter(uphone=phone)
    if phoneList:
        return HttpResponse('手机号码已存在')
    else:
        return HttpResponse('手机号码可以使用')

def checkLogin_views(request):
    if 'uid' in request.session and 'uphone' in request.session:
        #用户处于登录状态
        id = request.session['uid']
        user = Users.objects.filter(id=id)[0]
        jsonStr = json.dumps(user.to_dict())
        dic = {
            "status": '1',
            "user": jsonStr
        }

    else:
        #用户没有登录
        #检查cookie中是否有用户登录信息
        if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
            #取出用户登录信息，存入session
            uid = request.COOKIES['uid']
            uphone = request.COOKIES['uphone']
            request.session['uid'] = uid
            request.session['uphone'] = uphone
            user = Users.objects.filter(id=uid)[0]
            jsonStr = json.dumps(user.to_dict())
            dic = {
                "status": '1',
                "user": jsonStr
            }
        else:
            dic = {
                "status":'0',
                "text":'用户尚未登录'
            }
    return HttpResponse(json.dumps(dic))

def logout_views(request):
    #获取请求源地址，如果没有则返回主页
    url = request.META.get('HTTP_REFERER','/')

    resp = redirect(url)
    if 'uid' in request.session and 'uphone' in request.session:
        del request.session['uid']
        del request.session['uphone']
    if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
        resp.delete_cookie('uid')
        resp.delete_cookie('uphone')
    return resp

def loadgoods_views(request):
    #查询所有的商品类别
    goodsTypeList = GoodsType.objects.all()
    data = []
    for goodsType in goodsTypeList:
        # 根据商品类别查询商品
        # goodsList = Goods.objects.filter(goodsType=goodsType.id)
        # if len(goodsList) > 10:
        #     goodsList = goodsList[:10]

        goodsList = goodsType.goods_set.order_by("-price")[:10]
        jsonGoodsType = json.dumps(goodsType.to_dict())

        jsonGoods = serializers.serialize('json',goodsList)
        dic = {
            "type":jsonGoodsType,
            "goods":jsonGoods,
        }
        data.append(dic)

    return HttpResponse(json.dumps(data))

#添加或更新数量至购物车
def addcart_views(request):
    users_id = request.session['uid']
    goods_id = request.GET['goods_id']
    ccount = request.GET.get('ccount',1)

    #查看购物车中是否有相同用户购买过相同商品，
    # 如果有的话则更新数量，没有的话则新增数据
    cart_list = CartInfo.objects.filter(users_id=users_id,goods_id=goods_id)
    if cart_list:
        #已经有商品，更新购买数量
        cartinfo = cart_list[0]
        cartinfo.ccount = cartinfo.ccount + int(ccount)
        cartinfo.save()
        dic = {
            "status":'1',
            "text":'更新数量成功',
        }
        return HttpResponse(json.dumps(dic))
    else:
        #创建商品，并保存进数据库
        cartinfo = CartInfo(users_id=users_id,goods_id=goods_id,ccount=int(ccount))
        cartinfo.save()
        dic = {
            'status':'1',
            'text':'添加至购物车成功'
        }
        return HttpResponse(json.dumps(dic))

def cartcount_views(request):
    user_id = request.session['uid']
    cart_list = CartInfo.objects.filter(users_id=user_id)
    totle_count = 0
    for li in cart_list:
        totle_count += li.ccount
    return HttpResponse(totle_count)