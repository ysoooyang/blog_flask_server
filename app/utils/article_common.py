from app.services.article_tag_service import ArticleTagService
from app.services.category_service import CategoryService
from app.services.tag_service import TagService


def create_category_or_return(id, category_name):
    """新增和编辑文章关于分类的公共方法"""
    if id:
        return id

    one_category = CategoryService.get_one_category(category_name=category_name)
    if one_category:
        return one_category.id

    new_category = CategoryService.create_category({"category_name": category_name})
    return new_category.id


def create_article_tag_by_article_id(article_id, tag_list):
    """进行添加文章分类与标签关联的公共方法"""
    result_list = []

    # 处理新增的标签
    for tag in tag_list:
        if not tag.get('id'):
            one = TagService.get_one_tag(tag_name=tag['tag_name'])
            if one:
                tag['id'] = one.id
            else:
                new_tag = TagService.create_tag(tag)
                tag['id'] = new_tag.id

    # 文章id和标签id关联
    if article_id:
        article_tag_list = [{
            'article_id': article_id,
            'tag_id': tag['id']
        } for tag in tag_list]

        result_list = ArticleTagService.create_article_tags(article_tag_list)

    return result_list