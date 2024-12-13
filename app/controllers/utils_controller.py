import os
from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
from app.services.config_service import ConfigService
from app.utils.response import success_response, error_response, tips_response
from app.utils.qiniu_upload import up_to_qiniu, delete_imgs
from app.utils.minio_upload import minio_upload, delete_minio_imgs
from app.utils.tool import is_valid_url
from app.config.config import Config

bp = Blueprint('utils', __name__)


@bp.route('/upload', methods=['POST'])
def upload():
    """图片上传"""
    try:
        if 'file' not in request.files:
            return error_response("文件上传失败")

        file = request.files['file']
        if not file:
            return error_response("文件上传失败")

        filename = secure_filename(file.filename)

        if Config.UPLOAD_TYPE == "local" or not Config.UPLOAD_TYPE:
            # 本地存储
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return success_response("图片上传成功", {
                "url": f"http://127.0.0.1:8888/local/{filename}"
            })
        else:
            complete_url = Config.BASE_URL
            if not is_valid_url(complete_url):
                complete_url = f"http://{complete_url}"
            if not complete_url.endswith('/'):
                complete_url += '/'

            if Config.UPLOAD_TYPE == "qiniu":
                # 七牛云上传
                res = up_to_qiniu(file, filename)
                if res:
                    return success_response("图片上传成功", {
                        "url": f"{complete_url}{res['hash']}"
                    })

            elif Config.UPLOAD_TYPE == "minio":
                # MinIO上传
                res = minio_upload(file)
                if res:
                    return success_response("图片上传成功", {
                        "url": res
                    })

            elif Config.UPLOAD_TYPE == "online":
                # 在线存储
                file_path = os.path.join(current_app.config['ONLINE_UPLOAD_FOLDER'], filename)
                file.save(file_path)
                return success_response("图片上传成功", {
                    "url": f"{complete_url}online/{filename}"
                })

        return error_response("文件上传失败")
    except Exception as e:
        current_app.logger.error(f"文件上传失败: {str(e)}")
        return error_response("文件上传失败")


def delete_online_imgs(img_list):
    """删除服务器下的照片"""
    if not isinstance(img_list, list) or not img_list:
        return

    for img in img_list:
        if img:
            file_path = os.path.join(
                current_app.config['ONLINE_UPLOAD_FOLDER'],
                img
            )
            if os.path.exists(file_path):
                os.remove(file_path)


@bp.route('/config', methods=['PUT'])
@jwt_required()
def update_config():
    """修改网站设置"""
    try:
        data = request.get_json()
        config = ConfigService.get_config()

        # 检查并删除旧图片
        fields_to_check = [
            'avatar_bg', 'blog_avatar', 'qq_link', 'we_chat_link',
            'we_chat_group', 'qq_group', 'we_chat_pay', 'ali_pay'
        ]

        for field in fields_to_check:
            new_value = data.get(field)
            old_value = getattr(config, field, None)

            if new_value and old_value and new_value != old_value:
                img_key = old_value.split('/')[-1]

                if Config.UPLOAD_TYPE == "qiniu":
                    delete_imgs([img_key])
                elif Config.UPLOAD_TYPE == "online":
                    delete_online_imgs([img_key])
                elif Config.UPLOAD_TYPE == "minio":
                    delete_minio_imgs([img_key])

        res = ConfigService.update_config(data)
        return success_response("修改网站设置成功", res)
    except Exception as e:
        current_app.logger.error(f"修改网站设置失败: {str(e)}")
        return error_response("修改网站设置失败")


@bp.route('/config', methods=['GET'])
def get_config():
    """获取网站设置"""
    try:
        res = ConfigService.get_config()
        if res:
            return success_response("获取网站设置成功", res)
        return tips_response("请去博客后台完善博客信息")
    except Exception as e:
        current_app.logger.error(f"获取网站设置失败: {str(e)}")
        return error_response("获取网站设置失败")


@bp.route('/view', methods=['POST'])
def add_view():
    """增加网站访问次数"""
    try:
        res = ConfigService.add_view()
        if res == "添加成功":
            return success_response("增加访问量成功", res)
        elif res == "需要初始化":
            return tips_response("请先初始化网站信息")
    except Exception as e:
        current_app.logger.error(f"增加网站访问量失败: {str(e)}")
        return error_response("增加网站访问量失败")