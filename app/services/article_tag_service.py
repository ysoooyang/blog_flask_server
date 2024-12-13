from app.extensions.extensions import db
from app.models.article_tag import ArticleTag
from app.services.tag_service import TagService


class ArticleTagService:
    @staticmethod
    def create_article_tags(tag_list):
        """批量增加文章标签关联"""
        try:
            article_tags = [ArticleTag(**tag) for tag in tag_list]
            db.session.bulk_save_objects(article_tags)
            db.session.commit()
            return [tag.to_dict() for tag in article_tags]
        except Exception as e:
            db.session.rollback()
            return None

    @staticmethod
    def delete_article_tag(article_id):
        """根据文章id删除文章标签关联"""
        try:
            result = ArticleTag.query.filter_by(article_id=article_id).delete()
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            return 0

    @staticmethod
    def get_tag_list_by_article_id(article_id):
        """根据文章id获取标签名称列表"""
        tags = ArticleTag.query.filter_by(article_id=article_id).all()
        tag_ids = [tag.tag_id for tag in tags]
        tag_data = TagService.get_tag_by_tag_id_list(tag_ids)

        return {
            'tagList': tag_data['tagList'],
            'tagIdList': tag_ids,
            'tagNameList': tag_data['tagNameList']
        }

    @staticmethod
    def get_article_id_list_by_tag_id(tag_id):
        """根据标签id获取该标签下所有的文章id"""
        tags = ArticleTag.query.filter_by(tag_id=tag_id).all()
        article_ids = list(set(tag.article_id for tag in tags))
        return article_ids if article_ids else None

    @staticmethod
    def get_one_article_tag(article_id, tag_id):
        """查询满足的关联"""
        tag = ArticleTag.query.filter_by(
            article_id=article_id,
            tag_id=tag_id
        ).first()
        return bool(tag)