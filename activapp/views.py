import datetime
import json

from django.core.cache import caches
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import render
from django.utils import timezone
# Create your views here.
from django.views.generic import View
from django.forms import model_to_dict

from flapp.models import *
from django.http import HttpResponse, JsonResponse, QueryDict

user_cache = caches['user']
PAGE_NUM = 10

#首页

class IndexsAPI( View):
    def get(self,req):
        image =[]
        themetypes = []
        actives = []
        vote = []
        sponsors = []
        flimage = Lbimage.objects.all()
        for i in flimage:
            temp = {}
            temp['image'] = i.image.url
            image.append(temp)
        theme_types = Themetypes.objects.all()
        for i in theme_types:
            temp = model_to_dict(i)
            temp['images'] = i.images.url
            temp['list_image'] = i.list_image.url
            themetypes.append(temp)
        active = Active.objects.filter(is_status=True,is_active=True).order_by('-create_time')[0:5]
        for i in active:
            temp = model_to_dict(i)
            temp['img'] = i.img.url
            temp['typeactive'] = i.typeactive.name
            temp['sponsor'] = i.sponsor.name
            temp['bend_time'] = i.bend_time.strftime('%Y/%m/%d')
            temp['end_time'] = i.end_time.strftime('%Y/%m/%d')
            temp['start_time'] = i.start_time.strftime('%Y/%m/%d')
            actives.append(temp)

        vote_active = Voteactive.objects.filter(is_status=True,is_active=True).order_by('-create_time')[0:5]
        for i in vote_active:
            temp = {}
            temp['id'] = i.id
            temp['votetype'] = i.votetype.name
            temp['is_status'] = i.is_status
            temp['sponsor'] = i.sponsor.name
            temp['img'] = i.img.url
            temp['title'] = i.name
            temp['start_time'] = i.start_time.strftime('%Y/%m/%d')
            temp['end_time'] = i.end_time.strftime('%Y/%m/%d')
            vote.append(temp)

        sponsor = Sponsor.objects.order_by('fans_num')[0:5]
        for i in sponsor:
            votes = i.voteactive_set.all()
            active = i.active_set.all()
            lists = []
            for v in votes:
                lists.append(v)
            for a in active:
                lists.append(a)
            temp=model_to_dict(i)
            temp['active_num'] =len(lists)
            temp['img'] = i.img.url
            print(temp)
            sponsors.append(temp)
        information = Information.objects.order_by('-create_time')[0:10]
        informations = []
        for i in information:
            temp = model_to_dict(i)
            temp['sponsor'] = i.sponsor.name
            temp['img'] = i.img.url
            temp['create_time'] = i.create_time.strftime('%Y/%m/%d')
            informations.append(temp)

        data = {
            'flimage':image,
            'theme_types':themetypes,
            'active':actives,
            'vote_active':vote,
            'sponsor':sponsors,
            'information':informations
        }
        return JsonResponse(data)
