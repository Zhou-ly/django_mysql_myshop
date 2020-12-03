from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart:

    def __init__(self,request):
        """
        初始化购物车对象
        使用商品ID作为字典中的键，其值又是一个由数量和价格构成的字典，这样可以保证不会重复生成同一个商品的购物车数据，也简化了取出购物车数据的方式
        """
        # 使用request对象进行初始化,让类中的其他方法可以访问session数据
        self.session = request.session
        #尝试获取购物车对象
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # 向session中存入空白购物车数据
            #通过为购物车键设置一个空白字段对象从而新建一个购物车对象
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart =cart

#向购物车中增加商品或者更新购物车中的数量
    def add(self, product, quantity=1, update_quantity=False):
        """
        product：要向购物车内添加或更新的product对象
        quantity：商品数量，为整数，默认值为1
        update_quantity：布尔值，为True表示要将商品数量更新为quantity参数的值，为False表示将当前数量增加quantity参数的值。
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
            # 设置session.modified的值为True，中间件在看到这个属性的时候，就会保存session
        self.session.modified = True

    def remove(self, product):
        """
        从购物车中删除商品
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        遍历所有购物车中的商品并从数据库中取得商品对象
        """
        product_ids = self.cart.keys()
        # 获取购物车内的所有商品对象
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        购物车内一共有几种商品
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price'] * item['quantity']) for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
