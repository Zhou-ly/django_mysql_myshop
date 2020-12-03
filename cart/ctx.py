#自定义上下文处理器
from .cart import Cart
def cart(request):
    return {'cart': Cart(request)}
