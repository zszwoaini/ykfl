from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r"^indexs$",IndexsAPI.as_view()),
    url(r"^active$",ActiveAPI.as_view()),
    url(r"^vote$",VoteactiveAPI.as_view()),
    url(r"^sponsor$",sponselist),
    url(r"^serch$",sponse_serch),
    url(r"^spondetail$",SponsorDetailAPI.as_view()),
    url(r"^flow$",FollwAPI.as_view()),
    url(r"^userspon$",UserSponsorAPI.as_view()),
    url(r"^infolist$",information),
    url(r"activdetail$",ActivedetailAPI.as_view()),
    url(r"^colltie$",colltie),
    url(r"^sign$",SignUpAPI.as_view()),
    url(r"sanp$",SnapAPI.as_view()),
    url(r"^votedetail$",VotedetaiAPI.as_view()),
    url(r"^searchgd$",serch),
    url(r"^themelist$",ThemelistAPI.as_view()),
    url(r"^theme$",theme_detail),
    url(r'^usertheme$',ThemeComtainAPI.as_view()),
    url(r"info$",infolist),
    url(r'^infocom$',InfoComtainAPI.as_view()),
    url(r"uvote$",UserVoteAPI.as_view()),
    url(r"^msg$",message),
    url(r"^allserch$",AllserchAPI.as_view()),
    url(r"^activcom$",ActivComentAPI.as_view()),


]