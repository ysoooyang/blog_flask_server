from app.extensions.extensions import db
from app.models.tag import Tag
from sqlalchemy import or_


class TagService:
    @staticmethod
    def create_tag(data):
        """新增标签"""
        try:
            tag = Tag(tag_name=data.get('tag_name'))
            db.session.add(tag)
            db.session.commit()
            return tag.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update_tag(data):
        """修改标签"""
        try:
            tag = Tag.query.get(data['id'])
            if tag:
                tag.tag_name = data.get('tag_name')
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_tags(id_list):
        """删除标签"""
        try:
            result = Tag.query.filter(Tag.id.in_(id_list)).delete(synchronize_session=False)
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_one_tag(params):
        """获取单个标签"""
        try:
            query = Tag.query

            if params.get('id'):
                query = query.filter_by(id=params['id'])
            if params.get('tag_name'):
                query = query.filter_by(tag_name=params['tag_name'])

            tag = query.with_entities(Tag.id, Tag.tag_name).first()
            return tag.to_dict() if tag else None
        except Exception as e:
            raise e

    @staticmethod
    def get_tag_list(params):
        """分页获取标签列表"""
        try:
            query = Tag.query

            if params.get('tag_name'):
                query = query.filter(Tag.tag_name.like(f"%{params['tag_name']}%"))

            total = query.count()
            tags = query.offset(
                (params['current'] - 1) * params['size']
            ).limit(params['size']).all()

            return {
                'current': params['current'],
                'size': params['size'],
                'total': total,
                'list': [tag.to_dict() for tag in tags]
            }
        except Exception as e:
            raise e

    @staticmethod
    def get_tag_by_tag_id_list(tag_id_list):
        """根据标签ID列表获取标签信息"""
        try:
            tags = Tag.query.filter(
                Tag.id.in_(tag_id_list)
            ).with_entities(Tag.id, Tag.tag_name).all()

            tag_name_list = [tag.tag_name for tag in tags]
            return {
                'tagNameList': tag_name_list,
                'tagList': [tag.to_dict() for tag in tags]
            }
        except Exception as e:
            raise e

    @staticmethod
    def get_tag_dictionary():
        """获取标签字典"""
        try:
            tags = Tag.query.with_entities(Tag.id, Tag.tag_name).all()
            return [tag.to_dict() for tag in tags] if tags else None
        except Exception as e:
            raise e

    @staticmethod
    def get_tag_count():
        """获取标签总数"""
        try:
            return Tag.query.count()
        except Exception as e:
            raise e