'''
#报名活动列表
'''
class ActiveAPI(View):
    def get(self,req):
        page_num = int(req.GET.get("page", 1))
        active_list = Active.objects.filter(is_active=True).order_by('-create_time')
        print(active_list)
        actives = []
        for i in active_list:
            time = i.end_time.strftime('%Y/%m/%d')
            times = datetime.datetime.strptime(time, '%Y/%m/%d')
            print(times)
            now = datetime.datetime.now().strftime('%Y/%m/%d')
            nows = datetime.datetime.strptime(now, '%Y/%m/%d')
            print(nows)
            if times == nows:
                i.is_active = False
                i.save()
            temp = model_to_dict(i)
            temp['img'] = i.img.url
            temp['typeactive'] = i.typeactive.name
            temp['sponsor'] = i.sponsor.name
            temp['create_time'] = i.create_time.strftime('%Y/%m/%d')
            temp['bend_time'] = i.bend_time.strftime('%Y/%m/%d')
            temp['end_time'] = i.end_time.strftime('%Y/%m/%d')
            temp['start_time'] = i.start_time.strftime('%Y/%m/%d')
            actives.append(temp)
        pageinator = Paginator(actives, PAGE_NUM)
        try:
            page = pageinator.page(page_num)
            pages = page.object_list
        except:
            data = {
                "code": 0,
                "data": []
            }
            return JsonResponse(data)

        area = Area.objects.all()
        type = TypeActive.objects.all()
        types = []
        sponselist = []
        for i in area:
            temp = {}
            temp['id'] = i.id
            temp['name'] = i.name
            sponselist.append(temp)
        for i in type:
            temp = model_to_dict(i)
            types.append(temp)
        return JsonResponse({'code': 0, 'data':{
            'area':sponselist,
            'type':types,
            'activ':pages
        } })

    def post(self,req):
        page_num = int(req.POST.get("page",1))
        now = datetime.datetime.now()
        actives = []
        area = req.POST.get('area')
        print(area)
        type = req.POST.get('type')
        print(type)
        time = req.POST.get('time')
        print(time)
        heat = req.POST.get('heat')
        q_all = Q()

        #区域刷选
        if area:
            q_area = Q()
            q_area.connector = Q.OR

            q_area.children.append(('sponsor__area_id',area))
            q_all.add(q_area,Q.AND)
            print(q_all)
        #类别刷选
        if type:
            q_type = Q()
            q_type.connector = Q.OR
            q_type.children.append(('typeactive_id',type))
            q_all.add(q_type,Q.AND)
        if time == 'today':
            q_time = Q()
            q_time.connector = Q.OR
            q_time.children.append(('create_time__day',now.day))
            q_all.add(q_time,Q.AND)
            print(q_time)
        elif time == 'week':
            now_time = now.strftime('%Y-%m-%d')
            time = datetime.datetime.strptime(now_time, '%Y-%m-%d')
            times = time + datetime.timedelta(days=1)
            day_num = time.isoweekday()
            week_day = (time - datetime.timedelta(days=day_num))
            q_time = Q()
            q_time.connector = Q.OR
            q_time.children.append(('create_time__range', (week_day, times)))
            q_all.add(q_time, Q.AND)
        elif time == 'month':
            q_time = Q()
            q_time.connector = Q.OR
            q_time.children.append(('create_time__month', now.month))
            q_all.add(q_time, Q.AND)
        elif time == 'year':
            q_time = Q()
            q_time.connector = Q.OR
            q_time.children.append(('create_time__year', now.year))
            q_all.add(q_time, Q.AND)
        active_list = Active.objects.filter(q_all,is_active=True).order_by('%s'%(heat))
        #打印原生SQL语句
        print(active_list.query)
        for i in active_list:
            temp = model_to_dict(i)
            temp['img'] = i.img.url
            temp['typeactive'] = i.typeactive.name
            temp['sponsor'] = i.sponsor.name
            temp['bend_time'] = i.bend_time.strftime('%Y/%m/%d')
            temp['end_time'] = i.end_time.strftime('%Y/%m/%d')
            temp['start_time'] = i.start_time.strftime('%Y/%m/%d')
            actives.append(temp)
        pageinator = Paginator(actives, PAGE_NUM)
        try:
            page = pageinator.page(page_num)
            pages = page.object_list
        except:
            data = {
                "code": 0,
                "data": []
            }
            return JsonResponse(data)
        datas = {

            'active_list': pages
        }
        return JsonResponse(datas)
