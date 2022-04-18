from urllib.parse import urljoin
from django import template
from everybase import settings

register = template.Library()

@register.simple_tag(name='image_url')
def image_url(file):
    return urljoin(settings.MEDIA_URL, file.s3_object_key)