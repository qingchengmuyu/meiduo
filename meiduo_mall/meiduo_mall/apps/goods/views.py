from django.shortcuts import render
from django.views import View
from django import http
from django.core.paginator import Paginator, EmptyPage

from .models import GoodsCategory
from contents.utils import get_categories
from .utils import get_breadcrumb


class LastView(View):
    """商品列表页面"""

    def get(self, request, category_id, page_num):
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return http.HttpResponseForbidden('category_id不存在')
        sort = request.GET.get('sort', 'default')
        sort_field = '-create_time'
        if sort == 'price':
            sort_field = '-price'
        elif sort == 'hot':
            sort_field = '-sales'
        sku_qs = category.sku_set.filter(is_launched=True).order_by(sort_field)
        paginator = Paginator(sku_qs, 5)
        try:
            page_skus = paginator.page(page_num)
        except EmptyPage:
            return http.HttpResponseForbidden("超出指定页")
        total_page = paginator.num_pages
        context = {
            'categories': get_categories(),
            'breadcrumb': get_breadcrumb(category),
            'sort': sort,
            'category': category,
            'page_skus': page_skus,
            'total_page': total_page,
            'page_num': page_num
        }

        return render(request, 'list.html', context)

