from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from goods.models import GoodsSpecification
from .models import CartItem
# Create your views here.
#添加购物车
@login_required(login_url='/users/login/')
def add_cart(request):
    #如果是post请求
    if request.method == 'POST':
    #接收用户提交的数据
    #商品详情页只能提供spec_id 和count
        spec_id = request.POST.get('spec_id')
        goods_count = request.POST.get('count')
        #通过规格ID查找对应的商品规格对象
        #导入商品规格模型
        try:
            spec = GoodsSpecification.objects.get(id = spec_id)
        except:
            return HttpResponse('没有获取到商品信息')
        #添加购物车 将数据保存到数据库
        #导入购物车模型
        #判断之前该用户是否已经添加此类商品
        # if CartItem.objects.get(goods_spec=spec_id,user=request.user):
        try:
            #如果添加过 堆叠商品数量
            item = CartItem.objects.get(goods_spec=spec_id,user=request.user)
            item.count += int(goods_count)
        except:
        #     # 如果未添加 创建新的购物车商品
            item = CartItem(user=request.user,goods_spec=spec,count=goods_count)
        item.save()
    return HttpResponse('添加购物车成功')

#显示购物车列表
@login_required(login_url='/users/login')
def list_all(request):
    #查询当前用户的所有购物车信息
    cart_items = CartItem.objects.filter(user = request.user)
    for item in cart_items:
        #计算总价
        #通过item的中保存的商品规格信息获取商品价格 * 数量得到总价
        item.total = item.goods_spec.price * item.count
        #获取商品对象的图片以及标题等信息
        a_product = item.goods_spec.goods
        try:
            s = a_product.goods_images
            goods_images = eval(s)
            item.head_image = '/static/images/goods/'+str(a_product.id)+'/'+goods_images[0]
        except:
            item.head_image = '/static/images/default.png'
    return render(request,'cart/cart_list.html',locals())


def delete(request,id):
    try:
        item = CartItem.objects.get(id=id,user=request.user)
        item.delete()
    except:
        return HttpResponse('购物车没有此商品')
    return redirect('/cart/')