'''
投票活动列表
'''
class VoteactiveAPI(View):
    def get(self,req):
        page_num = int(req.GET.get("page", 1))
        active_list = Voteactive.objects.filter(is_active=True).order_by('-create_time')
        print(active_list)
        actives = []
        for i in active_list:
            time = i.end_time.strftime('%Y/%m/%d')
            times = datetime.datetime.strptime(time, '%Y/%m/%d')
            print(times)
            now = datetime.datetime.now().strftime('%Y/%m/%d')
            nows = datetime.datetime.strptime(now, '%Y/%m/%d')
            print(nows)
            if times == nows:
                i.is_active = False
                i.save()
            temp = model_to_dict(i)
            temp['votetype'] = i.votetype.name
            temp['img'] = i.img.url
            temp['sponsor'] = i.sponsor.name
            temp['title'] = i.name
            temp['start_time'] = i.start_time.strftime('%Y-%m-%d')
            temp['end_time'] = i.end_time.strftime('%Y-%m-%d')
            actives.append(temp)
        pageinator = Paginator(actives, PAGE_NUM)
        try:
            page = pageinator.page(page_num)
            pages = page.object_list
        except:
            data = {
                "code": 0,
                "data": []
            }
            return JsonResponse(data)

        area = Area.objects.all()
        type = Votetype.objects.all()
        types = []
        sponselist = []
        for i in area:
            temp = {}
            temp['id'] = i.id
            temp['name'] = i.name
            sponselist.append(temp)
        for i in type:
            temp = model_to_dict(i)
            types.append(temp)
        return JsonResponse({'code': 0, 'data':{
            'area':sponselist,
            'type':types,
            'activ':pages
        } })

    def post(self,req):
        page_num = int(req.POST.get("page",1))
        now = datetime.datetime.now()
        actives = []
        area = req.POST.get('area')
        print(area)
        type = req.POST.get('type')
        print(type)
        time = req.POST.get('time')
        print(time)
        heat = req.POST.get('heat')
        q_all = Q()

        #区域刷选
        if area:
            q_area = Q()
            q_area.connector = Q.OR
            q_area.children.append(('sponsor__area_id',area))
            q_all.add(q_area,Q.AND)
            print(q_all)
        #类别刷选
        if type:
            q_type = Q()
            q_type.connector = Q.OR
            q_type.children.append(('votetype_id',int(type)))
            q_all.add(q_type,Q.AND)
        if time == 'tonday':
            q_time = Q()
            q_time.connector = Q.OR
            q_time.children.append(('create_time__day',now.day))
            q_all.add(q_time, Q.AND)
            print(q_time)
        elif time == 'week':
            now_time = now.strftime('%Y-%m-%d')
            time = datetime.datetime.strptime(now_time, '%Y-%m-%d')
            times = time + datetime.timedelta(days=1)
            day_num = time.isoweekday()
            week_day = (time - datetime.timedelta(days=day_num))
            q_time = Q()
            q_time.connector = Q.OR
            q_time.children.append(('create_time__range', (week_day, times)))
            q_all.add(q_time, Q.AND)
        elif time == 'month':
            q_time = Q()
            q_time.connector = Q.OR
            q_time.children.append(('create_time__month', now.month))
            q_all.add(q_time, Q.AND)
        elif time == 'year':
            q_time = Q()
            q_time.connector = Q.OR
            q_time.children.append(('create_time__year', now.year))
            q_all.add(q_time, Q.AND)
        active_list = Voteactive.objects.filter(q_all).order_by('%s'%(heat))
        print(active_list.query)
        for i in active_list:
            temp = model_to_dict(i)
            temp['votetype'] = i.votetype.name
            temp['img'] = i.img.url
            temp['sponsor'] = i.sponsor.name
            temp['title'] = i.name
            temp['start_time'] = i.start_time.strftime('%Y-%m-%d')
            temp['end_time'] = i.end_time.strftime('%Y-%m-%d')
            actives.append(temp)
        pageinator = Paginator(actives, PAGE_NUM)
        try:
            page = pageinator.page(page_num)
            pages = page.object_list
        except:
            data = {
                "code": 0,
                "data": []
            }
            return JsonResponse(data)
        datas = {

            'active_list': pages
        }
        return JsonResponse(datas)
'''
组织列表
'''
def sponselist(req):
    sponse = Sponsor.objects.all()
    datas = []
    for i in sponse:
        temp = model_to_dict(i)
        list = []
        active = i.active_set.all()
        vote = i.voteactive_set.all()
        for v in vote:
            list.append(v)
        for a in active:
            list.append(a)
        temp['id'] = i.id
        temp['img'] = i.img.url
        temp['name'] = i.name
        temp['fans_num'] = i.fans_num
        temp['adress'] = i.adress
        temp['num'] = len(list)
        datas.append(temp)
        data = {
            'code':0,
            'data':datas
        }
    return JsonResponse(data)
'''
组织搜索
'''
def sponse_serch(req):
    kw = req.GET.get('kw')
    sponse= Sponsor.objects.filter(name__contains=kw)
    datas = []
    for i in sponse:
        temp = model_to_dict(i)
        list = []
        active = i.active_set.all()
        vote = i.voteactive_set.all()
        for v in vote:
            list.append(v)
        for a in active:
            list.append(a)
        temp['img'] = i.img.url
        temp['name'] = i.name
        temp['fans_num'] = i.fans_num
        temp['adress'] = i.adress
        temp['num'] = len(list)
        datas.append(temp)
        data = {
            'code': 0,
            'data': datas
        }

    return JsonResponse(data)
