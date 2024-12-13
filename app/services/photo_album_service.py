from app.extensions.extensions import db
from app.models.photo_album import PhotoAlbum
from app.services.photo_service import PhotoService
from sqlalchemy import desc


class PhotoAlbumService:
    @staticmethod
    def add_album(data):
        """新增相册"""
        try:
            album = PhotoAlbum(
                album_name=data.get('album_name'),
                album_cover=data.get('album_cover'),
                description=data.get('description')
            )
            db.session.add(album)
            db.session.commit()
            return album.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_album(id):
        """删除相册"""
        try:
            # 删除相册
            result = PhotoAlbum.query.filter_by(id=id).delete()
            # 删除相册下的所有照片
            PhotoService.delete_photos_by_album_id(id)

            db.session.commit()
            return bool(result)
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update_album(data):
        """修改相册"""
        try:
            album = PhotoAlbum.query.get(data['id'])
            if album:
                album.album_name = data.get('album_name')
                album.album_cover = data.get('album_cover')
                album.description = data.get('description')
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_album_list(params):
        """获取相册列表"""
        try:
            query = PhotoAlbum.query

            if params.get('album_name'):
                query = query.filter(
                    PhotoAlbum.album_name.like(f"%{params['album_name']}%")
                )

            total = query.count()
            albums = query.offset(
                (params['current'] - 1) * params['size']
            ).limit(params['size']).all()

            return {
                'current': params['current'],
                'size': params['size'],
                'list': [album.to_dict() for album in albums],
                'total': total
            }
        except Exception as e:
            raise e

    @staticmethod
    def get_one_album(params):
        """获取单个相册信息"""
        try:
            query = PhotoAlbum.query

            if params.get('id'):
                query = query.filter_by(id=params['id'])
            if params.get('album_name'):
                query = query.filter_by(album_name=params['album_name'])

            album = query.first()
            return album.to_dict() if album else None
        except Exception as e:
            raise e

    @staticmethod
    def get_all_album_list():
        """获取所有相册"""
        try:
            albums = PhotoAlbum.query.order_by(desc(PhotoAlbum.created_at)).all()
            return [album.to_dict() for album in albums]
        except Exception as e:
            raise e