from django.shortcuts import render
from .models import *
from django.http import Http404
# Create your views here.
def goods_list(request,type_id=None):
    if type_id:
        # 获取所有商品，到页面中展示
        # 通过type_id查找商品
        # 列出符合条件的商品
        # 未过期 是当前卖家的商品 管理员同意 type_id为当前的type_id
        try:
            goods_type = GoodsType.objects.get(id=type_id)
            goods = Goods.objects.filter(goods_type_id=type_id, is_delete=False, is_saller_empower=True,
                                         is_admin_empower=True)
        except:
            # 未通过type_id查找
            # 列出符合条件的商品
            # 未过期 是当前卖家的商品 管理员同意
            goods = Goods.objects.filter(is_delete=False, is_saller_empower=True, is_admin_empower=True)
    else:
        #如果没有type_id
        goods = Goods.objects.filter(is_delete=False,is_saller_empower=True,is_admin_empower=True)
    #展示的商品信息
    #遍历商品列表
    for a_product in goods:
        #图片
        s = a_product.goods_images
        # >>> s = '["images/goods/1.png"]'
        # >>> eval(s)
        # ['images/goods/1.png']
        goods_images = eval(s)
        #取列表的第一张图作为商品的主图片显示
        #/static/images/goods/1/0.png
        try:
            a_product.head_image = '/static/images/goods/'+str(a_product.id)+'/'+goods_images[0]
        except IndexError:
            #显示默认图片
            a_product.head_image = '/static/images/default.png'
        #价格
        #使用商品对象去查找对应的商品规格
        goods_specs = GoodsSpecification.objects.filter(goods=a_product)
        #使用第一个商品规格的价格作为商品的价格
        try:
            a_product.price = goods_specs[0].price
        except IndexError:
            a_product.price = 998
    return render(request,'goods/product_list.html',locals())

def detail(request,goods_id,spec_id=None):
    try:
        if spec_id:
            aspec = GoodsSpecification.objects.get(id = spec_id)
            a_goods = Goods.objects.get(id=aspec.goods_id)
        else:
            a_goods = Goods.objects.get(id=goods_id)
    except:
        raise Http404()
    goods_id = a_goods.id
    #通过商品id查找商品
    #处理显示
    title = a_goods.title
    desc = a_goods.desc
    #图片
    image_list = eval(a_goods.goods_images)
    image_list = [ '/static/images/goods/'+str(a_goods.id)+'/'+img for img in image_list]
    #如果图片列表能获取到 第一个作为主图
    if image_list:
        head_image = image_list[0]
    #否则显示默认图片
    else:
        head_image = '/static/images/defult.png'
    #页面下方的详情大图片
    detail_list = eval(a_goods.detail_images)
    #展示商品规格
    goods_specs = GoodsSpecification.objects.filter(goods_id=a_goods.id)
    #如果没找到 返回404
    if not goods_specs:
        raise Http404()
    #一下逻辑判断当前为哪个规格
    #如果没有传递规格参数 默认第一个商品规格的价格就是商品的价格
    if not spec_id:
        spec_id  = goods_specs[0].id
    else:
        spec_id = int(spec_id)
    for item in goods_specs:
        if spec_id == item.id:
            price = item.price
            #添加一个临时属性 确认那个规格对象被选择
            item.is_select = True
    #点击按钮 通过路由传值的传递spec_id到视图中
    return render(request,'goods/product_details.html',locals())

