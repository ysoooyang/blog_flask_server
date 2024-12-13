from app.extensions.extensions import db
from app.models.like import Like


class LikeService:
    @staticmethod
    def add_like(for_id, type_, user_id=None, ip=None):
        """点赞"""
        try:
            like = Like(for_id=for_id, type=type_, user_id=user_id, ip=ip)
            db.session.add(like)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False

    @staticmethod
    def cancel_like(for_id, type_, user_id=None, ip=None):
        """取消点赞"""
        try:
            query = Like.query.filter_by(for_id=for_id, type=type_)
            if ip:
                query = query.filter_by(ip=ip)
            if user_id:
                query = query.filter_by(user_id=user_id)

            result = query.delete()
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            return None

    @staticmethod
    def get_is_like_by_id_and_type(for_id, type_, user_id):
        """获取用户是否点赞"""
        like = Like.query.filter_by(
            for_id=for_id,
            type=type_,
            user_id=user_id
        ).first()
        return bool(like)

    @staticmethod
    def get_is_like_by_ip_and_type(for_id, type_, ip):
        """获取IP是否点赞"""
        like = Like.query.filter_by(
            for_id=for_id,
            type=type_,
            ip=ip
        ).first()
        return bool(like)