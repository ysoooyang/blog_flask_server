from app.extensions.extensions import db
from app.models.notify import Notify
from sqlalchemy import desc


class NotifyService:
    @staticmethod
    def create_notify(data):
        """新增消息通知"""
        try:
            notify = Notify(
                user_id=data.get('user_id'),
                type=data.get('type'),
                to_id=data.get('to_id'),
                message=data.get('message')
            )
            db.session.add(notify)
            db.session.commit()
            return notify.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update_notify(id):
        """已阅消息通知"""
        try:
            notify = Notify.query.get(id)
            if notify:
                notify.is_view = 2
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_notifys(id):
        """删除消息通知"""
        try:
            result = Notify.query.filter_by(id=id).delete()
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_notify_list(params):
        """获取当前用户的消息推送"""
        try:
            query = Notify.query

            if params.get('userId'):
                query = query.filter_by(user_id=params['userId'])

            total = query.count()
            notifies = query.order_by(
                Notify.is_view.asc(),
                desc(Notify.created_at)
            ).offset(
                (params['current'] - 1) * params['size']
            ).limit(params['size']).all()

            return {
                'current': params['current'],
                'size': params['size'],
                'total': total,
                'list': [notify.to_dict() for notify in notifies]
            }
        except Exception as e:
            raise e