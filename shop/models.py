from django.db import models

# Create your models here.
from django.urls import reverse

#商品品类模型
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)  #db_index=True 则代表着为此字段设置索引
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    # 元数据
    class Meta:
        # 排序
        ordering = ('name',)
        # 可读的模型类名字
        verbose_name = 'category'
        # 模型类的复数形式
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


#商品模型
class Product(models.Model):
    #外键
    #related_name:反向操作时，使用的字段名，用于代替原反向查询时的'表名_set'
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)  #商品简称，用于创建规范化URL
    #需要安装Pillow库
    #在settings.py文件加配置
    #MEDIA_URL = '/media/'
    #MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    #日期时间字段
    #auto_now_add=True，创建数据记录的时候会把当前时间添加到数据库
    #auto_now=True，每次更新数据记录的时候会更新该字段
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        #设置id和slug字段建立联合索引
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_path(self):
        return reverse('shop:product_detail',args=[self.id,self.slug])
