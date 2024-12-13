from app.extensions.extensions import db
from app.models.header import Header


class HeaderService:
    @staticmethod
    def add_or_update_header(data):
        """新增/修改背景"""
        try:
            id = data.get('id')
            route_name = data.get('route_name')
            bg_url = data.get('bg_url')

            if id:
                # 更新
                header = Header.query.get(id)
                if header:
                    header.route_name = route_name
                    header.bg_url = bg_url
            else:
                # 新增
                header = Header(route_name=route_name, bg_url=bg_url)
                db.session.add(header)

            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False

    @staticmethod
    def delete_header(id):
        """根据id删除背景"""
        try:
            result = Header.query.filter_by(id=id).delete()
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            return None

    @staticmethod
    def get_all_header():
        """获取所有背景"""
        headers = Header.query.with_entities(
            Header.id,
            Header.route_name,
            Header.bg_url
        ).all()
        return [header._asdict() for header in headers]

    @staticmethod
    def get_one_by_path(route_name):
        """根据路径获取背景"""
        header = Header.query.filter_by(route_name=route_name).first()
        return header.to_dict() if header else None