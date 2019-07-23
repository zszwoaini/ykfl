

from django.apps import AppConfig
import os

default_app_config = 'flapp.PrimaryBlogConfig'

VERBOSE_APP_NAME = "永康妇联后台"


def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]


class PrimaryBlogConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = VERBOSE_APP_NAME