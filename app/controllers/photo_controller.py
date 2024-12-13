from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required
from app.services.photo_service import PhotoService
from app.utils.response import success_response, error_response
from app.utils.qiniu_upload import delete_imgs
from app.config.config import Config

bp = Blueprint('photo', __name__)


@bp.route('', methods=['POST'])
@jwt_required()
def add_photos():
    """批量新增图片"""
    try:
        data = request.get_json()
        photo_list = data.get('photoList')
        res = PhotoService.add_photos(photo_list)
        return success_response("新增图片成功", res)
    except Exception as e:
        current_app.logger.error(f"新增图片失败: {str(e)}")
        return error_response("新增图片失败")


@bp.route('/delete', methods=['POST'])
@jwt_required()
def delete_photos():
    """批量删除图片"""
    try:
        data = request.get_json()
        img_list = data.get('imgList')
        delete_type = data.get('type')

        # 获取ID列表
        id_list = [img['id'] for img in img_list]
        res = PhotoService.delete_photos(id_list, delete_type)

        # 远程删除图片
        if delete_type == 2:
            keys = [img['url'].split('/')[-1] for img in img_list]
            if Config.UPLOAD_TYPE == "qiniu":
                delete_imgs(keys)
            # 其他存储类型的处理...

        return success_response("删除图片成功", res)
    except Exception as e:
        current_app.logger.error(f"删除图片失败: {str(e)}")
        return error_response("删除图片失败")


@bp.route('/revert', methods=['POST'])
@jwt_required()
def revert_photos():
    """批量恢复图片"""
    try:
        data = request.get_json()
        id_list = data.get('idList')
        res = PhotoService.revert_photos(id_list)
        return success_response("恢复图片成功", res)
    except Exception as e:
        current_app.logger.error(f"恢复图片失败: {str(e)}")
        return error_response("恢复图片失败")


@bp.route('/list', methods=['POST'])
def get_photos_by_album_id():
    """获取图片列表 分页"""
    try:
        data = request.get_json()
        res = PhotoService.get_photos_by_album_id(data)
        return success_response("获取相册图片成功", res)
    except Exception as e:
        current_app.logger.error(f"获取相册图片失败: {str(e)}")
        return error_response("获取相册图片失败")


@bp.route('/album/<int:id>', methods=['GET'])
def get_all_photos_by_album_id(id):
    """获取相册的所有照片"""
    try:
        res = PhotoService.get_all_photos_by_album_id(id)
        return success_response("获取相册所有照片成功", res)
    except Exception as e:
        current_app.logger.error(f"获取相册所有照片失败: {str(e)}")
        return error_response("获取相册所有照片失败")