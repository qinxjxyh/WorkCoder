from django.db import models
from users.models import User
# Create your models here.
# 1.商品分类模型
class GoodsType(models.Model):
    title = models.CharField('分类名称',max_length=30,null=False,default='分类名称')
    is_delete = models.BooleanField('是否下架',default=False)
    def __str__(self):
        return self.title

# 2.商品模型
class Goods(models.Model):
    #商品名称 title varchar
    title = models.CharField('商品名称',max_length=100,default='商品名称')
    #商品描述 desc  varchar(1000)
    desc = models.CharField('商品描述',max_length=1000,null=True)
    #商品图片列表 goods_images varchar(1000) '["images/goods/1.png",]'
    goods_images = models.CharField('商品图片列表',max_length=1000,default='[]')
   # 商品详情图列表 detail_images varchar(1000) '[]'
    detail_images = models.CharField('商品详情图片列表', max_length=1000, default='[]')
    #商品类型 和 GoodsType为一对多关系
    goods_type = models.ForeignKey(GoodsType,on_delete=models.CASCADE)
    #商品规格 spec_name varchar
    spec_name = models.CharField('商品规格',max_length=20,default='规格')
    #商品管理相关的字段
    #商品需要有自己的卖家 卖家也是用户
    saller = models.ForeignKey(User,on_delete=models.CASCADE)
    #商品是否上架(卖家)
    is_saller_empower = models.BooleanField('卖家上架',default=True)
    #管理员审核
    is_admin_empower = models.BooleanField('管理员审批',default=False)
    #商品是否有效
    is_delete = models.BooleanField('商品无效',default=False)

    def __str__(self):
        return self.title

# 3.商品规格明细
class GoodsSpecification(models.Model):
    #定义商品规格
    #商品
    goods = models.ForeignKey(Goods,on_delete=models.CASCADE)
    #价格
    price = models.DecimalField('此规格的价格',max_digits=8,decimal_places=2)
    #信息 '红色16G'
    spec_info =  models.CharField('规格信息',max_length=100,null=False)
    #库存
    stock = models.IntegerField('库存',default=1,null=False)

    def __str__(self):
        return '%s,价格：%s' % (self.spec_info,self.price)