#组织详情
class SponsorDetailAPI(View):
    def get(self,req):
        actives = []
        vote = []
        informations = []
        id = req.GET.get('s_id')
        sponsor = Sponsor.objects.get(pk=int(id))
        information = sponsor.information_set.all().order_by('-create_time')
        for i in information:
            temp = model_to_dict(i)
            temp['sponsor'] = i.sponsor.name
            temp['img'] = i.img.url
            informations.append(temp)
        active = sponsor.active_set.all().order_by('-create_time')
        for i in active:
            temp = model_to_dict(i)
            temp['img'] = i.img.url
            temp['sponsor'] = i.sponsor.name
            temp['bend_time'] = i.bend_time.strftime('%Y/%m/%d')
            temp['end_time'] = i.end_time.strftime('%Y/%m/%d')
            temp['start_time'] = i.start_time.strftime('%Y/%m/%d')
            actives.append(temp)
        a_num = active.count()
        vote_active = sponsor.voteactive_set.all().order_by('-create_time')

        for i in vote_active:
            temp = model_to_dict(i)
            temp['votetype'] = i.votetype.name
            temp['img'] = i.img.url
            temp['sponsor'] = i.sponsor.name
            temp['title'] = i.name
            temp['start_time'] = i.start_time.strftime('%Y-%m-%d')
            temp['end_time'] = i.end_time.strftime('%Y-%m-%d')
            vote.append(temp)

        v_num = vote_active.count()
        s_num = a_num + v_num
        temp = {}
        temp['img'] = sponsor.img.url
        temp['name'] = sponsor.name
        temp['fans_num'] = sponsor.fans_num
        temp['adress'] = sponsor.adress
        temp['phone'] = sponsor.phone
        temp['s_num'] = s_num
        temp['spons_detail'] = sponsor.spons_detail
        data = {
            'code':0,
            'data':{
                'sponsor':temp,
                'active':actives,
                'vote_active':vote,
                'information':informations
            }
        }
        return  JsonResponse(data)
'''
组织关注
'''
class FollwAPI(View):
    def post(self,req):
        user = User.objects.get(pk=int(user_cache.get(
            req.POST.get("token")
        )))

        id = req.POST.get('s_id')
        status = json.loads(req.POST.get('is_up'))
        sponsor = Sponsor.objects.get(pk=int(id))
        response = {"state": True, 'msg': ''}
        usersponsor = Usersponsor.objects.filter(user_id=user.id,sponsor_id=int(id))
        if  not usersponsor:
            if status:
                Usersponsor.objects.create(
                    user_id=user    .id,
                    sponsor_id=sponsor.id
                )
                sponsor.fans_num += 1
                sponsor.save()
                Messg.objects.create(
                    user=user,
                    content='关注 %s ' % (sponsor.name)
                )
                response['msg'] = '取消关注'
            else:
                response['state'] = False
                response['msg'] = '关注'
        else:
            if status:
                usersponsor.delete()
                sponsor.fans_num -= 1
                sponsor.save()
                Messg.objects.create(
                    user=user,
                    content='取消关注 %s ' % (sponsor.name)
                )
                response['msg'] = '关注'
            else:
                response['state'] = False
                response['msg'] = '取消关注'
        return JsonResponse(response)


'''
我的组织
'''
class UserSponsorAPI(View):
    def get(self,req):
        user = User.objects.get(pk=int(user_cache.get(
            req.GET.get("token")
        )))
        sponse = Usersponsor.objects.filter(user_id=user.id)
        data = []
        for i in sponse:
            temp = {}
            temp['img'] = i.sponsor.img.url
            temp['id'] = i.sponsor.id
            temp['name'] = i.sponsor.name
            temp['fans_num'] = i.sponsor.fans_num
            temp['adress'] = i.sponsor.adress
            data.append(temp)
        return JsonResponse({'code':0,'data':data})


