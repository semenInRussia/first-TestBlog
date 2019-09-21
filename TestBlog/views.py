from django.urls import include

from Main.models import MyArticles
from Main.models import Tag

import Main

from django.core.exceptions import PermissionDenied


def access_limitation_article(request, slug):
    article = MyArticles.objects.get(slug=slug)
    condition = article.author.pk==request.user.pk
    if request.user.is_staff or condition:
        return Main.urls
    raise PermissionDenied

def access_limitation_tag(request, slug):
    tag = Tag.objects.get(slug=slug)
    condition = tag.author.pk==request.user.pk
    if request.user.is_staff or condition:
        return Main.urls
    raise PermissionDenied