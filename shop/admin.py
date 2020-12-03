from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    #在列表页显示的字段,默认会显示所有字段,有对应的方法可以重写
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']

    #右侧的筛选,必须是字段
    list_filter = ['available', 'created', 'updated']

    #在列表页可以编辑的字段
    #注意:所有在list_editable中的字段必须出现在list_display中
    list_editable = ['price', 'available']

    #用于让slug字段通过name字段自动生成
    prepopulated_fields = {'slug': ('name',)}