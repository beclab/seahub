from rest_framework.response import Response
from rest_framework.views import APIView
import json
import logging

from seahub.base.accounts import User
from seahub.profile.models import Profile
from seaserv import seafile_api, ccnet_api
from seahub.base.templatetags.seahub_tags import email2nickname, email2contact_email
from seahub.views import create_default_library
# from seahub.auth.utils import list_all_users


logger = logging.getLogger(__name__)


def list_all_users():
    total_count = ccnet_api.count_emailusers('DB') + \
                      ccnet_api.count_inactive_emailusers('DB')

    users = ccnet_api.get_emailusers('DB', 0, total_count)

    data = {}
    for user in users:
        profile = Profile.objects.get_profile_by_user(user.email)

        info = {}
        info['email'] = user.email
        info['name'] = email2nickname(email2contact_email(user.email))
        info['contact_email'] = email2contact_email(user.email)
        info['login_id'] = profile.login_id if profile and profile.login_id else ''

        info['is_staff'] = user.is_staff
        info['is_active'] = user.is_active

        data[info['contact_email']] = info

    # result = {'data': data, 'total_count': total_count}
    logger.info(str(data))
    return data


class CallbackCreate(APIView):
    def post(self, request, *args, **kwargs):
        # 获取POST请求的数据
        data = json.loads(request.body)
        print(data)

        # 获取用户信息
        # user_data = data.get('data')
        new_user_username = data.get('name').strip()
        if new_user_username:
            # new_user_role = user_data.get('role')
            # new_user_email = data.get('email')
            new_user_email = new_user_username + "@seafile.com"

            # 创建新用户
            logger.info(f"Try to create user for {new_user_email}")
            user_manager = self.create_user(new_user_email)
            if user_manager:
                virtual_id = user_manager.email
                logger.info(f"Try to create default library for {new_user_email} with virtual_id {virtual_id}")
                repo_id = create_default_library(request, virtual_id)
                if repo_id:
                    logger.info(f"Create defualt library {repo_id} for {new_user_email} successfully!")
                else:
                    logger.info(f"Create defualt library for {new_user_email} failed!")

        # 返回成功响应
        return Response(status=200)

    def create_user(self, email):
        # 创建新用户的逻辑
        user_manager = None
        all_users = list_all_users()
        existed_user = all_users.get(email)
        if existed_user and existed_user.get("email"):
            logger.info(f"Contact Email {email} with Virtual Email {existed_user['email']} already exist. Ignore this procedure!")
            return None

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist as e:
            logger.info(e)
            logger.info(f"Email {email} not exist. Will do this procedure!")
            user = None
        if user:
            logger.info(f"Email {email} already exist. Ignore this procedure!")
        else:
            try:
                user_manager = User.objects.create_user(email=email, password="abcd123456", is_staff=True, is_active=True)
            except Exception as e:
                logger.info(e)
                logger.info(f"Create Email {email} has found it already exist. Ignore this procedure! Beware this causes a virtual user remained.")
        return user_manager


class CallbackDelete(APIView):
    def post(self, request, *args, **kwargs):
        # 获取POST请求的数据
        data = json.loads(request.body)
        print(data)

        # 获取用户信息
        # user_data = data.get('data')
        deleted_user_username = data.get('name')
        deleted_user_email = deleted_user_username + "@seafile.com"
        # deleted_user_email = data.get('email')

        # 删除用户
        self.delete_user(deleted_user_email)

        # 返回成功响应
        return Response(status=200)

    def delete_user(self, email):
        # 删除用户的逻辑
        all_users = list_all_users()
        existed_user = all_users.get(email)
        if existed_user and existed_user.get("email"):
            logger.info(
                f"Contact Email {email} with Virtual Email {existed_user['email']} exists. Will do this procedure!")
        else:
            logger.info(
                f"Contact Email {email} with Virtual Email {existed_user['email']} not existed. Ignore this procedure!")
            return

        virtual_id = existed_user.get("email", "")
        try:
            user = User.objects.get(email=virtual_id)
        except User.DoesNotExist as e:
            logger.info(e)
            user = None
        if not user:
            logger.info(f"Email {email} with virtual_id {virtual_id} found not existed when executing. Fatal Error!")
        else:
            logger.info(f"Try to delete {email} with virtual_id {virtual_id}!")
            user.delete()
            logger.info(f"Delete {email} with virtual_id {virtual_id} successfully!")
        return
