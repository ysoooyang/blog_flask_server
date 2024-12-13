from app.extensions.extensions import db
from app.models.photo import Photo
from sqlalchemy import desc


class PhotoService:
    @staticmethod
    def add_photos(photo_list):
        """批量新增图片"""
        try:
            photos = [Photo(**photo) for photo in photo_list]
            db.session.bulk_save_objects(photos)
            db.session.commit()
            return [photo.to_dict() for photo in photos]
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_photos(id_list, delete_type):
        """批量删除图片"""
        try:
            if int(delete_type) == 1:
                # 软删除
                result = Photo.query.filter(Photo.id.in_(id_list)).update(
                    {'status': 2},
                    synchronize_session=False
                )
            else:
                # 硬删除
                result = Photo.query.filter(Photo.id.in_(id_list)).delete(
                    synchronize_session=False
                )
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def revert_photos(id_list):
        """批量恢复图片"""
        try:
            result = Photo.query.filter(Photo.id.in_(id_list)).update(
                {'status': 1},
                synchronize_session=False
            )
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_photos_by_album_id(params):
        """获取图片列表"""
        try:
            query = Photo.query.filter_by(
                album_id=params['id'],
                status=params['status']
            )

            total = query.count()
            photos = query.offset(
                (params['current'] - 1) * params['size']
            ).limit(params['size']).all()

            return {
                'current': params['current'],
                'size': params['size'],
                'list': [photo.to_dict() for photo in photos],
                'total': total
            }
        except Exception as e:
            raise e

    @staticmethod
    def delete_photos_by_album_id(album_id):
        """根据相册id删除图片"""
        try:
            result = Photo.query.filter_by(album_id=album_id).delete()
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_photos_by_album_id(album_id):
        """获取相册所有照片"""
        try:
            photos = Photo.query.filter_by(
                album_id=album_id,
                status=1
            ).order_by(desc(Photo.created_at)).all()
            return [photo.to_dict() for photo in photos]
        except Exception as e:
            raise e