'''
报名活动详情
'''
class ActivedetailAPI(View):
    def get(self,req):
        id = req.GET.get('a_id')
        try:
            active = Active.objects.get(pk=int(id))
        except:
            data = {
                'code':2,
                'data':'活动不存在'
            }
            return  JsonResponse(data)
        active.browse += 1
        active.save()
        votes = active.sponsor.voteactive_set.all().count()
        actives = active.sponsor.active_set.all().count()
        num = votes + actives
        temp = model_to_dict(active)
        temp['img'] = active.img.url
        temp['sponsor'] = active.sponsor.name
        temp['fans_num'] = active.sponsor.fans_num
        temp['num'] = num
        temp['bend_time'] = active.bend_time.strftime('%Y/%m/%d')
        temp['end_time'] = active.end_time.strftime('%Y/%m/%d')
        temp['start_time'] = active.start_time.strftime('%Y/%m/%d')
        comment = active.comment_set.filter(is_active=True)
        text = []
        for i in comment:
            tem = {}
            tem['time'] = i.create_time.strftime('%Y/%m/%d')
            tem['content'] = i.content
            tem['name'] = i.user.nickname
            tem['icon'] = str(i.user.icon)
            text.append(tem)

        data = {
            'code':0,
            'data':{
                'active':temp,
                'comment':text
            }
        }
        return JsonResponse(data)
"""
报名活动收藏
"""
def colltie(req):
    user = User.objects.get(pk=int(user_cache.get(
        req.POST.get("token")
    )))
    id = req.POST.get('a_id')
    status = json.loads(req.POST.get('is_up'))
    active = Active.objects.get(pk=int(id))
    cootile = Cootile.objects.filter(user=user, active=active)
    response = {"state": True, 'msg': ''}
    if cootile:
        if status:
            cootile.delete()
            active.collection -= 1
            active.save()
            Messg.objects.create(
                user=user,
                content='取消收藏 %s ' % (active.name)
            )
            response['msg'] = '收藏'
        else:
            response['state'] = False
            response['msg'] = '取消收藏'
    else:
        if status:
            Cootile.objects.create(
                user=user,
                active=active
            )
            active.collection += 1
            active.save()
            Messg.objects.create(
                user=user,
                content='收藏 %s 成功 ' % (active.name)
            )
            response['msg'] = '取消收藏'
        else:
            response['state'] = False
            response['msg'] = '收藏'
    return JsonResponse(response)


"""
活动报名
"""
class SignUpAPI(View):
    def post(self,req):
        user = User.objects.get(pk=int(user_cache.get(
            req.POST.get("token")
        )))
        id = req.POST.get('a_id')
        status= req.POST.get('is_up')
        active = Active.objects.get(pk=int(id))
        useractive = Useractive.objects.filter(user_id=user.id,active_id=int(id))
        response = {"state": True, 'msg': ''}
        if active.active_quota == 0:
            if  not useractive:
                if status:
                    Useractive.objects.create(
                        user_id=user.id,
                        active_id=active.id
                    )
                    active.join_num += 1
                    active.save()
                    Messg.objects.create(
                        user=user,
                        content='报名 %s 成功 ' % (active.name)
                    )
                    response['msg'] = '取消报名'
                else:
                    response['state'] = False
                    response['msg'] = '立即报名'
            else:
                if status:
                    useractive.delete()
                    active.join_num -= 1
                    active.save()
                    Messg.objects.create(
                        user=user,
                        content='取消报名 %s ' % (active.name)
                    )
                    response['msg'] = '立即报名'
                else:
                    response['state'] = False
                    response['msg'] = '取消报名'
        else:
            if active.join_num == active.active_quota:
                response['state'] = '名额已满'
                response['msg'] = '对不起，请下次早点报名'
            else:
                if not useractive:
                    if status:
                        Useractive.objects.create(
                            user_id=user.id,
                            active_id=active.id
                        )
                        active.join_num += 1
                        active.save()
                        Messg.objects.create(
                            user=user,
                            content='报名 %s 成功 ' % (active.name)
                        )
                        response['msg'] = '取消报名'
                    else:
                        response['state'] = False
                        response['msg'] = '立即报名'
                else:
                    if status:
                        useractive.delete()
                        active.join_num -= 1
                        active.save()
                        Messg.objects.create(
                            user=user,
                            content='取消报名 %s ' % (active.name)
                        )
                        response['msg'] = '立即报名'
                    else:
                        response['state'] = False
                        response['msg'] = '取消报名'
        return  JsonResponse(response)
