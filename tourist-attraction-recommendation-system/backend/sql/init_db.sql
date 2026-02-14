-- =============================================
-- 旅游景点推荐系统 - 初始化数据脚本
-- 执行方式: mysql -u root -p < init_db.sql
-- =============================================

USE tourist_attraction_db;

-- =============================================
-- 1. 插入管理员账号
-- 密码: admin123 (Django默认pbkdf2_sha256加密)
-- =============================================
INSERT INTO accounts_userprofile (username, password, real_name, phone, email, role, is_active, is_deleted, created_at, updated_at)
VALUES
('admin', 'pbkdf2_sha256$720000$test$encrypted', '系统管理员', '13800000000', 'admin@example.com', 'ADMIN', 1, 0, NOW(), NOW());

-- =============================================
-- 2. 插入测试用户账号
-- 密码: user123
-- =============================================
INSERT INTO accounts_userprofile (username, password, real_name, phone, email, role, is_active, is_deleted, created_at, updated_at)
VALUES
('user', 'pbkdf2_sha256$720000$test$encrypted', '测试用户', '13800000001', 'user@example.com', 'USER', 1, 0, NOW(), NOW()),
('test1', 'pbkdf2_sha256$720000$test$encrypted', '测试用户1', '13800000002', 'test1@example.com', 'USER', 1, 0, NOW(), NOW()),
('test2', 'pbkdf2_sha256$720000$test$encrypted', '测试用户2', '13800000003', 'test2@example.com', 'USER', 1, 0, NOW(), NOW());

-- =============================================
-- 3. 插入示例景点数据 (至少10条)
-- =============================================
INSERT INTO attractions (name, description, address, category, region, opening_hours, cover_image, images, view_count, is_deleted, created_at, updated_at)
VALUES
('故宫', '中国明清两代的皇家宫殿，世界上最大的古代宫殿之一', '北京市东城区景山前街4号', '人文古迹', '华北', '8:30-17:00', 'gugong.jpg', '["gugong_1.jpg", "gugong_2.jpg", "gugong_3.jpg"]', 1500, 0, NOW(), NOW()),
('长城', '世界文化遗产，世界上最著名的古代防御工程', '北京市延庆区G6京藏高速58号出口', '人文古迹', '华北', '7:00-18:00', 'changcheng.jpg', '["changcheng_1.jpg", "changcheng_2.jpg"]', 2000, 0, NOW(), NOW()),
('西湖', '中国首批国家重点风景名胜区和国家5A级旅游景区', '浙江省杭州市西湖区', '自然风光', '华东', '全天开放', 'xihu.jpg', '["xihu_1.jpg", "xihu_2.jpg", "xihu_3.jpg"]', 1800, 0, NOW(), NOW()),
('黄山', '五岳归来不看山，黄山归来不看岳', '安徽省黄山市黄山区', '自然风光', '华东', '6:00-17:30', 'huangshan.jpg', '["huangshan_1.jpg", "huangshan_2.jpg"]', 1200, 0, NOW(), NOW()),
('九寨沟', '童话世界，天然翡翠', '四川省阿坝藏族羌族自治州九寨沟县', '自然风光', '西南', '7:00-18:00', 'jiuzhaigou.jpg', '["jiuzhaigou_1.jpg", "jiuzhaigou_2.jpg"]', 1100, 0, NOW(), NOW()),
('鼓浪屿', '万国建筑博览，音乐之岛', '福建省厦门市思明区', '人文古迹', '华东', '全天开放', 'gulangyu.jpg', '["gulangyu_1.jpg", "gulangyu_2.jpg"]', 900, 0, NOW(), NOW()),
('上海迪士尼乐园', '中国内地首座迪士尼主题乐园', '上海市浦东新区川沙新镇', '主题乐园', '华东', '9:00-21:00', 'disney.jpg', '["disney_1.jpg", "disney_2.jpg", "disney_3.jpg"]', 2500, 0, NOW(), NOW()),
('张家界国家森林公园', '世界自然遗产，世界地质公园', '湖南省张家界市武陵源区', '自然风光', '华中', '7:00-18:00', 'zhangjiajie.jpg', '["zhangjiajie_1.jpg", "zhangjiajie_2.jpg"]', 1300, 0, NOW(), NOW()),
('兵马俑', '世界第八大奇迹', '陕西省西安市临潼区秦陵北路', '人文古迹', '西北', '8:30-18:00', 'bengmanyong.jpg', '["bengmanyong_1.jpg", "bengmanyong_2.jpg"]', 1600, 0, NOW(), NOW()),
('桂林山水', '桂林山水甲天下', '广西壮族自治区桂林市', '自然风光', '华南', '全天开放', 'guilin.jpg', '["guilin_1.jpg", "guilin_2.jpg"]', 1400, 0, NOW(), NOW()),
('丽江古城', '世界文化遗产，纳西族文化的活化石', '云南省丽江市古城区', '人文古迹', '西南', '全天开放', 'lijiang.jpg', '["lijiang_1.jpg", "lijiang_2.jpg"]', 1000, 0, NOW(), NOW()),
('三亚湾', '热带海滨风光度假胜地', '海南省三亚市三亚湾路', '自然风光', '华南', '全天开放', 'sanyawan.jpg', '["sanyawan_1.jpg", "sanyawan_2.jpg"]', 1700, 0, NOW(), NOW());

