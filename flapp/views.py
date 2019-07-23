import datetime
import json
import urllib
import uuid
from django.db import connection


import requests
from io import BytesIO

import qrcode
import hashlib

from django.conf import settings
from django.core.cache import caches
from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import View

from .models import *

user_cache = caches['user']

# Create your views her

def wechat(request):
    signature = str(request.GET.get("signature", None))
    timestamp = str(request.GET.get("timestamp", None))
    nonce = str(request.GET.get('nonce', None))
    echostr = str(request.GET.get('echostr', None))
    token = settings.TOKEN
    # 将要排序加密的参数放在一个数组中
    hashlist = [token, timestamp, nonce]
    hashlist.sort()
    print(hashlist)
    temp_str = ''.join(hashlist)
    hashstr = hashlib.sha1(temp_str.encode(encoding='UTF-8')).hexdigest()
    print(hashstr)

    if hashstr == signature:
        return HttpResponse(echostr)
    else:
        return HttpResponse("error")

# def oauth(request):
#      redirect_uri = "http://ykfl.lizhouyun.cn/flus/userlogin"
#      redirect_uri = urllib.request.quote(redirect_uri)
#      url="https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect"\
#          %(settings.APPID,redirect_uri)
#      return redirect(url)


class UserLoginAPI(View):
    def get(self,req):
        code = req.GET.get('code')
        print(code)
        if not code:
            return HttpResponse('not find code')

        url =  'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code'\
               %(settings.APPID,settings.APPSECRET,code)
        print(url)
        #获取url数据
        response = urllib.request.urlopen(url)
        #读取数据内容，返回json数据
        res_str = response.read()
        #转换字典
        res_dict = json.loads(res_str)
        print(res_dict)
        access_token = res_dict.get('access_token')
        open_id =  res_dict.get('openid')
        if not access_token or not open_id:
            return None
        #请求微信服务器，获取用资料
        urls = 'https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN'\
              %(access_token,open_id)
        responses= urllib.request.urlopen(urls)
        user_json = responses.read()
        user_dict = json.loads(user_json)
        if 'openid'in user_dict:
            openid = user_dict.get('openid')
            user = User.objects.get_or_create(openid=openid)[0]
            token = uuid.uuid4().hex
            user_cache.set(token,user.id,settings.TIME_LONG)
            user.nickname = user_dict['nickname']
            user.icon = user_dict['headimgurl']
            user.sex = user_dict['sex']
            user.save()
            print(token)
            return HttpResponse(json.dumps({'code': 0, 'data': {'token': token}}),
                                content_type='application/json')
        else:
            return HttpResponse(json.dumps({'code': 1, 'msg': '授权失败，请回到首页'}),
                                content_type='application/json')
class UserAPI(View):
    def get(self,req):
        user = User.objects.get(pk=int(user_cache.get(
            req.GET.get("token")
        )))
        icon = str(user.icon)
        name = user.nickname
        return JsonResponse({'code':0,'name':name,'icon':icon})

class UserinfoAPI(View):
    def post(self,req):
        user = User.objects.get(pk=int(user_cache.get(
            req.POST.get("token")
        )))
        par = req.POST
        user.rname = par.get('name')
        user.nickname = par.get('nickname')
        user.phone = par.get('phone')
        user.qq = par.get('qq')
        user.sex = par.getlist('sex')[0]
        user.address = par.get('address')
        user.save()
        return HttpResponse('修改完成')



#阅读任务表
class RtaskAPI(View):
    def get(self,req):
        rtask = Rtask.objects.filter(is_active=True)
        data = []
        for i in rtask:
            temp={}
            temp['id'] = i.id
            temp['title']=i.title
            temp['score_num']=i.score_num
            temp['share_give_money']=i.share_give_money
            temp['end_time'] = i.end_time
            temp['detail_url'] = i.detail_url
            temp['content'] = i.content
            temp['icon'] = i.icon.url
            data.append(temp)


        res = {
            'code':0,
            'data':data

        }
        return JsonResponse(res)
class ContentAPI(View):
    def get(self,req):
        id = req.GET.get('t_id')
        content = Rtask.objects.get(pk=int(id))
        content.complete_num += 1
        content.save()
        temp = {}
        temp['complete_num'] = content.complete_num
        temp['content'] = content.content
        temp['detail_url'] = content.detail_url
        temp['title'] = content.title
        data = {
            'code':0,
            'data':temp
        }
        return JsonResponse(data)