"""
报名活动点赞
"""
class SnapAPI(View):
    def post(self,req):
        user = User.objects.get(pk=int(user_cache.get(
            req.POST.get("token")
        )))
        id = req.POST.get('a_id')
        active = Active.objects.get(pk=int(id))
        sanp = Sanp.objects.filter(user=user,active=active)
        if  sanp:
            data = {'code':0,'data':'你已点赞'}
            return JsonResponse(data)
        Sanp.objects.create(
            user=user,
            active=active
        )
        active.sanp_num += 1
        active.save()
        data = {'code':1,'data':'点赞成功'}
        return JsonResponse(data)




"""
投票活动详情
"""
class VotedetaiAPI(View):
    def get(self,req):
        v_id = req.GET.get('id')
        v_active = Voteactive.objects.get(pk=int(v_id))
        tem = model_to_dict(v_active)
        tem['img'] = v_active.img.url
        tem['sponsor'] = v_active.sponsor.name
        tem['votetype'] = v_active.votetype.name
        tem['end_time'] = v_active.end_time.strftime('%Y/%m/%d')
        tem['start_time'] = v_active.start_time.strftime('%Y/%m/%d')
        v_active.browse += 1
        v_active.save()
        list = []
        tex = []
        goods = v_active.votegood_set.all()
        for i in goods:
            tex.append(i.vote_num)
            temp = {}
            temp['id'] = i.id
            temp['name'] = i.name
            temp['goodimage'] = i.goodimage.url
            temp['store'] = i.store
            temp['vote_num'] = i.vote_num
            list.append(temp)
        good_num = goods.count()
        data = {
            'code':0,
            'data':{
                'active':tem,
                'goods':list,
                'good_num':good_num,
                'vote_nums':sum(tex)
            }
        }
        return JsonResponse(data)
'''
用户投票
'''
class UserVoteAPI(View):
    def post(self,req):
        user = User.objects.get(pk=int(user_cache.get(
            req.POST.get("token")
        )))
        id = req.POST.get('v_id')
        test = req.POST.getlist('id')
        status = json.loads(req.POST.get('is_up'))
        v_active = Voteactive.objects.get(pk=int(id))
        response = {'status':True,'msg':''}
        list = []
        for i in test:
            list.append(int(i))
        if len(list) > 2:
            data = {
                'code':2,
                'data':'选中商品数量超限'
            }
            return JsonResponse(data)
        up = Usergood.objects.filter(user=user,voteactive=v_active)
        if up:
            now = timezone.now().strftime("%Y-%m-%d")
            t = datetime.datetime.strptime(now, '%Y-%m-%d')
            nows = up[0].create_time.strftime("%Y-%m-%d")
            p = datetime.datetime.strptime(nows, '%Y-%m-%d')
            if (t - p).days == 0:
                response['status'] = False
                response['msg'] = '已投过票'
            else:
                if status:
                    up[0].create_time = timezone.now()
                    up[0].vote_num += 1
                    up[0].save()
                    for i in test:
                        good = Votegood.objects.get(pk=int(i))
                        good.vote_num += 1
                        good.save()
                    v_active.people_num += 1
                    v_active.save()
                    Messg.objects.create(
                        user=user,
                        content='投票 %s 成功 ' % (v_active.title)
                    )
                    response['msg'] = '已投票成功'
                else:
                    response['status'] = False
                    response['msg'] = '立即投票'
        else:
            if status:
                Usergood.objects.create(
                    user=user,
                    voteactive=v_active,
                    vote_num=1
                )
                v_active.people_num += 1
                v_active.save()
                Messg.objects.create(
                    user=user,
                    content='投票 %s 成功 ' % (v_active.title)
                )
                for i in test:
                    good = Votegood.objects.get(pk=int(i))
                    good.vote_num += 1
                    good.save()
                response['msg'] = '已投票'
            else:
                response['status'] = False
                response['msg'] = '立即投票'
        return JsonResponse(response)
