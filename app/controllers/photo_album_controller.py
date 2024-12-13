from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required
from app.services.photo_album_service import PhotoAlbumService
from app.utils.response import success_response, error_response
from app.utils.qiniu_upload import delete_imgs
from app.config.config import Config

bp = Blueprint('photo_album', __name__)


@bp.route('/', methods=['POST'])
@jwt_required()
def add_album():
    """新增相册"""
    try:
        data = request.get_json()
        album_name = data.get('album_name')

        # 检查相册名是否存在
        one = PhotoAlbumService.get_one_album({'album_name': album_name})
        if one:
            return error_response("已经存在相同的相册名称，换一个试试")

        res = PhotoAlbumService.add_album(data)
        return success_response("创建相册成功", res)
    except Exception as e:
        current_app.logger.error(f"创建相册失败: {str(e)}")
        return error_response("创建相册失败")


@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_album(id):
    """删除相册"""
    try:
        one = PhotoAlbumService.get_one_album({'id': id})
        if one:
            # 删除封面图片
            if Config.UPLOAD_TYPE == "qiniu":
                delete_imgs([one['album_cover'].split("/")[-1]])
            # 其他存储类型的处理...

        res = PhotoAlbumService.delete_album(id)
        return success_response("删除相册成功", res)
    except Exception as e:
        current_app.logger.error(f"删除相册失败: {str(e)}")
        return error_response("删除相册失败")


@bp.route('', methods=['PUT'])
@jwt_required()
def update_album():
    """修改相册"""
    try:
        data = request.get_json()
        id = data.get('id')
        album_name = data.get('album_name')
        album_cover = data.get('album_cover')

        # 检查相册名是否存在
        one = PhotoAlbumService.get_one_album({'album_name': album_name})
        if one and one['id'] != id:
            return error_response("已经存在相同的相册名称，换一个试试")

        # 获取原相册信息
        album = PhotoAlbumService.get_one_album({'id': id})

        # 如果封面更改，删除原封面
        if album and album_cover != album['album_cover']:
            if Config.UPLOAD_TYPE == "qiniu":
                delete_imgs([album['album_cover'].split("/")[-1]])
            # 其他存储类型的处理...

        res = PhotoAlbumService.update_album(data)
        return success_response("修改相册成功", res)
    except Exception as e:
        current_app.logger.error(f"修改相册失败: {str(e)}")
        return error_response("修改相册失败")


@bp.route('/list', methods=['POST'])
def get_album_list():
    """获取相册列表"""
    try:
        data = request.get_json()
        res = PhotoAlbumService.get_album_list(data)
        return success_response("获取相册列表成功", res)
    except Exception as e:
        current_app.logger.error(f"获取相册列表失败: {str(e)}")
        return error_response("获取相册列表失败")


@bp.route('/all', methods=['GET'])
def get_all_album_list():
    """获取所有相册列表"""
    try:
        res = PhotoAlbumService.get_all_album_list()
        return success_response("获取所有相册列表成功", res)
    except Exception as e:
        current_app.logger.error(f"获取所有相册列表失败: {str(e)}")
        return error_response("获取所有相册列表失败")