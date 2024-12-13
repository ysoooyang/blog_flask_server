from sqlalchemy import or_
from app.extensions.extensions import db
from app.models.category import Category


class CategoryService:
    @staticmethod
    def create_category(category):
        """新增分类"""
        try:
            category_name = category.get('category_name')
            new_category = Category(category_name=category_name)
            db.session.add(new_category)
            db.session.commit()
            return new_category
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update_category(category):
        """修改分类"""
        try:
            id = category.get('id')
            category_name = category.get('category_name')
            result = Category.query.filter_by(id=id).update({'category_name': category_name})
            db.session.commit()
            return result > 0
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_categories(id_list):
        """删除分类"""
        try:
            result = Category.query.filter(Category.id.in_(id_list)).delete()
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_one_category(params):
        """根据id或者分类名称获取分类信息"""
        id = params.get('id')
        category_name = params.get('category_name')

        query = Category.query
        if id:
            query = query.filter_by(id=id)
        if category_name:
            query = query.filter_by(category_name=category_name)

        category = query.first()
        return category.to_dict() if category else None

    @staticmethod
    def get_category_name_by_id(id):
        """通过分类id获取分类名称"""
        category = Category.query.get(id)
        return category.category_name if category else None

    @staticmethod
    def get_category_list(current, size, category_name=None):
        """分页获取分类列表"""
        query = Category.query
        if category_name:
            query = query.filter(Category.category_name.like(f'%{category_name}%'))

        total = query.count()
        categories = query.offset((current - 1) * size).limit(size).all()

        return {
            'current': current,
            'size': size,
            'total': total,
            'list': [category.to_dict() for category in categories]
        }

    @staticmethod
    def get_category_dictionary():
        """获取分类数据字典"""
        categories = Category.query.with_entities(Category.id, Category.category_name).all()
        return [{'id': c.id, 'category_name': c.category_name} for c in categories]

    @staticmethod
    def get_category_count():
        """获取分类总数"""
        return Category.query.count()