'''
投票商品搜索
'''
def serch(req):
    kw = req.POST.get('kw')
    goods = Votegood.objects.filter(name__contains=kw)
    data = []
    for i in goods:
        temp = {}
        temp['id'] = i.id
        temp['goodimage'] = i.goodimage.url
        temp['vote_num'] = i.vote_num
        temp['store'] = i.store
        temp['name'] = i.name
        data.append(temp)
    return JsonResponse({'code': 0, 'data': data})
'''
主题列表
'''
class ThemelistAPI(View):
    def get(self,req):
        id = req.GET.get('t_id')
        print(id)
        theme_type = Themetypes.objects.get(pk=int(id))
        themes = theme_type.theme_set.all()
        data = []
        for i  in themes:
            temp = {}
            temp['id'] = i.id
            temp['theme_title'] = i.theme_title
            temp['theme_image'] = i.theme_image.url
            temp['list_image'] = theme_type.list_image.url
            data.append(temp)
        return JsonResponse({'code': 0, 'data': data})
'''
主题详情
'''
def theme_detail(req):
    id = req.GET.get('id')
    theme = Theme.objects.get(pk=int(id))
    theme.browse += 1
    theme.save()
    temp = {}
    temp['content'] = theme.content
    temp['url'] = theme.url
    temp['theme_title'] = theme.theme_title
    temp['theme_image'] = theme.theme_image.url
    temp['browse'] = theme.browse
    temp['create_time'] = theme.create_time
    return JsonResponse({'code':0,'data':temp})
"""
主题评论
"""
class ThemeComtainAPI(View):
    def post(self,req):
        user = User.objects.get(pk=int(user_cache.get(
                req.POST.get("token")
            )))
        id = req.POST.get('s_id')
        theme = Theme.objects.get(pk=int(id))
        com = req.POST.get('com','')
        print(com)
        if com is '':
            data = {
                'code':0,
                'data':'你没有填写内容'
            }
            return JsonResponse(data)
        Usertheme.objects.create(
            user=user,
            theme=theme,
            coment=com
        )
        return JsonResponse({'code':0,'data':'评论成功'})
"""
新闻详情
"""
def information(req):
    id = req.GET.get('id')
    i = Information.objects.get(pk=int(id))
    i.browse += 1
    i.save()
    temp = {}
    temp['browse'] = i.browse
    temp['name'] = i.name
    temp['create_time'] = i.create_time.strftime('%Y-%m-%d')
    temp['sponsor'] = i.sponsor.name
    temp['url'] = i.url
    temp['content'] = i.content

    data = {
        'code':0,
        'data':temp
    }

    return JsonResponse(data)
"""
新闻列表
"""
def infolist(req):
    info = Information.objects.all().order_by('-create_time')
    obj = []
    for i in info:
        temp = {}
        temp['id'] = i.id
        temp['img'] = i.img.url
        temp['name'] = i.name
        temp['create_time'] = i.create_time.strftime("%Y-%m-%d")
        temp['sponsor'] = i.sponsor.name
        obj.append(temp)
    return JsonResponse({'code':0,'data':obj})
"""
新闻评论
"""
class InfoComtainAPI(View):
    def post(self,req):
        user = User.objects.get(pk=int(user_cache.get(
                req.POST.get("token")
            )))
        id = req.POST.get('s_id')
        info = Information.objects.get(pk=int(id))
        com = req.POST.get('com','')
        print(com)
        if com is '':
            data = {
                'code':0,
                'data':'你没有填写内容'
            }
            return JsonResponse(data)
        Userinfo.objects.create(
            user=user,
            information=info,
            coment=com
        )
        return JsonResponse({'code':0,'data':'评论成功'})
"""
系统消息
"""
def message(req):
    user = User.objects.get(pk=int(user_cache.get(
            req.GET.get("token")
        )))
    msg = Messg.objects.filter(user_id=user.id).order_by('-create_time')
    data =[]
    for i in msg:
        temp ={}
        temp['id'] = i.id
        temp['content'] = i.content
        temp['create_time'] = i.create_time.strftime("%Y%m%d%H%S")
        data.append(temp)
    return  JsonResponse({'code':0,'data':data})
