from sqlalchemy import desc
from app.extensions.extensions import db
from app.models.message import Message
from app.services.comment_service import CommentService
from app.services.like_service import LikeService
from app.services.user_service import UserService


class MessageService:
    @staticmethod
    def add_message(message, color, font_size, font_weight, bg_color, bg_url, user_id, tag, nick_name):
        """发布留言"""
        try:
            new_message = Message(
                message=message,
                color=color,
                font_size=font_size,
                font_weight=font_weight,
                bg_color=bg_color,
                bg_url=bg_url,
                user_id=user_id,
                tag=tag,
                nick_name=nick_name
            )
            db.session.add(new_message)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False

    @staticmethod
    def update_message(data):
        """修改留言"""
        try:
            message = Message.query.get(data['id'])
            if message:
                message.message = data.get('message')
                message.color = data.get('color')
                message.font_size = data.get('font_size')
                message.font_weight = data.get('font_weight')
                message.bg_color = data.get('bg_color')
                message.bg_url = data.get('bg_url')
                message.tag = data.get('tag')
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            return False

    @staticmethod
    def delete_message(id_list):
        """删除留言"""
        try:
            result = Message.query.filter(Message.id.in_(id_list)).delete(synchronize_session=False)
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            return None

    @staticmethod
    def message_like(id):
        """点赞留言"""
        try:
            message = Message.query.get(id)
            if message:
                message.like_times += 1
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            return False

    @staticmethod
    def cancel_message_like(id):
        """取消点赞留言"""
        try:
            message = Message.query.get(id)
            if message:
                message.like_times = max(0, message.like_times - 1)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            return False

    @staticmethod
    def get_message_list(params):
        """分页获取留言"""
        try:
            query = Message.query

            if params.get('tag'):
                query = query.filter_by(tag=params['tag'])
            if params.get('message'):
                query = query.filter(Message.message.like(f"%{params['message']}%"))
            if params.get('time'):
                query = query.filter(Message.created_at.between(*params['time']))

            total = query.count()
            messages = query.order_by(desc(Message.created_at)).offset(
                (params['current'] - 1) * params['size']
            ).limit(params['size']).all()

            # 获取用户信息
            for message in messages:
                if message.user_id:
                    user = UserService.get_one_user_info({'id': message.user_id})
                    if user:
                        message.nick_name = user.nick_name
                        message.avatar = user.avatar
                else:
                    message.avatar = ""

            # 获取点赞状态
            if params.get('user_id'):
                for message in messages:
                    message.is_like = LikeService.get_is_like_by_id_and_type(
                        message.id, 3, params['user_id']
                    )
            else:
                for message in messages:
                    message.is_like = LikeService.get_is_like_by_ip_and_type(
                        message.id, 3, params['ip']
                    )

            # 获取评论数
            for message in messages:
                message.comment_total = CommentService.get_comment_total({
                    'for_id': message.id,
                    'type': 3
                })

            return {
                'current': params['current'],
                'size': params['size'],
                'list': [message.to_dict() for message in messages],
                'total': total
            }
        except Exception as e:
            return None

    @staticmethod
    def get_all_message():
        """获取所有留言"""
        try:
            messages = Message.query.order_by(desc(Message.created_at)).all()
            total = len(messages)

            # 获取用户信息
            for message in messages:
                if message.user_id:
                    user = UserService.get_one_user_info({'id': message.user_id})
                    if user:
                        message.nick_name = user.nick_name
                        message.avatar = user.avatar
                else:
                    message.avatar = ""

            return {
                'list': [message.to_dict() for message in messages],
                'total': total
            }
        except Exception as e:
            return None

    @staticmethod
    def get_message_tag():
        """获取热门标签"""
        try:
            messages = Message.query.all()
            tag_dict = {}

            for message in messages:
                if message.tag:
                    tag_dict[message.tag] = tag_dict.get(message.tag, 0) + 1

            # 转换为列表并排序
            tag_list = [{'tag': tag, 'count': count} for tag, count in tag_dict.items()]
            tag_list.sort(key=lambda x: x['count'], reverse=True)

            return tag_list[:10]
        except Exception as e:
            return []