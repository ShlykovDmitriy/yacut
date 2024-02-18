import random
import string as s

from .models import URLMap


def get_short_url():
    short = ''.join(random.choice(s.ascii_letters + s.digits) for i in range(6))
    if not check_unique_short_url(short):
        return short
    return get_short_url()


def check_unique_short_url(short):
    return URLMap.query.filter_by(short=short).first()