'''
首页搜索框
'''
class AllserchAPI(View):
    def get(self,req):
        area = Area.objects.all()
        datas = []
        for i in area:
            temp = model_to_dict(i)
            datas.append(temp)
        return JsonResponse({'code':0,'data':datas})
    def post(self,req):
        id = req .POST.get('id')
        kw = req.POST.get('kw')
        con = Q()
        if id:
            q_area = Q()
            q_area.connector = Q.OR
            q_area.children.append(('sponsor__area_id',id))
            con.add(q_area,Q.AND)
        if kw :
            q_kw = Q()
            q_kw.connector = Q.OR
            q_kw.children.append(('name__contains',kw))
            con.add(q_kw,Q.AND)
        infos = []
        info = Information.objects.filter(con).order_by('-create_time')
        for i in info:
            temp = {}
            temp['id'] = i.id
            temp['img'] = i.img.url
            temp['title'] = i.name
            temp['create_time'] = i.create_time.strftime("%Y-%m-%d")
            temp['sponsor'] = i.sponsor.name
            infos.append(temp)

        active = Active.objects.filter(con).order_by('-create_time')
        actives = []
        for i in active:
            tem = model_to_dict(i)
            tem['img'] = i.img.url
            tem['typeactive'] = i.typeactive.name
            tem['sponsor'] = i.sponsor.name
            tem['bend_time'] = i.bend_time.strftime('%Y/%m/%d')
            tem['end_time'] = i.end_time.strftime('%Y/%m/%d')
            tem['start_time'] = i.start_time.strftime('%Y/%m/%d')
            actives.append(tem)

        vote = Voteactive.objects.filter(con).order_by('-create_time')
        votes = []
        for i in vote:
            te = model_to_dict(i)
            te['votetype'] = i.votetype.name
            te['img'] = i.img.url
            te['sponsor'] = i.sponsor.name
            te['title'] = i.name
            te['start_time'] = i.start_time.strftime('%Y-%m-%d')
            te['end_time'] = i.end_time.strftime('%Y-%m-%d')
            votes.append(te)
        sponsors = []
        sponsor = Sponsor.objects.filter(con).order_by('-fans_num')
        for i in sponsor:
            vot = i.voteactive_set.all()
            activ = i.active_set.all()
            lists = []
            for v in vot:
                lists.append(v)
            for a in activ:
                lists.append(a)
            temp = model_to_dict(i)
            temp['active_num'] = len(lists)
            temp['img'] = i.img.url
            print(temp)
            sponsors.append(temp)
        data = {
            'info':infos,
            'active':actives,
            'vote':votes,
            'sponsor':sponsors
        }
        return JsonResponse(data)
"""
报名活动评论
"""
class ActivComentAPI(View):
    def post(self,req):
        user = User.objects.get(pk=int(user_cache.get(
            req.POST.get("token")
        )))
        id = req.POST.get('id')
        active = Active.objects.get(pk=int(id))
        com = req.POST.get('com', '')
        print(com)
        if com is '':
            data = {
                'code': 0,
                'data': '你没有填写内容'
            }
            return JsonResponse(data)
        Comment.objects.create(
            user=user,
            active=active,
            content=com
        )
        return JsonResponse({'code': 0, 'data': '评论成功'})
# class FoodenlorAPI(View):
#     def post(self,req):
#         user = User.objects.get(pk=int(user_cache.get(
#             req.POST.get("token")
#         )))
#         store = req.POST.get('store')
#         sarea = req.POST.get('sarea')
#         person = req.POST.get('person')
#         parea = req.POST.get('parea')
#         icard = req.POST.get('icard')
#         phone = req.POST.get('phone')
#         type = req.post.get('type')
#         food = req.POST.get('food')
#         price = req.POST.get('price')
#         types = req.post.get('types')
#         foods = req.POST.get('foods')
#         prices = req.POST.get('prices')
#         icon = req.FILES.getlist('img')
#         uenroll = UserEnroll.objects.create(
#             store=store,
#             store_area_id=int(sarea),
#             name=person,
#             parea_id=int(parea),
#             ucard=icard,
#             phone=phone,
#             foodtype_id=int(type),
#             price=price,
#             foodtypeone_id=int(types),
#             type=food,
#             typeone=foods,
#             prices=prices,
#             img=icon
#
#         )





























