from sqlalchemy import and_, or_, desc
from app.extensions.extensions import db
from app.models.comment import Comment
from app.services.user_service import UserService
from app.services.like_service import LikeService
from app.utils.tool import get_ip_address

class CommentService:
    @staticmethod
    def create_comment(comment):
        """新增评论"""
        try:
            new_comment = Comment(**comment)
            db.session.add(new_comment)
            db.session.commit()
            return new_comment.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def apply_comment(comment):
        """回复评论"""
        try:
            new_comment = Comment(**comment)
            db.session.add(new_comment)
            db.session.commit()
            return new_comment.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def comment_like(id):
        """点赞评论"""
        comment = Comment.query.get(id)
        if comment:
            comment.thumbs_up += 1
            db.session.commit()
            return True
        return False

    @staticmethod
    def cancel_comment_like(id):
        """取消点赞评论"""
        comment = Comment.query.get(id)
        if comment:
            comment.thumbs_up -= 1
            db.session.commit()
            return True
        return False

    @staticmethod
    def delete_comment(id, parent_id):
        """删除评论"""
        try:
            if parent_id > 0:
                result = Comment.query.filter_by(id=id).delete()
            else:
                result = Comment.query.filter_by(id=id).delete()
                Comment.query.filter_by(parent_id=id).delete()
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def back_get_comment_list(params):
        """后台分页获取评论列表"""
        query = Comment.query
        if params.get('content'):
            query = query.filter(Comment.content.like(f"%{params['content']}%"))
        if params.get('to_name'):
            query = query.filter(Comment.to_name.like(f"%{params['to_name']}%"))
        if params.get('from_name'):
            query = query.filter(Comment.from_name.like(f"%{params['from_name']}%"))
        if params.get('time'):
            query = query.filter(Comment.created_at.between(*params['time']))

        total = query.count()
        comments = query.order_by(Comment.created_at.desc()).offset((params['current'] - 1) * params['size']).limit(params['size']).all()

        for comment in comments:
            comment.ip_address = get_ip_address(comment.ip)
            if comment.from_id:
                user = UserService.get_one_user_info(comment.from_id)
                if user:
                    comment.from_avatar = user.avatar
                    comment.from_name = user.nick_name
            if comment.to_id:
                user = UserService.get_one_user_info(comment.to_id)
                if user:
                    comment.to_avatar = user.avatar
                    comment.to_name = user.nick_name

        return {
            'current': params['current'],
            'size': params['size'],
            'total': total,
            'list': [comment.to_dict() for comment in comments]
        }

    @staticmethod
    def front_get_parent_comment(params):
        """前台分页获取父级评论"""
        query = Comment.query.filter_by(type=params['type'], for_id=params['for_id'], parent_id=None)
        order = desc(Comment.created_at) if params['order'] == 'new' else desc(Comment.thumbs_up)
        comments = query.order_by(order).offset((params['current'] - 1) * params['size']).limit(params['size']).all()
        total = query.count()

        for comment in comments:
            comment.ip_address = get_ip_address(comment.ip)
            if comment.from_id:
                user = UserService.get_one_user_info(comment.from_id)
                if user:
                    comment.from_avatar = user.avatar
                    comment.from_name = user.nick_name
            if params['user_id']:
                comment.is_like = LikeService.get_is_like_by_id_and_type(comment.id, 4, params['user_id'])
            else:
                comment.is_like = LikeService.get_is_like_by_ip_and_type(comment.id, 4, params['ip'])

        return {
            'current': params['current'],
            'size': params['size'],
            'total': total,
            'list': [comment.to_dict() for comment in comments]
        }

    @staticmethod
    def front_get_children_comment(params):
        """前台分页获取子评论"""
        query = Comment.query.filter_by(type=params['type'], for_id=params['for_id'], parent_id=params['parent_id'])
        comments = query.order_by(Comment.created_at.asc()).offset((params['current'] - 1) * params['size']).limit(params['size']).all()
        total = query.count()

        for comment in comments:
            comment.ip_address = get_ip_address(comment.ip)
            if comment.from_id:
                user = UserService.get_one_user_info(comment.from_id)
                if user:
                    comment.from_avatar = user.avatar
                    comment.from_name = user.nick_name
            if comment.to_id:
                user = UserService.get_one_user_info(comment.to_id)
                if user:
                    comment.to_avatar = user.avatar
                    comment.to_name = user.nick_name
            if params['user_id']:
                comment.is_like = LikeService.get_is_like_by_id_and_type(comment.id, 4, params['user_id'])
            else:
                comment.is_like = LikeService.get_is_like_by_ip_and_type(comment.id, 4, params['ip'])

        return {
            'current': params['current'],
            'size': params['size'],
            'total': total,
            'list': [comment.to_dict() for comment in comments]
        }

    @staticmethod
    def get_comment_total(params):
        """获取评论总数"""
        return Comment.query.filter_by(for_id=params['for_id'], type=params['type']).count()