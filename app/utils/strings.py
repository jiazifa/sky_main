# -*- coding: utf-8 -*-

import hashlib
import random
import datetime
import time
import re
from .regex import is_emoji
from typing import Dict, List, Optional


def get_unix_time_tuple(
    date = datetime.datetime.now(),
    millisecond: bool = False
) -> str:
    """ get time tuple

    get unix time tuple, default `date` is current time

    Args:
        date: datetime, default is datetime.datetime.now()
        millisecond: if True, Use random three digits instead of milliseconds, default id False 

    Return:
        a str type value, return unix time of incoming time
    """
    time_tuple = time.mktime(date.timetuple())
    time_tuple = round(time_tuple * 1000) if millisecond else time_tuple
    second = str(int(time_tuple))
    return second


def get_date_from_time_tuple(unix_time: str = get_unix_time_tuple(), formatter: str = '%Y-%m-%d %H:%M:%S') -> str:
    """ translate unix time tuple to time

    get time from unix time

    Args:
        unix_time: unix time tuple
        formatter: str time formatter

    Return:
        a time type value, return time of incoming unix_time
    """
    if len(unix_time) == 13:
        unix_time = str(float(unix_time) / 1000)
    t = int(unix_time)
    time_locol = time.localtime(t)
    return time.strftime(formatter, time_locol)


def getmd5(code: str) -> Optional[str]:
    """ return md5 value of incoming code

    get md5 from code

    Args:
        code: str value

    Return:
        return md5 value of code
    """
    if code:
        md5string = hashlib.md5(code.encode('utf-8'))
        return md5string.hexdigest()
    return None


def get_random_num(digit: int = 6) -> str:
    """ get a random num

    get random num 

    Args:
        digit: digit of the random num, limit (1, 32)

    Return:
        return Generated random num
    """
    if digit is None:
        digit = 1
    digit = min(max(digit, 1), 32)  # 最大支持32位
    result = ""
    while len(result) < digit:
        append = str(random.randint(1, 9))
        result = result + append
    return result



def contain_emoji(content: str) -> bool:
    """ judge str contain emoji str

    Args: str type

    Return : Bool type, return True if contain Emoji, else False
    """
    for c in content:
        if is_emoji(c):
            return True
    return False


def get_domain(url: str) -> str:
    """ get domain from url by given

    Args: str type
    Return: str type, return domain if can get
    """
    from urllib.parse import urlparse
    parsed_uri = urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    return domain


def filter_all_img_src(content: str) -> List[str]:
    replace_pattern = r'<[img|IMG].*?>'  # img标签的正则式
    img_url_pattern = r'.+?src="(\S+)"'  # img_url的正则式
    replaced_img_url_list: List[str] = []
    img_url_list = []
    need_replace_list = re.findall(replace_pattern, content)  # 找到所有的img标签
    for tag in need_replace_list:
        imgs = re.findall(img_url_pattern, tag)
        if imgs:
            img_url_list.append(imgs[0])  # 找到所有的img_url
    return img_url_list
