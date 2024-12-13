from typing import List, Optional
import qiniu
from flask import current_app


def get_qiniu_client():
    """获取七牛云客户端"""
    access_key = current_app.config['QINIU_ACCESS_KEY']
    secret_key = current_app.config['QINIU_SECRET_KEY']

    q = qiniu.Auth(access_key, secret_key)
    bucket_manager = qiniu.BucketManager(q, qiniu.config.Config())

    return q, bucket_manager


def up_to_qiniu(file_data, key: str) -> Optional[dict]:
    """上传文件到七牛云"""
    try:
        auth, _ = get_qiniu_client()
        bucket = current_app.config['QINIU_BUCKET']

        # 生成上传凭证
        token = auth.upload_token(bucket, key)

        # 配置上传区域
        config = qiniu.config.Config()
        config.zone = qiniu.zone.Zone_z2

        # 创建上传对象
        uploader = qiniu.put_data.PutData(
            up_token=token,
            key=key,
            data=file_data,
            params={},
            mime_type=None,
            progress_handler=None,
            upload_progress_recorder=None,
            config=config
        )

        ret, info = uploader.upload()
        if info.status_code == 200:
            return ret
        return None

    except Exception as e:
        current_app.logger.error(f"七牛云上传失败: {str(e)}")
        return None


def delete_imgs(img_list: List[str]) -> bool:
    """删除七牛云上的图片"""
    try:
        _, bucket_manager = get_qiniu_client()
        bucket = current_app.config['QINIU_BUCKET']

        # 构建批量删除操作
        delete_ops = [qiniu.build_batch_delete_op(bucket, key) for key in img_list]

        # 执行批量删除
        ret, info = bucket_manager.batch(delete_ops)

        if info.status_code == 200:
            for item in ret:
                if item['code'] != 200:
                    current_app.logger.error(f"删除失败: {item}")
            return True

        return False

    except Exception as e:
        current_app.logger.error(f"七牛云删除失败: {str(e)}")
        return False