from app.extensions.extensions import db
from app.models.config import Config


class ConfigService:
    @staticmethod
    def update_config(config_data):
        """更新配置"""
        try:
            id = config_data.get('id')
            config = Config.query.get(id)

            if config:
                # 更新现有配置
                for key, value in config_data.items():
                    setattr(config, key, value)
            else:
                # 创建新配置
                config = Config(**config_data)
                db.session.add(config)

            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False

    @staticmethod
    def get_config():
        """获取配置"""
        try:
            config = Config.query.first()
            return config if config else False
        except Exception as e:
            return False

    @staticmethod
    def add_view():
        """增加访问量"""
        try:
            config = Config.query.first()
            if config:
                config.view_time += 1
                db.session.commit()
                return "添加成功"
            return "需要初始化"
        except Exception as e:
            db.session.rollback()
            return "需要初始化"