from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.decorators.http import require_POST

from cart.cart import Cart
from cart.forms import CartAddProductForm
from shop.models import Product

#向购物车中添加商品
@require_POST   #该视图仅接受POST请求
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart:cart_detail')

#删除商品
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


#展示购物车详情
'''
这个视图为每个购物车的商品对象添加了一个CartAddProductForm对象，这个表单使用当前数量初始化，然后将update字段设置为True，这样在提交表单时，当前的数字直接覆盖原数字。
'''
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        #更新商品数量
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})
