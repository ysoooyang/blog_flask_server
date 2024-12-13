import os
import random
import string
from typing import Optional, List
from minio import Minio
from flask import current_app


def get_minio_client() -> Optional[Minio]:
    """获取MinIO客户端"""
    try:
        return Minio(
            endpoint=current_app.config['MINIO_PATH'],
            access_key=current_app.config['MINIO_ACCESS_KEY'],
            secret_key=current_app.config['MINIO_SECRET_KEY'],
            secure=False,
            port=current_app.config['MINIO_PORT']
        )
    except Exception as e:
        current_app.logger.error(f"MinIO客户端创建失败: {str(e)}")
        return None


def generate_random_filename(length: int = 12) -> str:
    """生成随机文件名"""
    chars = string.ascii_letters
    return ''.join(random.choice(chars) for _ in range(length))


def bucket_exists() -> bool:
    """检查bucket是否存在"""
    try:
        client = get_minio_client()
        if not client:
            return False
        return client.bucket_exists(current_app.config['MINIO_BUCKET'])
    except Exception as e:
        current_app.logger.error(f"检查bucket失败: {str(e)}")
        return False


def minio_upload(file_path: str) -> Optional[str]:
    """上传文件到MinIO"""
    try:
        if not bucket_exists():
            current_app.logger.error("Bucket不存在")
            return None

        client = get_minio_client()
        if not client:
            return None

        file_name = generate_random_filename()
        bucket = current_app.config['MINIO_BUCKET']

        # 上传文件
        client.fput_object(
            bucket_name=bucket,
            object_name=file_name,
            file_path=file_path,
            metadata={
                'Content-Type': 'application/octet-stream',
                'X-Amz-Meta-Testing': '1234',
                'Example': '5678'
            }
        )

        return f"/blog-images/{file_name}"

    except Exception as e:
        current_app.logger.error(f"MinIO上传失败: {str(e)}")
        return None


def delete_minio_imgs(img_list: List[str]) -> bool:
    """删除MinIO中的图片"""
    try:
        client = get_minio_client()
        if not client:
            return False

        bucket = current_app.config['MINIO_BUCKET']
        for img in img_list:
            client.remove_object(bucket, img)
        return True

    except Exception as e:
        current_app.logger.error(f"MinIO删除失败: {str(e)}")
        return False