import os
from typing import List
from flask import current_app
from .qiniu_upload import up_to_qiniu, delete_imgs as delete_qiniu_imgs
from .minio_upload import minio_upload, delete_minio_imgs


def delete_online_imgs(img_list: List[str]) -> bool:
    """
    删除在线存储的图片
    Args:
        img_list: 图片文件名列表
    Returns:
        bool: 删除是否成功
    """
    try:
        for img in img_list:
            if img:
                # 构建文件完整路径
                file_path = os.path.join(
                    current_app.config['UPLOAD_FOLDER'],
                    'online',
                    img
                )
                # 检查文件是否存在并删除
                if os.path.exists(file_path):
                    os.remove(file_path)
        return True
    except Exception as e:
        current_app.logger.error(f"删除在线图片失败: {str(e)}")
        return False


def delete_images(img_list: List[str]) -> bool:
    """
    根据不同的存储类型删除图片
    Args:
        img_list: 图片URL或文件名列表
    Returns:
        bool: 删除是否成功
    """
    try:
        # 提取文件名
        file_names = [img.split('/')[-1] for img in img_list if img]
        if not file_names:
            return True

        upload_type = current_app.config['UPLOAD_TYPE']

        if upload_type == 'qiniu':
            return delete_qiniu_imgs(file_names)
        elif upload_type == 'minio':
            return delete_minio_imgs(file_names)
        elif upload_type == 'online':
            return delete_online_imgs(file_names)
        elif upload_type == 'local':
            # 本地存储的删除逻辑
            return delete_online_imgs(file_names)

        return True
    except Exception as e:
        current_app.logger.error(f"删除图片失败: {str(e)}")
        return False