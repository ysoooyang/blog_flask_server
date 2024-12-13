from app.extensions.extensions import db
from app.models.chat import Chat
from app.services.user_service import UserService

class ChatService:
    @staticmethod
    def create_chat(chat):
        """新增聊天"""
        try:
            content_type = chat.get('content_type')
            user_id = chat.get('user_id')
            content = chat.get('content')
            new_chat = Chat(content_type=content_type, content=content, user_id=user_id)
            db.session.add(new_chat)
            db.session.commit()
            return new_chat
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_chats():
        """删除聊天"""
        try:
            result = Chat.query.delete()
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_one_chat(id):
        """删除单条聊天"""
        try:
            result = Chat.query.filter_by(id=id).delete()
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_one_chat(id):
        """根据id获取聊天信息"""
        chat = Chat.query.get(id)
        return chat.to_dict() if chat else None

    @staticmethod
    def get_all_chats():
        """获取所有的聊天记录"""
        chats = Chat.query.filter_by(content_type="image").all()
        return [chat.to_dict() for chat in chats]

    @staticmethod
    def get_chat_list(params):
        """分页获取聊天列表"""
        size = params.get('size')
        last_id = params.get('last_id')
        query = Chat.query

        if last_id:
            query = query.filter(Chat.id < last_id)
        else:
            last_chat = Chat.query.order_by(Chat.id.desc()).first()
            if last_chat:
                last_id = last_chat.id
                query = query.filter(Chat.id <= last_id)

        chats = query.order_by(Chat.id.desc()).limit(size).all()
        total = query.count()

        chat_list = []
        for chat in chats:
            chat_data = chat.to_dict()
            if chat.user_id:
                user = UserService.get_one_user_info(chat.user_id)
                if user:
                    chat_data['nick_name'] = user.nick_name
                    chat_data['avatar'] = user.avatar
                else:
                    chat_data['nick_name'] = "小黑子"
                    chat_data['avatar'] = ""
            chat_list.append(chat_data)

        return {
            'current': last_id,
            'size': len(chat_list),
            'total': total,
            'list': chat_list[::-1]
        }