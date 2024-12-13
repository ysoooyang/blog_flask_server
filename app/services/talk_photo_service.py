from app.extensions.extensions import db
from app.models.talk_photo import TalkPhoto
from app.config.config import Config
from app.utils.qiniu_upload import delete_imgs
from app.controllers.utils_controller import delete_online_imgs
from app.utils.minio_upload import delete_minio_imgs


class TalkPhotoService:
    @staticmethod
    def publish_talk_photo(img_list):
        """新增说说图片"""
        try:
            photos = [TalkPhoto(**img) for img in img_list]
            db.session.bulk_save_objects(photos)
            db.session.commit()
            return [photo.to_dict() for photo in photos]
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_talk_photo(talk_id):
        """根据说说id删除图片"""
        try:
            # 获取所有图片URL
            photos = TalkPhoto.query.filter_by(talk_id=talk_id).all()
            if photos:
                keys = [photo.url.split('/')[-1] for photo in photos]

                # 根据不同存储类型删除远程图片
                if Config.UPLOAD_TYPE == "qiniu":
                    delete_imgs(keys)
                elif Config.UPLOAD_TYPE == "online":
                    delete_online_imgs(keys)
                elif Config.UPLOAD_TYPE == "minio":
                    delete_minio_imgs(keys)

                # 删除数据库记录
                result = TalkPhoto.query.filter_by(talk_id=talk_id).delete()
                db.session.commit()
                return result
            return 0
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_photo_by_talk_id(talk_id):
        """根据说说id获取图片列表"""
        try:
            photos = TalkPhoto.query.filter_by(talk_id=talk_id).all()
            return [{'talk_id': photo.talk_id, 'url': photo.url} for photo in photos] if photos else []
        except Exception as e:
            raise e