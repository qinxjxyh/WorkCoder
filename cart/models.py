from django.db import models
from users.models import User
from goods.models import GoodsSpecification
# Create your models here.
class CartItem(models.Model):
    #用户
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    #相关商品规格信息
    goods_spec = models.ForeignKey(GoodsSpecification,on_delete=models.CASCADE)
    #商品数量
    count = models.IntegerField('商品个数',default=1)
    def __str__(self):
        return self.user.username + self.goods_spec.spec_info
