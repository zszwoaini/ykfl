from django.conf.urls import url
from .views import *

urlpatterns = [

     url(r"^wechat$",wechat),
     # url(r"^oauth$",oauth),
     url(r"^userlogin$",UserLoginAPI.as_view()),
     url(r"^user$",UserAPI.as_view()),
     url(r'^userinfo$',UserinfoAPI.as_view()),
     url(r"^rtask$",RtaskAPI.as_view()),
     url(r'^content$',ContentAPI.as_view()),
     url(r'^join$',JoinRtaskAPI.as_view()),
     url("^share$",TaskShareaAPI.as_view()),
     url(r'^uscore$',UserScoreAPI.as_view()),
     url(r'^umoney$',MoneyChartsAPI.as_view()),
     url(r'^sign$',SignAPI.as_view()),
     url(r"^index$",IndexAPI.as_view()),
     url(r"^goodlist$",GoodListAPI.as_view()),
     url(r"^gooddetail$",GoodDetailAPI.as_view()),
     url(r'^orderdetail$',OrderDetailAPI.as_view()),
     url(r"^qrcode$",QrcodeAPI.as_view()),
     url(r"^orderpay$",OrderPayAPI.as_view()),
     url(r"^orderlist$",LogUserAPI.as_view()),
     url(r"^order$",OderAPI.as_view())



]