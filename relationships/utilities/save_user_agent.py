from relationships import models as relmods

from django_user_agents.utils import get_user_agent
from ipware import get_client_ip

def save_user_agent(request, user):
    # Record IP and user agent
    r = get_user_agent(request)
    ip_address, is_routable = get_client_ip(request)
    relmods.UserAgent.objects.create(
        user=user,
        ip_address=ip_address,
        is_routable=is_routable,
        is_mobile=r.is_mobile,
        is_tablet=r.is_tablet,
        is_touch_capable=r.is_touch_capable,
        is_pc=r.is_pc,
        is_bot=r.is_bot,
        browser=r.browser,
        browser_family=r.browser.family,
        browser_version=r.browser.version,
        browser_version_string=r.browser.version_string,
        os=r.os,
        os_family=r.os.family,
        os_version=r.os.version,
        os_version_string=r.os.version_string,
        device=r.device,
        device_family=r.device.family
    )