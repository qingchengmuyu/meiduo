from goods.models import GoodsChannel


def get_categories():
    categories = {}
    goods_channel_qs = GoodsChannel.objects.order_by('group_id', 'sequence')
    for categories_model in goods_channel_qs:
        group_id = categories_model.group_id
        if group_id not in categories:
            categories[group_id] = {
                'channels': [],
                'sub_cats': []
            }
        cat1 = categories_model.category
        cat1.url = categories_model.url
        categories[group_id]['channels'].append(cat1)
        cat2_qs = cat1.subs.all()
        for cat2 in cat2_qs:
            cat3_qs = cat2.subs.all()
            cat2.sub_cats = cat3_qs
            categories[group_id]['sub_cats'].append(cat2)
    return categories