class JoinRtaskAPI(View):
    def post(self,req):
        user = User.objects.get(pk=user_cache.get(
            req.POST.get("token")
        ))
        id = req.POST.get('id')
        rtask = Rtask.objects.get(pk=int(id))
        if UserRtaskLog.objects.filter(user_id=user.id,rtask_id=int(id),type='join').exists():
            data = {
                "code": 2,
                "data": "任务已完成"
            }
            return JsonResponse(data)
        log = UserRtaskLog.objects.create(
            rtask_id=id,
            user_id=user.id,
            integral=rtask.score_num,
            type='join'

        )
        user_blance = Balance.objects.get_or_create(user_id=user.id)[0]
        user_blance.money += rtask.score_num
        user_blance.save()
        Scoredetail.objects.create(
            user=user,
            msg='阅读 "%s" 任务完成，获取%s积分' % (rtask.title,rtask.score_num),
            money=rtask.score_num
        )
        data = {
            "code": 0,
            "data": "领取成功"
        }
        return JsonResponse(data)

class TaskShareaAPI(View):
    def post(self,req):
        user = User.objects.get(pk=int(user_cache.get(
            req.POST.get("token")
        )))
        id = req.POST.get('id')
        rtask = Rtask.objects.get(pk=int(id))
        if UserRtaskLog.objects.filter(user_id=user.id, rtask_id=int(id),type='share').exists():
            data = {
                "code": 2,
                "data": "任务已完成"
            }
            return JsonResponse(data)
        log = UserRtaskLog.objects.create(
            rtask_id=id,
            user_id=user.id,
            integral=rtask.share_give_money,
            type='share'

        )
        user_blance = Balance.objects.get_or_create(user_id=user.id)[0]
        user_blance.money += rtask.share_give_money
        user_blance.save()
        Scoredetail.objects.create(
            user=user,
            msg='分享 "%s" 任务完成，获取%s积分' % (rtask.title, rtask.score_num),
            money=rtask.share_give_money

        )
        data = {
            "code": 0,
            "data": "领取成功"
        }
        return JsonResponse(data)


#用户参与获得积分记录消息
class UserScoreAPI(View):
    def get(self,req):
        user = User.objects.get(pk=user_cache.get(
            req.GET.get("token")
        ))
        mg = Scoredetail.objects.filter(user=user).order_by('-create_time')
        list = []
        for i in mg:
            temp = {}
            temp['msg'] = i.msg
            temp['create_time'] = i.create_time
            temp['money'] = i.money
            list.append(temp)
        return JsonResponse({'code':0,'data':list})




#ji积分排行榜
class MoneyChartsAPI(View):
    def get(self,req):
        user = User.objects.get(pk=int(user_cache.get(
            req.GET.get("token")
        )))
        now_time = datetime.datetime.now().strftime('%Y-%m-%d')
        time = datetime.datetime.strptime(now_time,'%Y-%m-%d')
        times = time + datetime.timedelta(days=1)
        day_num = time.isoweekday()
        week_day = (time - datetime.timedelta(days=day_num))
        all_datas = Scoredetail.objects.filter(user=user,create_time__range=(week_day, times))
        print(all_datas)
        list = []
        for i in all_datas:
            if int(i.money) > 0:
              list.append(int(i.money))
        ublance = Balance.objects.filter(user=user)[0].money
        blance  = Balance.objects.all().order_by('money')[0:101]
        blan_data = []
        for i in blance:
            tep = {}
            tep['nickname'] = i.user.nickname
            tep['money'] = i.money
            blan_data.append(tep)
        res = {
            'code':0,
            'data':{
                'money':sum(list),
                'umoney':ublance,
                'user':blan_data

            }
        }
        return JsonResponse (res)
