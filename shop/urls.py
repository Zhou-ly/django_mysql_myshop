from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from shop import views

# 赋予app名字，用来识别
app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]

#有在debug模式下才有作用．它的功能只是实现了从url规则到文件系统的映射
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
