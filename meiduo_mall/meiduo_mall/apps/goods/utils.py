def get_breadcrumb(category):
    breadcrumbs = {}
    breadcrumbs['cat3'] = category
    breadcrumbs['cat2'] = category.parent
    cat1 = category.parent.parent
    cat1.url = cat1.goodschannel_set.all()[0].url
    breadcrumbs['cat1'] = cat1
    return breadcrumbs