class SignAPI(View):
    def post(self,req):
        user = User.objects.get(pk=int(user_cache.get(
            req.POST.get("token")
        )))
        sgindetail = Signdetail.objects.all()[0]
        status = json.loads(req.POST.get('is_sign'))
        obj = Sign.objects.filter(user_id=user.id )
        response = {'statue':True,'msg':''}
        if not obj:
            if status:
                sign = Sign.objects.create(
                    user=user,
                    sing_count=1,
                    singdays=1

                )
                user_blance = Balance.objects.get_or_create(user_id=user.id)[0]
                user_blance.money += sgindetail.one_money
                user_blance.save()
                Scoredetail.objects.create(
                    user=user,
                    msg='首签成功，获取%s积分'%(sgindetail.one_money),
                    money=sgindetail.one_money
                )
                response['msg'] = '首签成功'

            else:
                response['statue'] = False
                response['msg'] = '你还没有签到'
        else:
            if status:
                now = timezone.now().strftime("%Y-%m-%d")
                t = datetime.datetime.strptime(now, '%Y-%m-%d')
                print(t)
                nows = obj[0].create_time.strftime("%Y-%m-%d")
                p = datetime.datetime.strptime(nows, '%Y-%m-%d')
                print(p)
                print((t-p).days)
                if (t-p).days == 0:
                    response['msg'] = '今天已经签过'
                    response['statue'] = False
                else:
                    if (t - p).days == 1:
                        obj[0].singdays += 1
                        obj[0].sing_count += 1
                        obj[0].save()
                        if obj[0].singdays >= sgindetail.days:
                            user_blance = Balance.objects.get_or_create(user_id=user.id)[0]
                            user_blance.money += sgindetail.x_money
                            user_blance.save()
                            Scoredetail.objects.create(
                                user=user,
                                msg='连续签到超过%s天，每日获取%s积分' %(sgindetail.days,sgindetail.one_money),
                                money=sgindetail.one_money
                            )
                        else:
                            user_blance = Balance.objects.get_or_create(user_id=user.id)[0]
                            user_blance.money += sgindetail.sign_money
                            user_blance.save()
                            Scoredetail.objects.create(
                                user=user,
                                msg='每日签到，获取%s积分' % ( sgindetail.sign_money),
                                money=sgindetail.sign_money

                            )

                        response['msg'] = '签到成功'
                    else:
                        obj[0].singdays = 1
                        obj[0].sing_count += 1
                        obj[0].save()
                        user_blance = Balance.objects.get_or_create(user_id=user.id)[0]
                        user_blance.money += sgindetail.sign_money
                        user_blance.save()
                        Scoredetail.objects.create(
                            user=user,
                            msg='每日签到，获取%s积分' % (sgindetail.sign_money),
                            money=sgindetail.sign_money
                        )
                        response['msg'] = '连续签到中断'
            else:
                response['statue'] = False
                response['msg'] = '你没有签到'
        return  JsonResponse(response)



class IndexAPI(View):
    def get(self,req):
        img = []
        list = []
        types=[]
        floor = FloorImg.objects.all()
        for i in floor:
            test = {}
            test['imags'] = i.imags.url
            img.append(test)
        type = GoodType.objects.all()
        for i in type:
            obj = {}
            obj['id'] = i.id
            obj['typeimg'] = i.typeimg.url
            obj['name'] = i.name
            types.append(obj)

        goods = Good.objects.order_by('sales')[0:4]

        for i in goods:
            temp = {}
            temp['id'] = i.id
            temp['goodimage'] = i.goodimage.url
            temp['name'] = i.name
            temp['price'] = i.price
            list.append(temp)

        content = {
            'type':types,
            'goods':list,
            'img':img

        }
        return  JsonResponse(content)
class GoodListAPI(View):
    def get(self,req):
        type_id = req.GET.get('id')
        types = GoodType.objects.get(pk=int(type_id))
        good = types.good_set.order_by('-create_time')
        good_list = []
        for i in good:
            temp = model_to_dict(i)
            temp['name'] = i.name
            temp['goodimage'] = i.goodimage.url
            temp['price'] = i.price
            good_list.append(temp)
        data = {
            'code':0,
            'data':good_list
        }
        return JsonResponse(data)
class GoodDetailAPI(View):
    def post(self,req):
        user = User.objects.get(pk=int(user_cache.get(
            req.POST.get("token")
        )))
        good_id = req.POST.get('id')
        good = Good.objects.get(pk=int(good_id))
        temps = model_to_dict(good)
        temps['goodimage'] = good.goodimage.url
        order = Order.objects.filter(goods_id=good.id)
        order_list = []
        # if order:
        for i in order:
            temp = model_to_dict(i)
            temp['create_time'] = i.create_time.strftime("%Y-%m-%d %H:%M:%S")
            temp['user'] = i.user.nickname
            temp['icon'] = str(i.user.icon)
            order_list.append(temp)
        data = {
            'code':0,
            'data':{
                'order':order_list,
                'good':temps,
            }
        }
        return  JsonResponse (data)



#订单记录表
class LogUserAPI(View):
    def get(self,req):
        user = User.objects.get(pk=user_cache.get(
            req.GET.get("token")
        ))
        order = Order.objects.filter(user_id=user.id)
        log_data = []
        for i in order:
            temp = model_to_dict(i)
            temp['goodimage'] = i.goods.goodimage.url
            temp['name'] = i.goods.name
            temp['status'] = i.status
            temp['price'] = i.goods.price
            temp['ordercard'] = i.ordercard
            log_data.append(temp)
        data = {
            'code':0,
            'data':log_data
        }
        return JsonResponse (data)