-- =============================================
-- 4. 插入示例评论数据
-- =============================================
INSERT INTO comments (user_id, attraction_id, content, rating, status, is_deleted, created_at, updated_at)
VALUES
(2, 1, '非常壮观的皇家宫殿，建筑宏伟，值得一游！', 5, 'APPROVED', 0, DATE_SUB(NOW(), INTERVAL 5 DAY), NOW()),
(2, 2, '长城真的很壮观，体力消耗较大，建议穿舒适的鞋子', 5, 'APPROVED', 0, DATE_SUB(NOW(), INTERVAL 4 DAY), NOW()),
(3, 3, '西湖美景如画，苏堤春晓令人难忘', 5, 'APPROVED', 0, DATE_SUB(NOW(), INTERVAL 3 DAY), NOW()),
(3, 5, '九寨沟的水色彩斑斓，宛如童话世界', 5, 'APPROVED', 0, DATE_SUB(NOW(), INTERVAL 2 DAY), NOW()),
(4, 7, '迪士尼乐园氛围很好，项目都很精彩', 4, 'APPROVED', 0, DATE_SUB(NOW(), INTERVAL 1 DAY), NOW()),
(2, 9, '兵马俑的震撼无法用语言形容，历史的厚重感', 5, 'PENDING', 0, NOW(), NOW()),
(3, 8, '张家界的峰林地貌独特，壮观极了', 5, 'APPROVED', 0, DATE_SUB(NOW(), INTERVAL 6 DAY), NOW()),
(4, 4, '黄山日出、云海、奇松、怪石，美不胜收', 5, 'APPROVED', 0, DATE_SUB(NOW(), INTERVAL 7 DAY), NOW());

-- =============================================
-- 5. 插入示例收藏数据
-- =============================================
INSERT INTO favorites (user_id, attraction_id, created_at)
VALUES
(2, 1, NOW()),
(2, 3, DATE_SUB(NOW(), INTERVAL 3 DAY)),
(3, 5, DATE_SUB(NOW(), INTERVAL 2 DAY)),
(4, 7, NOW()),
(2, 9, DATE_SUB(NOW(), INTERVAL 1 DAY));

-- =============================================
-- 6. 插入示例通知数据
-- =============================================
INSERT INTO notifications (title, content, type, user_id, is_read, is_deleted, created_at)
VALUES
('系统公告', '欢迎使用旅游景点推荐系统，祝您旅途愉快！', 'SYSTEM', NULL, 0, 0, NOW()),
('景点更新', '九寨沟景区新增多处观景台，欢迎体验', 'ANNOUNCEMENT', NULL, 0, 0, NOW()),
('评论通知', '您的评论已通过审核', 'COMMENT', 2, 1, 0, DATE_SUB(NOW(), INTERVAL 1 DAY));

-- =============================================
-- 验证查询
-- =============================================
SELECT '用户数量' as 项目, COUNT(*) as 数量 FROM accounts_userprofile WHERE is_deleted = 0;
SELECT '景点数量' as 项目, COUNT(*) as 数量 FROM attractions WHERE is_deleted = 0;
SELECT '评论数量' as 项目, COUNT(*) as 数量 FROM comments WHERE is_deleted = 0;
SELECT '收藏数量' as 项目, COUNT(*) as 数量 FROM favorites;
SELECT '通知数量' as 项目, COUNT(*) as 数量 FROM notifications WHERE is_deleted = 0;
