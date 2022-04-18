from urllib.parse import urljoin
from django import template
from everybase import settings

register = template.Library()

@register.simple_tag(name='thumbnail_url')
def thumbnail_url(file):
    return urljoin(settings.MEDIA_URL, file.thumbnail_s3_object_key)