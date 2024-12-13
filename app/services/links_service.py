from app.extensions.extensions import db
from app.models.links import Links


class LinksService:
    @staticmethod
    def add_or_update_links(data):
        """新增/编辑友链"""
        try:
            id = data.get('id')
            if id:
                # 更新
                link = Links.query.get(id)
                if link:
                    link.site_name = data.get('site_name')
                    link.site_desc = data.get('site_desc')
                    link.site_avatar = data.get('site_avatar')
                    link.url = data.get('url')
                    link.status = data.get('status')
            else:
                # 新增
                link = Links(
                    site_name=data.get('site_name'),
                    site_desc=data.get('site_desc'),
                    site_avatar=data.get('site_avatar'),
                    url=data.get('url'),
                    status=1,
                    user_id=data.get('user_id')
                )
                db.session.add(link)

            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False

    @staticmethod
    def delete_links(id_list):
        """批量删除友链"""
        try:
            result = Links.query.filter(Links.id.in_(id_list)).delete(synchronize_session=False)
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            return None

    @staticmethod
    def approve_links(id_list):
        """批量审核友链"""
        try:
            result = Links.query.filter(Links.id.in_(id_list)).update({'status': 2}, synchronize_session=False)
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            return None

    @staticmethod
    def get_links_list(params):
        """分页获取友链"""
        try:
            query = Links.query
            if params.get('site_name'):
                query = query.filter(Links.site_name.like(f"%{params['site_name']}%"))
            if params.get('status'):
                query = query.filter_by(status=params['status'])
            if params.get('time'):
                query = query.filter(Links.created_at.between(*params['time']))

            total = query.count()
            links = query.order_by(Links.created_at.asc()).offset((params['current'] - 1) * params['size']).limit(
                params['size']).all()

            return {
                'current': params['current'],
                'size': params['size'],
                'list': [link.to_dict() for link in links],
                'total': total
            }
        except Exception as e:
            return None