from app.extensions.extensions import db
from app.models.talk import Talk
from app.services.talk_photo_service import TalkPhotoService
from app.services.user_service import UserService
from app.services.like_service import LikeService
from sqlalchemy import desc


class TalkService:
    @staticmethod
    def publish_talk(talk_data):
        """新增说说"""
        try:
            talk_img_list = talk_data.pop('talkImgList', [])
            talk = Talk(**talk_data)
            db.session.add(talk)
            db.session.flush()  # 获取新创建的talk的id

            if talk.id:
                img_list = [{
                    'talk_id': talk.id,
                    'url': img['url']
                } for img in talk_img_list]
                TalkPhotoService.publish_talk_photo(img_list)

            db.session.commit()
            return talk.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update_talk(talk_data):
        """修改说说"""
        try:
            talk_id = talk_data.pop('id')
            talk_img_list = talk_data.pop('talkImgList', [])

            # 更新说说基本信息
            Talk.query.filter_by(id=talk_id).update(talk_data)

            # 更新图片
            TalkPhotoService.delete_talk_photo(talk_id)
            img_list = [{
                'talk_id': talk_id,
                'url': img['url']
            } for img in talk_img_list]
            TalkPhotoService.publish_talk_photo(img_list)

            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_talk_by_id(id, status):
        """删除说说"""
        try:
            if status in [1, 2]:
                result = Talk.query.filter_by(id=id).update({'status': 3})
            else:
                result = Talk.query.filter_by(id=id).delete()
                TalkPhotoService.delete_talk_photo(id)

            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def toggle_public(id, status):
        """切换说说公开性"""
        try:
            result = Talk.query.filter_by(id=id).update({'status': status})
            db.session.commit()
            return bool(result)
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def revert_talk(id):
        """恢复说说"""
        try:
            result = Talk.query.filter_by(id=id).update({'status': 1})
            db.session.commit()
            return bool(result)
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def toggle_top(id, is_top):
        """置顶/取消置顶说说"""
        try:
            result = Talk.query.filter_by(id=id).update({'is_top': is_top})
            db.session.commit()
            return bool(result)
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def talk_like(id):
        """说说点赞"""
        try:
            talk = Talk.query.get(id)
            if talk:
                talk.like_times += 1
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def cancel_talk_like(id):
        """取消说说点赞"""
        try:
            talk = Talk.query.get(id)
            if talk:
                talk.like_times = max(0, talk.like_times - 1)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_talk_list(current, size, status=None):
        """获取说说列表"""
        try:
            query = Talk.query
            if status:
                query = query.filter_by(status=status)

            # 排序
            query = query.order_by(Talk.is_top.asc(), desc(Talk.created_at))

            # 分页
            total = query.count()
            talks = query.offset((current - 1) * size).limit(size).all()

            # 获取图片和用户信息
            for talk in talks:
                talk_dict = talk.to_dict()
                # 获取图片
                photos = TalkPhotoService.get_photo_by_talk_id(talk.id)
                talk_dict['talkImgList'] = [photo['url'] for photo in photos] if photos else []

                # 获取用户信息
                user = UserService.get_one_user_info({'id': talk.user_id})
                if user:
                    talk_dict['nick_name'] = user.get('nick_name')
                    talk_dict['avatar'] = user.get('avatar')

            return {
                'current': current,
                'size': size,
                'total': total,
                'list': [talk.to_dict() for talk in talks]
            }
        except Exception as e:
            raise e

    @staticmethod
    def get_talk_by_id(id):
        """获取说说详情"""
        try:
            talk = Talk.query.get(id)
            if not talk:
                return None

            talk_dict = talk.to_dict()
            photos = TalkPhotoService.get_photo_by_talk_id(id)
            talk_dict['talkImgList'] = [photo['url'] for photo in photos] if photos else []

            return talk_dict
        except Exception as e:
            raise e

    @staticmethod
    def blog_get_talk_list(current, size, user_id, ip):
        """前台获取说说列表"""
        try:
            # 基础查询
            query = Talk.query.filter_by(status=1)
            query = query.order_by(Talk.is_top.asc(), desc(Talk.created_at))

            # 分页
            total = query.count()
            talks = query.offset((current - 1) * size).limit(size).all()

            talk_list = []
            for talk in talks:
                talk_dict = talk.to_dict()

                # 获取图片
                photos = TalkPhotoService.get_photo_by_talk_id(talk.id)
                talk_dict['talkImgList'] = [photo['url'] for photo in photos] if photos else []

                # 获取用户信息
                user = UserService.get_one_user_info({'id': talk.user_id})
                if user:
                    talk_dict['nick_name'] = user.get('nick_name')
                    talk_dict['avatar'] = user.get('avatar')

                # 获取点赞状态
                if user_id:
                    talk_dict['is_like'] = LikeService.get_is_like_by_id_and_type({
                        'for_id': talk.id,
                        'type': 2,
                        'user_id': user_id
                    })
                else:
                    talk_dict['is_like'] = LikeService.get_is_like_by_ip_and_type({
                        'for_id': talk.id,
                        'type': 2,
                        'ip': ip
                    })

                talk_list.append(talk_dict)

            return {
                'current': current,
                'size': size,
                'total': total,
                'list': talk_list
            }
        except Exception as e:
            raise e