from django.contrib import admin
from .models import Tag
from .models import MyArticles
from .models import Coments

# Register your models here.

admin.site.register(Tag)
admin.site.register(MyArticles)
admin.site.register(Coments)