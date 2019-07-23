from django.db import models

# Create your models here.
from django.utils import timezone

from flapp import choices
from .choices import *


class User(models.Model):
    openid = models.CharField(
        max_length=100
    )
    icon = models.ImageField(
        max_length=1000,
        upload_to='png',


    )
    rname = models.CharField(
        max_length=20,
        null=False,
        verbose_name='真实姓名'
    )
    nickname = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='昵称'

    )
    phone = models.CharField(
        max_length=13,
        null=False
    )
    qq = models.CharField(
        max_length=20,
        verbose_name='QQ号'
    )
    address = models.CharField(
        max_length=100,
        null=False,
        verbose_name='地址'
    )
    sex = models.CharField(
        max_length=10,
        verbose_name='性别'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='用户'
        verbose_name_plural = verbose_name
class Balance(models.Model):
    money = models.IntegerField(

        verbose_name="积分余额",
        default=0
    )
    user = models.OneToOneField(
        User,
        verbose_name="用户"
    )
    update_time = models.DateTimeField(
        auto_now=True,
        verbose_name="用户余额更新时间"
    )

    def __str__(self):
        return self.money
    class Meta:
        verbose_name = "余额积分表"
        verbose_name_plural = verbose_name

class Rtask(models.Model):
    content = models.TextField(
        verbose_name='文章内容',
        blank=True
    )

    title = models.CharField(
        max_length= 100,
        verbose_name='文章标题'
    )
    create_time = models.DateTimeField(
       auto_now_add=True,
        verbose_name='创建时间'

   )
    complete_num = models.IntegerField(
        default=0,
        verbose_name="阅读量"
    )
    end_time = models.DateTimeField(

        verbose_name='结束时间'
    )
    score_num = models.IntegerField(
        verbose_name='阅读给与积分数',
        default=0

    )
    share_give_money = models.IntegerField(
        verbose_name="分享成功所得积分",
        default=0
    )
    task_detail = models.CharField(
        max_length=100,
        verbose_name="活动规则"
    )
    detail_url = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="详情页跳转"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="是否活跃"
    )
    icon = models.ImageField(
        upload_to='task/',
        verbose_name='图片'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "活动表"
        verbose_name_plural = verbose_name


class Sign(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='用户'

    )
    create_time = models.DateTimeField(
        auto_now=True,
        verbose_name='创建时间'

    )
    sing_count = models.IntegerField(
        verbose_name="签到总次数",
        default=0

    )
    singdays = models.IntegerField(
        verbose_name='连续签到多少天',
        default=0

    )
    def __str__(self):
        return self.user.nickname
    class Meta:
        verbose_name = '用户签到表'
        verbose_name_plural = verbose_name
class Signdetail(models.Model):
    sign_money = models.IntegerField(
        verbose_name='每次签到获取积分',
        default=0
    )
    one_money = models.IntegerField(
        verbose_name='首次签到获取积分',
        default=0
    )
    x_money = models.IntegerField(
        verbose_name='连续签到多少天后每次获取积分',
        default=0

    )
    days = models.IntegerField(
        verbose_name='连续签到天数',
        default=0
    )

    class Meta:
        verbose_name = '签到积分规则'
        verbose_name_plural = verbose_name



class UserRtaskLog(models.Model):
    user = models.ForeignKey(
        User
    )
    rtask = models.ForeignKey(
        Rtask
    )
    integral = models.IntegerField(
        verbose_name="当时所获积分"
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="参加时间"
    )
    type = models.CharField(
        max_length=10,
        choices=INTEGRAL_TYPE,
        verbose_name="奖励来源"
    )
    def __str__(self):
        return self.user.nickname

    class Meta:
        verbose_name = "用户获取积分记录表"
        verbose_name_plural = verbose_name
class GoodType(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='商品分类名'
    )
    typeimg = models.ImageField(
        upload_to='goodtype/',
        verbose_name='分类图标'
    )
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name

class Good(models.Model):
    goodimage = models.ImageField(
        upload_to='good/',
        verbose_name="商品图片"
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='商品创建时间'
    )
    term_validity = models.IntegerField(
        verbose_name='领奖商品有效期'
    )


    name = models.CharField(
        max_length=100,
        verbose_name='商品名字'

    )
    price = models.IntegerField(
        verbose_name='价格'
    )
    sales = models.IntegerField(
        verbose_name='销量',
        default=0
    )
    stock = models.IntegerField(
        verbose_name='库存'
    )
    gooddetail = models.CharField(
        max_length=200,
        verbose_name='商品详情'
    )
    type = models.ForeignKey(
        GoodType,
        verbose_name='商品分类'
    )
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name
class Order(models.Model):
    ordercard = models.CharField(
        max_length=100,
        verbose_name='下单号'
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    goods = models.ForeignKey(
        Good,
        verbose_name='商品'

    )
    user = models.ForeignKey(
        User,
        verbose_name='用户'
    )
    status = models.IntegerField(
        default=1,
        verbose_name="审核状态",
        choices=PAY_STATUS
    )
    def __str__(self):
        return self.ordercard
    class Meta:
        verbose_name = '兑换记录表'
        verbose_name_plural = verbose_name
class Payoder(models.Model):
    order = models.OneToOneField(
        Order
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    pay_status = models.IntegerField(
        default=1,
        choices=CODE_STATUS,
        verbose_name='扫码状态'
    )
    def __str__(self):
        return self.order.ordercard
    class Meta:
        verbose_name = '领取状态'
        verbose_name_plural = verbose_name

class FloorImg(models.Model):
    imags = models.ImageField(
        upload_to='floo/',
        verbose_name='轮播图'
    )
    url = models.URLField(
        verbose_name='详情链接',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

class Area(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='区域名'
    )
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '行政区域'
        verbose_name_plural = verbose_name

class Sponsor(models.Model):
    img = models.ImageField(
        upload_to='spon/',
        verbose_name='组织图徽',
        null=True,
        blank=True
    )
    name = models.CharField(
        max_length=100,
        verbose_name='组织名'
    )

    fans_num = models.IntegerField(
        verbose_name='粉丝数',
        default=0
    )
    spons_detail = models.CharField(
        max_length=200,
        verbose_name='主办方介绍'

    )

    adress = models.CharField(
        max_length=200,
        verbose_name='主办方地址'
    )
    area = models.ForeignKey(
        Area,

        verbose_name='主办方所属区域'
    )
    phone = models.CharField(
        max_length=11,
        verbose_name='主办方电话'
    )
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '组织'
        verbose_name_plural = verbose_name
class TypeActive(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='类型'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '报名活动类型'
        verbose_name_plural = verbose_name

class Votetype(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='类型'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '投票活动类型'
        verbose_name_plural = verbose_name


class Active(models.Model):
    typeactive = models.ForeignKey(
        TypeActive,
        null=True,
        blank=True,
        verbose_name='活动类型'
    )
    img = models.ImageField(
        upload_to='ac/',
        blank=True,
        null=True,
        verbose_name='活动图片'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='活动名字'
    )
    browse = models.IntegerField(
        verbose_name='浏览量',
        default=0
    )
    collection = models.IntegerField(
        verbose_name='收藏数',
        default=0
    )


    end_time = models.DateTimeField(
        default=timezone.now,
        verbose_name='活动结束时间'
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='活动创建时间'
    )
    start_time = models.DateTimeField(
        default=timezone.now,
        verbose_name='活动开始时间'
    )
    bend_time = models.DateTimeField(
        default=timezone.now,
        verbose_name='报名截止时间',

    )

    active_address = models.CharField(
        max_length=200,
        verbose_name='活动地址'
    )
    lat = models.DecimalField(
        decimal_places=15,
        max_digits=30,
        null=True,
        verbose_name="纬度"
    )
    lng = models.DecimalField(
        decimal_places=15,
        max_digits=30,
        null=True,
        verbose_name="经度"
    )
    active_detail = models.CharField(
        max_length=200,
        verbose_name='活动详情'
    )
    join_num = models.IntegerField(
        verbose_name='活动参加人数',
        default=0
    )
    contacts = models.CharField(
        max_length=20,
        verbose_name='活动联系人'
    )
    phone = models.CharField(
        max_length=11,
        verbose_name='联系人电话'
    )
    sponsor = models.ForeignKey(
        Sponsor,
        verbose_name='主办方'
    )
    active_quota = models.IntegerField(
        verbose_name='活动名额',

    )
    sanp_num = models.IntegerField(
        verbose_name='点赞数',
        default=0
    )
    is_status = models.BooleanField(
        default=False,
        verbose_name='是否置顶'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='是否活跃'
    )
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '报名活动表'
        verbose_name_plural = verbose_name
class Sanp(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='用户'
    )
    active = models.ForeignKey(
        Active,
        verbose_name='报名活动'
    )
class Comment(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='用户'
    )
    active = models.ForeignKey(
        Active,
        verbose_name='活动'
    )
    content = models.TextField(
        verbose_name='评论'
    )
    create_time = models.DateTimeField(
        auto_now_add=True
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="是否合格"
    )
    def __str__(self):
        return self.active.name
    class Meta:
        verbose_name='评论'
        verbose_name_plural = verbose_name
class Voteactive(models.Model):
    votetype = models.ForeignKey(
        Votetype,
        null=True,
        blank=True,
        verbose_name='活动类型'

    )
    img = models.ImageField(
        upload_to='ac/',
        blank=True,
        null=True,
        verbose_name='活动图片'
    )
    sponsor = models.ForeignKey(
        Sponsor
    )
    name = models.CharField(
        max_length=100,
        verbose_name='投票活动标题'
    )
    browse = models.IntegerField(
        verbose_name='浏览量',
        default=0
    )
    people_num = models.IntegerField(
        verbose_name='参与人数',
        default=0
    )

    create_time = models.DateTimeField(
        auto_now_add=True,
    )
    start_time = models.DateTimeField(
        default=timezone.now,
        verbose_name='开始时间'
    )
    end_time = models.DateTimeField(
        default=timezone.now,
        verbose_name='结束时间'
    )
    vot_rule = models.CharField(
        max_length=200,
        verbose_name='投票规则'
    )
    vote_detail = models.CharField(
        max_length=200,
        verbose_name='活动介绍'
    )
    is_status = models.BooleanField(
        default=False,
        verbose_name='是否置顶'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='是否活跃'
    )
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '投票活动'
        verbose_name_plural = verbose_name
class Votegood(models.Model):
    voteactive = models.ForeignKey(
        Voteactive
    )
    vote_num = models.IntegerField(
        verbose_name='投票数量',
        default=0
    )
    goodimage= models.ImageField(
        upload_to='votegood/',
        verbose_name='图片'
    )
    name = models.CharField(
        max_length=30,
        verbose_name='名字'
    )
    store = models.CharField(
        max_length=100,
        verbose_name='店家'
    )
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '投票商品'
        verbose_name_plural = verbose_name


class Usergood(models.Model):
    user = models.ForeignKey(
        User
    )
    voteactive = models.ForeignKey(
        Voteactive
    )
    vote_num = models.IntegerField(
        verbose_name='参与投票次数',
        default=0
    )
    create_time = models.DateTimeField(
        auto_now_add= True
    )
class Themetypes(models.Model):
    name = models.CharField(
        max_length=20,
        verbose_name='主题分类名'
    )
    images = models.ImageField(
        upload_to='theme/',
        verbose_name='主题图标'
    )
    list_image = models.ImageField(
        upload_to='theme/',
        verbose_name='主题列表首页图'
    )
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '主题分类'
        verbose_name_plural = verbose_name
class Theme(models.Model):
    theme = models.ForeignKey(
        Themetypes
    )
    theme_title = models.CharField(
        max_length=100,
        verbose_name='标题'
    )
    theme_image = models.ImageField(
        upload_to='theme/',
        verbose_name='图签'
    )
    url = models.URLField(
        verbose_name='文本链接',
        blank=True
    )
    content = models.TextField(
        verbose_name='文本内容',
        blank=True

    )
    create_time = models.DateTimeField(
        auto_now_add= True
    )
    browse = models.IntegerField(
        verbose_name='浏览量',
        default=0
    )
    def __str__(self):
        return self.theme_title
    class Meta:
        verbose_name = '主题'
        verbose_name_plural = verbose_name


class Lbimage(models.Model):
    image = models.ImageField(
        upload_to='floo/',
        verbose_name='轮播图'
    )
    url = models.URLField(
        verbose_name='详情链接',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name
class Information(models.Model):
    img = models.ImageField(
        upload_to='info/',
        blank=True,
        null=True,
        verbose_name='图片'
    )
    sponsor = models.ForeignKey(
        Sponsor
    )
    name = models.CharField(
        max_length=100,
        verbose_name='标题'
    )
    content = models.TextField(
        verbose_name='资讯内容',
        blank=True
    )
    url = models.URLField(
        verbose_name='资讯链接',
        blank=True
    )
    create_time = models.DateTimeField(
        auto_now_add=True
    )

    browse = models.IntegerField(
        verbose_name='浏览量',
        default=0
    )


    def __str__(self):
        return self.name
    class Meta:
        verbose_name='资讯'
        verbose_name_plural = verbose_name
class Messg(models.Model):
    user = models.ForeignKey(
        User
    )

    content = models.CharField(
        max_length=100,
        verbose_name='消息'
    )
    create_time = models.DateTimeField(
        auto_now_add=True
    )
    class Meta:
        verbose_name='系统消息'
        verbose_name_plural = verbose_name
class Useractive(models.Model):
    user = models.ForeignKey(
        User
    )
    active = models.ForeignKey(
        Active
    )
    is_up = models.BooleanField(
        default=False,

    )
    class Meta:
        verbose_name='我的报名活动'
        verbose_name_plural = verbose_name

class Cootile(models.Model):
    user = models.ForeignKey(
        User
    )
    active = models.ForeignKey(
        Active
    )
    coolltion_status = models.IntegerField(
        default=1,
        choices=choices.COO_STATUS,
        verbose_name='是否收藏'
    )
    class Meta:
        verbose_name='我的收藏'
        verbose_name_plural = verbose_name
class Usersponsor(models.Model):
    user = models.ForeignKey(
        User
    )
    sponsor = models.ForeignKey(
        Sponsor
    )
    class Meta:
        verbose_name = '我的组织'

class Scoredetail(models.Model):
    user =  models.ForeignKey(
        User
    )
    msg = models.CharField(
        max_length = 200,

    )
    create_time = models.DateTimeField(
        auto_now_add=True
    )
    money = models.IntegerField(
        verbose_name='获取积分数',
        default=0
    )
    class Meta:
        verbose_name='积分消息'
        verbose_name_plural = verbose_name

class Userinfo(models.Model):
    user = models.ForeignKey(
        User,
    )
    information = models.ForeignKey(
        Information
    )
    coment = models.TextField()
    class Meta:
        verbose_name = '我的资讯评论'
        verbose_name_plural = verbose_name

class Usertheme(models.Model):
    user = models.ForeignKey(
        User
    )
    theme = models.ForeignKey(
        Theme
    )
    coment = models.TextField()
    class Meta:
        verbose_name = '我的主题评论'
        verbose_name_plural = verbose_name

class Foodactive(models.Model):
    start_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='报名时间'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='报名形式'
    )
    b_know = models.TextField(
        verbose_name='报名须知'
    )
    sure = models.TextField(
        verbose_name='确定对象'
    )
    class Meta:
        verbose_name='美食活动详情'
        verbose_name_plural=verbose_name



class Foodtype(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='分类'
    )
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
class Ftypes(models.Model):
    foodtype = models.ForeignKey(
        Foodtype,
        verbose_name='分类'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='美食'
    )
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '美食'
        verbose_name_plural = verbose_name
class UserEnroll(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='用户'
    )
    store = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    store_area = models.ForeignKey(
        Area,
        null=True,
        blank=True

    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    name = models.CharField(
        max_length=30,
        verbose_name='法人代表名'
    )
    parea = models.ForeignKey(
        Area,
        null=True,
        blank=True,
        related_name='parea',
        verbose_name='法人所属区域'

    )
    ucard = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='身份证'
    )
    phone = models.CharField(
        max_length=11,
        unique=True,
        verbose_name='手机号'
    )
    foodtype = models.ForeignKey(
        Foodtype,
        related_name='types',
        verbose_name='类别'

    )
    type = models.CharField(
        max_length=20,
        verbose_name='美食'
    )
    foodtypeone = models.ForeignKey(
        Foodtype,
        null=True,
        blank=True,
        verbose_name='类别'
    )
    typeone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='美食'

    )
    prices = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='单价'
    )
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '报名表'
        verbose_name_plural = verbose_name


class Uicon(models.Model):
    img = models.ImageField(
        upload_to='up/',
        verbose_name='证件'

    )
    userenroll = models.ForeignKey(
        UserEnroll
    )







