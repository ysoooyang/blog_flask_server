from datetime import datetime
from sqlalchemy import desc
from app.extensions.extensions import db
from app.models.article import Article
from app.services.article_tag_service import ArticleTagService
from app.services.category_service import CategoryService
from app.services.user_service import UserService


class ArticleService:
    @staticmethod
    def create_article(article_data):
        """新增文章"""
        try:
            now = datetime.now()
            article = Article(
                created_at=now,
                updated_at=now,
                **article_data
            )
            db.session.add(article)
            db.session.commit()
            return article.to_dict()
        except Exception as e:
            db.session.rollback()
            return None

    @staticmethod
    def update_article(article_data):
        """修改文章信息"""
        try:
            article = Article.query.get(article_data['id'])
            if not article:
                return False

            article_data['updated_at'] = datetime.now()
            for key, value in article_data.items():
                setattr(article, key, value)

            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False

    @staticmethod
    def update_top(id, is_top):
        """修改文章置顶信息"""
        try:
            article = Article.query.get(id)
            if not article:
                return False

            article.is_top = is_top
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False

    @staticmethod
    def delete_article(id, status):
        """删除文章"""
        try:
            if status != 3:
                article = Article.query.get(id)
                if not article:
                    return False

                article.status = 3
                db.session.commit()
                return True
            else:
                Article.query.filter_by(id=id).delete()
                ArticleTagService.delete_article_tag(id)
                db.session.commit()
                return True
        except Exception as e:
            db.session.rollback()
            return False

    @staticmethod
    def revert_article(id):
        """恢复文章"""
        try:
            article = Article.query.get(id)
            if not article:
                return False

            article.status = 1
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False

    @staticmethod
    def toggle_article_public(id, status):
        """公开或隐藏文章"""
        try:
            article = Article.query.get(id)
            if not article:
                return False

            article.status = 1 if status == 2 else 2
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False

    @staticmethod
    def get_article_info_by_title(id, article_title):
        """根据文章标题获取文章信息"""
        article = Article.query.filter_by(article_title=article_title).first()
        if article:
            if id:
                return article.id != id
            return True
        return False

    @staticmethod
    def get_article_list(params):
        """条件分页查询文章列表"""
        current = params.get('current', 1)
        size = params.get('size', 10)
        article_title = params.get('article_title')
        is_top = params.get('is_top')
        status = params.get('status')
        tag_id = params.get('tag_id')
        category_id = params.get('category_id')
        create_time = params.get('create_time')

        query = Article.query

        # 添加查询条件
        if article_title:
            query = query.filter(Article.article_title.like(f'%{article_title}%'))
        if create_time:
            query = query.filter(Article.created_at.between(*create_time))
        if is_top:
            query = query.filter_by(is_top=is_top)
        if status:
            query = query.filter_by(status=status)
        elif not status:
            query = query.filter(Article.status.in_([1, 2]))
        if category_id:
            query = query.filter_by(category_id=category_id)
        if tag_id:
            article_ids = ArticleTagService.get_article_id_list_by_tag_id(tag_id)
            if article_ids:
                query = query.filter(Article.id.in_(article_ids))

        # 分页
        total = query.count()
        articles = query.order_by(desc(Article.created_at)) \
            .offset((current - 1) * size) \
            .limit(size) \
            .all()

        # 获取文章的分类名称和标签
        result_list = []
        for article in articles:
            article_dict = article.to_dict(exclude=['article_content', 'origin_url'])
            article_dict['categoryName'] = CategoryService.get_category_name_by_id(article.category_id)
            tag_info = ArticleTagService.get_tag_list_by_article_id(article.id)
            article_dict['tagNameList'] = tag_info['tagNameList']
            result_list.append(article_dict)

        return {
            'current': current,
            'size': size,
            'total': total,
            'list': result_list
        }

    @staticmethod
    def get_article_by_id(id):
        """根据文章id获取文章详细信息"""
        article = Article.query.get(id)
        if not article:
            return None

        # 增加浏览次数
        article.view_times += 1
        db.session.commit()

        # 获取标签列表
        tag_info = ArticleTagService.get_tag_list_by_article_id(id)

        # 获取分类名称
        category_name = CategoryService.get_category_name_by_id(article.category_id)

        # 获取作者昵称
        author_name = UserService.get_author_name_by_id(article.author_id)

        article_dict = article.to_dict()
        article_dict.update({
            'tagIdList': tag_info['tagIdList'],
            'tagNameList': tag_info['tagNameList'],
            'authorName': author_name,
            'categoryName': category_name
        })

        return article_dict

    @staticmethod
    def blog_home_get_article_list(current, size):
        """博客前台获取文章列表"""
        query = Article.query.filter_by(status=1)
        total = query.count()

        articles = query.order_by(
            Article.is_top.asc(),
            Article.order.asc(),
            Article.created_at.desc()
        ).offset((current - 1) * size).limit(size).all()

        result_list = []
        for article in articles:
            article_dict = article.to_dict(exclude=['article_content', 'origin_url'])
            article_dict['categoryName'] = CategoryService.get_category_name_by_id(article.category_id)
            tag_info = ArticleTagService.get_tag_list_by_article_id(article.id)
            article_dict['tagNameList'] = tag_info['tagNameList']
            result_list.append(article_dict)

        return {
            'current': current,
            'size': size,
            'total': total,
            'list': result_list
        }

    @staticmethod
    def blog_timeline_get_article_list(current, size):
        """时间轴列表"""
        query = Article.query.filter_by(status=1)
        total = query.count()

        articles = query.order_by(Article.created_at.desc()) \
            .offset((current - 1) * size) \
            .limit(size) \
            .all()

        # 按年份分组
        result_dict = {}
        for article in articles:
            year = article.created_at.strftime('%Y')
            if year not in result_dict:
                result_dict[year] = []
            result_dict[year].append(article.to_dict(
                only=['id', 'article_title', 'article_cover', 'created_at']
            ))

        # 转换为列表格式
        result_list = [
            {'year': year, 'articleList': articles}
            for year, articles in result_dict.items()
        ]

        return {
            'current': current,
            'size': size,
            'total': total,
            'list': result_list
        }

    @staticmethod
    def get_article_list_by_tag_id(current, size, tag_id):
        """通过tagId获取文章列表"""
        article_ids = ArticleTagService.get_article_id_list_by_tag_id(tag_id)
        if not article_ids:
            return {
                'current': current,
                'size': size,
                'total': 0,
                'list': []
            }

        query = Article.query.filter(
            Article.id.in_(article_ids),
            Article.status == 1
        )

        total = query.count()
        articles = query.order_by(Article.created_at.desc()) \
            .offset((current - 1) * size) \
            .limit(size) \
            .all()

        result_list = [
            article.to_dict(only=['id', 'article_title', 'article_cover', 'created_at'])
            for article in articles
        ]

        return {
            'current': current,
            'size': size,
            'total': total,
            'list': result_list
        }

    @staticmethod
    def get_article_list_by_category_id(current, size, category_id):
        """通过分类id获取文章列表"""
        query = Article.query.filter_by(
            category_id=category_id,
            status=1
        )

        total = query.count()
        articles = query.order_by(Article.created_at.desc()) \
            .offset((current - 1) * size) \
            .limit(size) \
            .all()

        result_list = [
            article.to_dict(only=['id', 'article_title', 'article_cover', 'created_at'])
            for article in articles
        ]

        return {
            'current': current,
            'size': size,
            'total': total,
            'list': result_list
        }

    @staticmethod
    def get_recommend_article_by_id(article_id):
        """根据文章id获取推荐文章"""
        # 获取上一篇文章
        previous = Article.query.filter(
            Article.id < article_id,
            Article.status == 1
        ).order_by(Article.id.desc()).first()

        # 获取下一篇文章
        next_article = Article.query.filter(
            Article.id > article_id,
            Article.status == 1
        ).order_by(Article.id.asc()).first()

        # 如果不存在上一篇或下一篇，使用当前文章
        if not previous:
            previous = Article.query.get(article_id)
        if not next_article:
            next_article = Article.query.get(article_id)

        # 获取相关标签的文章推荐
        tag_info = ArticleTagService.get_tag_list_by_article_id(article_id)
        tag_ids = tag_info['tagIdList']
        article_ids = []
        for tag_id in tag_ids:
            ids = ArticleTagService.get_article_id_list_by_tag_id(tag_id)
            if ids:
                article_ids.extend(ids)

        # 获取推荐文章
        recommend = Article.query.filter(
            Article.id.in_(set(article_ids)),
            Article.status == 1
        ).order_by(Article.created_at.desc()).limit(6).all()

        return {
            'previous': previous.to_dict(only=['id', 'article_title', 'article_cover']),
            'next': next_article.to_dict(only=['id', 'article_title', 'article_cover']),
            'recommend': [
                article.to_dict(only=['id', 'article_title', 'article_cover', 'created_at'])
                for article in recommend
            ]
        }

    @staticmethod
    def get_article_count():
        """获取文章总数"""
        return Article.query.filter_by(status=1).count()

    @staticmethod
    def get_article_list_by_content(content):
        """根据文章内容搜索文章"""
        articles = Article.query.filter(
            Article.article_content.like(f'%{content}%'),
            Article.status == 1
        ).order_by(Article.view_times.desc()).limit(8).all()

        result_list = []
        for article in articles:
            article_content = article.article_content
            index = article_content.find(content)
            previous = index
            next_index = index + len(content) + 12

            result_list.append({
                'id': article.id,
                'article_content': article_content[previous:next_index],
                'article_title': article.article_title
            })

        return result_list

    @staticmethod
    def get_hot_article():
        """获取热门文章"""
        articles = Article.query.filter_by(status=1) \
            .order_by(Article.view_times.desc()) \
            .limit(5) \
            .all()

        return [
            article.to_dict(only=['id', 'article_title', 'view_times'])
            for article in articles
        ]

    @staticmethod
    def article_like(id):
        """文章点赞"""
        article = Article.query.get(id)
        if article:
            article.thumbs_up_times += 1
            db.session.commit()
            return True
        return False

    @staticmethod
    def cancel_article_like(id):
        """取消文章点赞"""
        article = Article.query.get(id)
        if article:
            article.thumbs_up_times -= 1
            db.session.commit()
            return True
        return False

    @staticmethod
    def add_reading_duration(id, duration):
        """文章增加阅读时长"""
        article = Article.query.get(id)
        if article:
            article.reading_duration += duration
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_article_cover_by_id(id):
        """根据文章获取文章封面"""
        article = Article.query.get(id)
        return article.article_cover if article else None
