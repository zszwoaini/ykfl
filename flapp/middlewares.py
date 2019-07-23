__author__ = '进'
__date__ = '2019-07-08'

from django.middleware.common import MiddlewareMixin


class CORSMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # 添加响应头

        # 允许你的域名来获取我的数据
        response['Access-Control-Allow-Origin'] = "*"

        # 允许你携带Content-Type请求头
        response['Access-Control-Allow-Headers'] = "Content-Type,token"

        # 允许你发送DELETE,PUT
        response['Access-Control-Allow-Methods'] = "DELETE,PUT,POST"
        return response
