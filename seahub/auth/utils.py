# Copyright (c) 2012-2016 Seafile Ltd.
from django.core.cache import cache
from django.conf import settings

from seahub.profile.models import Profile
from seahub.utils import normalize_cache_key
from seahub.utils.ip import get_remote_ip

import logging

from seahub.base.accounts import User
from seaserv import seafile_api, ccnet_api
from seahub.base.templatetags.seahub_tags import email2nickname, email2contact_email

LOGIN_ATTEMPT_PREFIX = 'UserLoginAttempt_'

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

def find_request_user(request):
    user_header = request.headers.get('X-Bfl-User')
    if user_header and user_header.strip():
        username = user_header + "@seafile.com"
        logger.info(f"username: {username}")

        all_users = list_all_users()
        logger.info(f"all_users: {all_users}")
        existed_user = all_users.get(username)
        if existed_user and existed_user.get("email"):
            logger.info(f"Contact Email {username} with Virtual Email {existed_user['email']} exists!")
        else:
            logger.info(f"Contact Email {username} with Virtual Email {existed_user['email']} doesn't exist!")

        virtual_email = existed_user.get("email")
        try:
            user = User.objects.get(email=virtual_email)
            if user:
                logger.info(f"User existed_user_email {virtual_email} found.")
                return user
        except User.DoesNotExist:
            logger.info(f"User does not exist.")
    return None



def get_login_failed_attempts(username=None, ip=None):
    """Get login failed attempts base on username and ip.
    If both username and ip are provided, return the max value.

    Arguments:
    - `username`:
    - `ip`:
    """
    if username is None and ip is None:
        return 0

    username_attempts = ip_attempts = 0

    if username:
        cache_key = normalize_cache_key(username, prefix=LOGIN_ATTEMPT_PREFIX)
        username_attempts = cache.get(cache_key, 0)

    if ip:
        cache_key = normalize_cache_key(ip, prefix=LOGIN_ATTEMPT_PREFIX)
        ip_attempts = cache.get(cache_key, 0)

    return max(username_attempts, ip_attempts)


def incr_login_failed_attempts(username=None, ip=None):
    """Increase login failed attempts by 1 for both username and ip.

    Arguments:
    - `username`:
    - `ip`:

    Returns new value of failed attempts.
    """
    timeout = settings.LOGIN_ATTEMPT_TIMEOUT
    username_attempts = 1
    ip_attempts = 1

    if username:
        cache_key = normalize_cache_key(username, prefix=LOGIN_ATTEMPT_PREFIX)
        try:
            username_attempts = cache.incr(cache_key)
        except ValueError:
            cache.set(cache_key, 1, timeout)

    if ip:
        cache_key = normalize_cache_key(ip, prefix=LOGIN_ATTEMPT_PREFIX)
        try:
            ip_attempts = cache.incr(cache_key)
        except ValueError:
            cache.set(cache_key, 1, timeout)

    return max(username_attempts, ip_attempts)


def clear_login_failed_attempts(request, username):
    """Clear login failed attempts records.

    Arguments:
    - `request`:
    """
    ip = get_remote_ip(request)

    cache.delete(normalize_cache_key(username, prefix=LOGIN_ATTEMPT_PREFIX))
    cache.delete(normalize_cache_key(ip, prefix=LOGIN_ATTEMPT_PREFIX))
    p = Profile.objects.get_profile_by_user(username)
    if p and p.login_id:
        cache.delete(normalize_cache_key(p.login_id, prefix=LOGIN_ATTEMPT_PREFIX))


def get_virtual_id_by_email(email):
    p = Profile.objects.get_profile_by_contact_email(email)
    if p is None:
        return email
    else:
        return p.user
