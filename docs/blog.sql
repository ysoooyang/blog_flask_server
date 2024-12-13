SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- 创建数据库
CREATE DATABASE IF NOT EXISTS online_blog CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE online_blog;

-- ----------------------------
-- Table structure for blog_article
-- ----------------------------
DROP TABLE IF EXISTS `blog_article`;
CREATE TABLE `blog_article` (
  `id` int NOT NULL AUTO_INCREMENT,
  `article_title` varchar(255) NOT NULL COMMENT '文章标题',
  `author_id` int NOT NULL DEFAULT '1' COMMENT '文章作者',
  `category_id` int NOT NULL COMMENT '分类id',
  `article_content` text COMMENT '文章内容',
  `article_cover` varchar(255) DEFAULT 'https://mrzym.gitee.io/blogimg/html/rabbit.png' COMMENT '文章缩略图',
  `is_top` tinyint DEFAULT '2' COMMENT '是否置顶 1 置顶 2 取消置顶',
  `status` tinyint DEFAULT '1' COMMENT '文章状态 1 公开 2 私密 3 草稿箱',
  `type` tinyint DEFAULT '1' COMMENT '文章类型 1 原创 2 转载 3 翻译',
  `origin_url` varchar(255) DEFAULT NULL COMMENT '原文链接',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `view_times` int DEFAULT '0' COMMENT '访问次数',
  `article_description` varchar(255) DEFAULT NULL COMMENT '描述信息',
  `thumbs_up_times` int DEFAULT '0' COMMENT '点赞次数',
  `reading_duration` double DEFAULT '0' COMMENT '阅读时长',
  `order` int DEFAULT NULL COMMENT '排序',
  PRIMARY KEY (`id`),
  INDEX `idx_author_category` (`author_id`, `category_id`),
  INDEX `idx_status_type` (`status`, `type`),
  INDEX `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for blog_article_tag
-- ----------------------------
DROP TABLE IF EXISTS `blog_article_tag`;
CREATE TABLE `blog_article_tag` (
  `id` int NOT NULL AUTO_INCREMENT,
  `article_id` int NOT NULL COMMENT '文章id',
  `tag_id` int NOT NULL COMMENT '标签id',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  INDEX `idx_article_tag` (`article_id`, `tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for blog_category
-- ----------------------------
DROP TABLE IF EXISTS `blog_category`;
CREATE TABLE `blog_category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(55) NOT NULL COMMENT '分类名称',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_category_name` (`category_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for blog_chat
-- ----------------------------
DROP TABLE IF EXISTS `blog_chat`;
CREATE TABLE `blog_chat` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL COMMENT '用户id',
  `content` varchar(555) DEFAULT NULL COMMENT '聊天内容',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `content_type` varchar(55) DEFAULT 'text' COMMENT '内容类型: text/image',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for blog_comment
-- ----------------------------
DROP TABLE IF EXISTS `blog_comment`;
CREATE TABLE `blog_comment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `parent_id` int DEFAULT NULL COMMENT '父评论id',
  `for_id` int NOT NULL COMMENT '评论对象id',
  `type` tinyint NOT NULL COMMENT '评论类型 1文章 2说说 3留言',
  `from_id` int NOT NULL COMMENT '评论人id',
  `from_name` varchar(255) NOT NULL COMMENT '评论人昵称',
  `from_avatar` varchar(555) DEFAULT NULL COMMENT '评论人头像',
  `to_id` int DEFAULT NULL COMMENT '被回复人id',
  `to_name` varchar(255) DEFAULT NULL COMMENT '被回复人昵称',
  `to_avatar` varchar(555) DEFAULT NULL COMMENT '被回复人头像',
  `content` varchar(555) NOT NULL COMMENT '评论内容',
  `thumbs_up` int DEFAULT '0' COMMENT '点赞数',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `ip` varchar(255) DEFAULT NULL COMMENT 'ip地址',
  PRIMARY KEY (`id`),
  INDEX `idx_type_for` (`type`, `for_id`),
  INDEX `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for blog_config
-- ----------------------------
DROP TABLE IF EXISTS `blog_config`;
CREATE TABLE `blog_config` (
  `id` int NOT NULL AUTO_INCREMENT,
  `blog_name` varchar(55) DEFAULT '小张的博客' COMMENT '博客名称',
  `blog_avatar` varchar(255) DEFAULT 'https://mrzym.gitee.io/blogimg/html/rabbit.png' COMMENT '博客头像',
  `avatar_bg` varchar(255) DEFAULT NULL COMMENT '头像背景图',
  `personal_say` varchar(255) DEFAULT NULL COMMENT '个性签名',
  `blog_notice` varchar(255) DEFAULT NULL COMMENT '博客公告',
  `qq_link` varchar(255) DEFAULT NULL COMMENT 'QQ链接',
  `we_chat_link` varchar(255) DEFAULT NULL COMMENT '微信链接',
  `github_link` varchar(255) DEFAULT NULL COMMENT 'Github链接',
  `git_ee_link` varchar(255) DEFAULT NULL COMMENT 'Gitee链接',
  `bilibili_link` varchar(255) DEFAULT NULL COMMENT 'B站链接',
  `view_time` bigint DEFAULT '0' COMMENT '访问次数',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `we_chat_group` varchar(255) DEFAULT NULL COMMENT '微信群二维码',
  `qq_group` varchar(255) DEFAULT NULL COMMENT 'QQ群二维码',
  `we_chat_pay` varchar(255) DEFAULT NULL COMMENT '微信收款码',
  `ali_pay` varchar(255) DEFAULT NULL COMMENT '支付宝收款码',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for blog_header
-- ----------------------------
DROP TABLE IF EXISTS `blog_header`;
CREATE TABLE `blog_header` (
  `id` int NOT NULL AUTO_INCREMENT,
  `bg_url` varchar(255) DEFAULT NULL COMMENT '背景图URL',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `route_name` varchar(555) DEFAULT NULL COMMENT '路由名称',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for blog_like
-- ----------------------------
DROP TABLE IF EXISTS `blog_like`;
CREATE TABLE `blog_like` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type` tinyint NOT NULL COMMENT '点赞类型 1文章 2说说 3留言 4评论',
  `for_id` int NOT NULL COMMENT '点赞对象id',
  `user_id` int NOT NULL COMMENT '点赞用户id',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `ip` varchar(255) DEFAULT NULL COMMENT '点赞IP',
  PRIMARY KEY (`id`),
  INDEX `idx_type_for_user` (`type`, `for_id`, `user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for blog_links
-- ----------------------------
DROP TABLE IF EXISTS `blog_links`;
CREATE TABLE `blog_links` (
  `id` int NOT NULL AUTO_INCREMENT,
  `site_name` varchar(55) NOT NULL COMMENT '网站名称',
  `site_desc` varchar(255) DEFAULT NULL COMMENT '网站描述',
  `site_avatar` varchar(555) DEFAULT NULL COMMENT '网站图标',
  `url` varchar(255) NOT NULL COMMENT '网站地址',
  `status` tinyint DEFAULT '1' COMMENT '状态 1待审核 2通过',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `user_id` int DEFAULT NULL COMMENT '申请用户id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for blog_message
-- ----------------------------
DROP TABLE IF EXISTS `blog_message`;
CREATE TABLE `blog_message` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tag` varchar(255) DEFAULT NULL COMMENT '标签',
  `message` varchar(555) NOT NULL COMMENT '留言内容',
  `color` varchar(255) DEFAULT '#676767' COMMENT '字体颜色',
  `font_size` tinyint DEFAULT '12' COMMENT '字体大小',
  `bg_color` varchar(255) DEFAULT NULL COMMENT '背景颜色',
  `bg_url` varchar(255) DEFAULT NULL COMMENT '背景图片',
  `user_id` int DEFAULT NULL COMMENT '用户id',
  `like_times` int DEFAULT '0' COMMENT '点赞次数',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `font_weight` int DEFAULT '500' COMMENT '字体粗细',
  `nick_name` varchar(255) DEFAULT NULL COMMENT '昵称',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for blog_notify
-- ----------------------------
DROP TABLE IF EXISTS `blog_notify`;
CREATE TABLE `blog_notify` (
  `id` int NOT NULL AUTO_INCREMENT,
  `message` varchar(555) NOT NULL COMMENT '通知内容',
  `user_id` int NOT NULL COMMENT '通知用户id',
  `type` tinyint NOT NULL COMMENT '类型 1文章 2说说 3留言 4友链',
  `to_id` int DEFAULT NULL COMMENT '跳转id',
  `is_view` tinyint DEFAULT '1' COMMENT '是否查看 1未读 2已读',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  INDEX `idx_user_view` (`user_id`, `is_view`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for blog_photo
-- ----------------------------
DROP TABLE IF EXISTS `blog_photo`;
CREATE TABLE `blog_photo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `album_id` int NOT NULL COMMENT '相册id',
  `url` varchar(555) NOT NULL COMMENT '图片地址',
  `status` tinyint DEFAULT '1' COMMENT '状态 1正常 2回收站',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  INDEX `idx_album_status` (`album_id`, `status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for blog_photo_album
-- ----------------------------
DROP TABLE IF EXISTS `blog_photo_album`;
CREATE TABLE `blog_photo_album` (
  `id` int NOT NULL AUTO_INCREMENT,
  `album_name` varchar(26) NOT NULL COMMENT '相册名称',
  `description` varchar(55) DEFAULT NULL COMMENT '相册描述',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `album_cover` varchar(555) DEFAULT NULL COMMENT '相册封面',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for blog_recommend
-- ----------------------------
DROP TABLE IF EXISTS `blog_recommend`;
CREATE TABLE `blog_recommend` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(55) NOT NULL COMMENT '推荐标题',
  `link` varchar(255) NOT NULL COMMENT '推荐链接',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for blog_tag
-- ----------------------------
DROP TABLE IF EXISTS `blog_tag`;
CREATE TABLE `blog_tag` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tag_name` varchar(55) NOT NULL COMMENT '标签名称',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_tag_name` (`tag_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for blog_talk
-- ----------------------------
DROP TABLE IF EXISTS `blog_talk`;
CREATE TABLE `blog_talk` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '用户id',
  `content` varchar(255) NOT NULL COMMENT '说说内容',
  `status` tinyint DEFAULT '1' COMMENT '状态 1公开 2私密 3回收站',
  `is_top` tinyint DEFAULT '2' COMMENT '是否置顶 1置顶 2不置顶',
  `like_times` int DEFAULT '0' COMMENT '点赞次数',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  INDEX `idx_user_status` (`user_id`, `status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for blog_talk_photo
-- ----------------------------
DROP TABLE IF EXISTS `blog_talk_photo`;
CREATE TABLE `blog_talk_photo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `talk_id` int NOT NULL COMMENT '说说id',
  `url` varchar(255) NOT NULL COMMENT '图片地址',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  INDEX `idx_talk_id` (`talk_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for blog_user
-- ----------------------------
DROP TABLE IF EXISTS `blog_user`;
CREATE TABLE `blog_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL COMMENT '账号',
  `password` char(64) NOT NULL COMMENT '密码',
  `role` tinyint NOT NULL DEFAULT '2' COMMENT '角色 1管理员 2普通用户',
  `nick_name` varchar(255) DEFAULT '' COMMENT '昵称',
  `avatar` varchar(255) DEFAULT '' COMMENT '头像',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `qq` varchar(255) DEFAULT '' COMMENT 'QQ号',
  `ip` varchar(255) DEFAULT '' COMMENT 'IP地址',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;