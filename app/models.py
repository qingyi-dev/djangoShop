from django.db import models


# Create your models here.
class Goods(models.Model):
    # id = models.IntegerField(primary_key=True, auto_created=True, null=False, verbose_name='商品ID')
    name = models.CharField(max_length=20, null=False, verbose_name='商品名称')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    unite = models.CharField(max_length=20, verbose_name='商品单位')
    image = models.ImageField(upload_to='static', verbose_name='商品图片')
    stock = models.IntegerField(default=1, verbose_name='商品库存')
    type = models.ForeignKey('GoodsType', on_delete=models.CASCADE, verbose_name='商品种类')
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='收藏用户', null=True)

    # user_loved_id = models.IntegerField(default=0)

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name


class GoodsType(models.Model):
    # id = models.IntegerField(max_length=12, auto_created=True, null=False, verbose_name='商品分类ID')
    name = models.CharField(max_length=20, null=False, verbose_name='商品分类名称')

    # image = models.ImageField(upload_to='static', verbose_name='商品图片')

    class Meta:
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name


class User(models.Model):
    # id = models.IntegerField(null=False, primary_key=True, auto_created=True, verbose_name="用户ID")
    name = models.CharField(max_length=56, null=False, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=256, null=True, verbose_name='用户密码')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name


# 购物车
class Cart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='加购用户')
    goods = models.ForeignKey(to=Goods, on_delete=models.CASCADE, verbose_name='加购商品')
    count = models.IntegerField(max_length=3, default=1, verbose_name='加购数量')

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