class OderAPI(View):
    def post(self,req):
        user = User.objects.get(pk=int(user_cache.get(
            req.POST.get("token")
        )))
        g_id = req.POST.get('g_id')
        good = Good.objects.get(pk=int(g_id))
        blance = Balance.objects.get_or_create(user_id=user.id)[0]
        if (good.stock < 1) or (blance.money < good.price):
            data = {
                'code':2,
                'data':'库存或余额不足，无法购买'
            }
            return  JsonResponse(data)
        if Order.objects.filter(user_id=user.id,goods_id=int(g_id)).exists():
            data = {
                'code':1,
                'data':'你已参与过，请去领奖'
            }
            return JsonResponse(data)


        ordercard = datetime.datetime.now().strftime("%Y%m%d%H%S") + str(user.id)
        order = Order.objects.create(
            user_id=user.id,
            goods_id=good.id,
            ordercard=ordercard,
            status=1


        )
        good.stock -= 1
        good.sales += 1
        good.save()
        blance.money -= good.price
        blance.save()
        Scoredetail.objects.create(
            user=user,
            msg='添加%s商品成功，消耗-%s' %(good.name,good.price),
            money=-(good.price)
        )
        data = {
            'code':0,
            'data':'下单成功'
        }
        return  JsonResponse(data)
#订单详情表

class OrderDetailAPI(View):
    def get(self,req):
        user = User.objects.get(pk=int(user_cache.get(
            req.GET.get("token")
        )))
        o_id = req.GET.get('id',None)
        order = Order.objects.filter(user_id=user.id,id=o_id)
        datas = []
        for i  in order:
            temp = model_to_dict(i)
            temp['goodimage'] = i.goods.goodimage.url
            temp['name'] = i.goods.name
            temp['price'] = i.goods.price
            temp['num'] = 1
            datas.append(temp)
        return  JsonResponse({'code':0,'data':datas})
#制作商品二维码
class QrcodeAPI(View):
    def post(self,req):
        user = User.objects.get(pk=int(user_cache.get(
            req.POST.get("token")
        )))
        o_id = req.POST.get('id')
        order = Order.objects.filter(user=user,id=o_id)[0]

        now = timezone.now().strftime("%Y-%m-%d")
        t = datetime.datetime.strptime(now, '%Y-%m-%d')
        nows = order.create_time.strftime("%Y-%m-%d")
        p = datetime.datetime.strptime(nows, '%Y-%m-%d')
        print((t-p).days)
        if (t - p).days > order.goods.term_validity:
            order.status = 3
            order.goods.stock += 1
            order.goods.save()
            order.save()
            data = {
                'code': 0,
                'data': '超过商品领奖有效期，不能领奖'
            }
            return JsonResponse(data)
        url = 'http://ykfl.lizhouyun.cn/flus/orderdetail?id='+str(order.id)
        code_make = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H,
        )
        code_make.add_data(url)
        code_make.make(fit=True)
        img = code_make.make_image()
        buf = BytesIO()
        img.save(buf)
        return  HttpResponse(buf.getvalue(),content_type='image/png')
class OrderPayAPI(View):
    def get(self,req):
        user = User.objects.get(pk=int(user_cache.get(
            req.GET.get("token")
        )))
        s_id = req.GET.get('o_id')
        order = Order.objects.filter(user_id=user.id,id=s_id)[0]

        if Payoder.objects.filter(order_id=int(s_id),pay_status=1).exists():
            data = {
                'code':2,
                'data':'奖品已发放'
            }
            return  JsonResponse(data)
        let = Payoder.objects.create(
            order=order,
            pay_status=1
        )
        order.status = 2
        order.save()
        Scoredetail.objects.create(
            user=user,
            msg='%s商品领取成功' % (order.goods.name),

        )


        return HttpResponse('领取成功')

def token(requset):
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
        settings.APPID, settings.APPSECRET)
    result = urllib.request.urlopen(url).read()
    access_token = json.loads(result).get('access_token')
    return access_token


def createMenu(request):
    url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % Config.access_token
    data = {
        "button": [
            {
                "name": "积分系统",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "每天签到",
                        "url": ""
                    },
                    {
                        "type": "view",
                        "name": "阅读分享",
                        "url": ""
                    },
                    {
                        "type": "view",
                        "name": "积分商城",
                        "url": "http://m.qzone.com/infocenter?g_f=#2378686916/mine"
                    },

                    ]
            },
            {
                "name": "云上妇联",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "找活动",
                        "url": ""
                    },
                    {
                        "type": "view",
                        "name": "找组织",
                        "url": ""
                    },
                    {
                        "type": "view",
                        "name": "新闻资讯",
                        "url": ""
                    },
                    {
                        "type": "view",
                        "name": "首页",
                        "url": "http://m.guju.com.cn/projects"
                    }]
            },


        ]
    }
    # data = json.loads(data)
    # data = urllib.urlencode(data)
    req = urllib.request.Request(url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('encoding', 'utf-8')
    response = urllib.request.urlopen(req, json.dumps(data, ensure_ascii=False))
    result = response.read()
    return HttpResponse(result)


































            














