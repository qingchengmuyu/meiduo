from django import http
from django.shortcuts import render
from django.views import View
from .models import ContentCategory
from .utils import get_categories


class IndexView(View):
    def get(self, request):
        contents = {}
        contents_category_qs = ContentCategory.objects.all()
        for contents_category in contents_category_qs:
            contents[contents_category.key] = contents_category.content_set.filter(status=True).order_by('sequence')
        context = {
            'categories': get_categories(),
            'contents': contents
        }
        return render(request, 'index.html', context)
