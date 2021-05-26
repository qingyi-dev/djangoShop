from django.conf.urls import url
from django.contrib import admin

# Register your models here.
from app import models

urlpatterns = [
    url(r'^admin', admin.site.urls),

]
admin.site.register(models.Goods)
admin.site.register(models.GoodsType)