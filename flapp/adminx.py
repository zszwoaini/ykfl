import datetime

import xadmin
from .models import *
from xadmin import views

# class GlobalSetting(object):
#     """
#     全局配置
#     """
#     # global_search_models = [Template, Category, Article]
#     # global_models_icon = {
#     #     models.Template: "fa fa-cubes",
#     #     models.Category: "fa fa-folder",
#     #     models.Article: "fa fa-files-o",
#     # }
#     menu_style = 'default'  # 'default'  'accordion'
# xadmin.sites.register(views.CommAdminView,GlobalSetting)

class BaseSetting(object):
    enable_themes = True  # 开启主题选择
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "管理系统"  # 设置左上角title名字
    site_footer = "永康妇联"  # 设置底部关于版权信息
    # 设置菜单缩放
    menu_style = "default"  # 左侧导航条修改可折叠



xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)

class RtaskAdmin(object):
    list_display = ['content','title','end_time','score_num','share_give_money',
                     'task_detail','detail_url','icon']
    list_per_page = 20
    search_fields = ['title']
    def get_readonly_fields(self):
        """  重新定义此函数，限制普通用户所能修改的字段  """
        if self.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields

    readonly_fields = ('complete_num',)
xadmin.site.register(Rtask,RtaskAdmin)
class SigndetailAdmin(object):
    list_display = ['sign_money','one_money','x_money','days']
xadmin.site.register(Signdetail,SigndetailAdmin)
class GoodTypeAdmin(object):
    list_display = ['name','typeimg']
xadmin.site.register(GoodType,GoodTypeAdmin)
class GoodAdmin(object):
    list_display = ['goodimage','term_validity','name','price','stock','gooddetail','type']
    search_fields =['name','type__name']
    list_filter = ['name','type__name']
    list_per_page = 20

    def get_readonly_fields(self):
        """  重新定义此函数，限制普通用户所能修改的字段  """
        if self.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields

    readonly_fields = ('sales',)
xadmin.site.register(Good,GoodAdmin)
class FloorImgAdmin(object):
    list_display = ['id','imags']
xadmin.site.register(FloorImg,FloorImgAdmin)
class AreaAdmin(object):
    list_display = ['id','name']
xadmin.site.register(Area,AreaAdmin)
class SponsorAdmin(object):
    list_display = ['name','spons_detail','adress','area','phone']
    search_fields = ['name','area']
    list_per_page = 20
    list_filter = ['name', 'area']
    def get_readonly_fields(self):
        """  重新定义此函数，限制普通用户所能修改的字段  """
        if self.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields

    readonly_fields = ('fans_num','active_num')
xadmin.site.register(Sponsor,SponsorAdmin)
class TypeActiveAdmin(object):
    list_display = ['id','name']
xadmin.site.register(TypeActive,TypeActiveAdmin)
class VotetypeAdmin(object):
    list_display = ['id','name']
xadmin.site.register(Votetype,VotetypeAdmin)
class ActiveAdmin(object):
    list_display = ['name','active_address','active_detail',
                    'contacts','phone','sponsor','active_quota','is_active']
    search_fields = ['name','sponsor']
    list_filter = ['name','sponsor']
    # def save_models(self):
    #     """
    #     保存
    #     :return:
    #     """
    #     super().save_models()
    #
    #     time = self.new_obj.end_time.strftime('%Y/%m/%d')
    #     times = datetime.datetime.strptime(time, '%Y/%m/%d')
    #     print(times)
    #     now = datetime.datetime.now().strftime('%Y/%m/%d')
    #     nows = datetime.datetime.strptime(now, '%Y/%m/%d')
    #     print(nows)
    #     if times == nows:
    #         self.new_obj.is_active = False
    #         self.new_obj.save()



    def get_readonly_fields(self):
        """  重新定义此函数，限制普通用户所能修改的字段  """
        if self.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields

    readonly_fields = ('browse','collection','join_num')

xadmin.site.register(Active,ActiveAdmin)
class VoteactiveAdmin(object):
    list_display = ['sponsor','name','vote_detail','vot_rule']
    search_fields = ['sponsor','name']
    list_filter = ['sponsor','name']
xadmin.site.register(Voteactive,VoteactiveAdmin)
class VotegoodAdmin(object):
    list_display = ['voteactive','goodimage','name','store',]
    list_filter = ['voteactive','name','store']
    search_fields = ['name', 'store']
xadmin.site.register(Votegood,VotegoodAdmin)
class ThemetypesAdmin(object):
    list_display = ['name','images','list_image']
xadmin.site.register(Themetypes,ThemetypesAdmin)
class ThemeAdmin(object):
    list_display = ['theme','theme_title','theme_image','url','content',]
    search_fields = ['theme', 'theme_title']
    list_filter = ['theme', 'theme_title']
    list_per_page = 20
xadmin.site.register(Theme,ThemeAdmin)
class LbimageAdmin(object):
    list_display = ['image']
xadmin.site.register(Lbimage,LbimageAdmin)
class InformationAdmin(object):
    list_display = ['sponsor','name','content','url']
    search_fields = ['sponsor', 'name']
    list_filter = ['sponsor', 'name']
    list_per_page = 20

xadmin.site.register(Information,InformationAdmin)
class FoodactiveAdmin(object):
    list_display = ['start_time','title','b_know','sure',]
xadmin.site.register(Foodactive,FoodactiveAdmin)


