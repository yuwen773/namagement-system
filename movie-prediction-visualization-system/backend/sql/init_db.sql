-- =====================================================
-- 电影票房预测与可视化系统 - 数据库初始化脚本
-- =====================================================
-- 创建数据库
CREATE DATABASE IF NOT EXISTS movie_prediction_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE movie_prediction_db;

-- =====================================================
-- 1. 用户表 (users)
-- =====================================================
DROP TABLE IF EXISTS boxoffice_records;
DROP TABLE IF EXISTS cinemas;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS regions;
DROP TABLE IF EXISTS movie_types;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    password VARCHAR(255) NOT NULL COMMENT '密码（加密存储）',
    real_name VARCHAR(50) COMMENT '真实姓名',
    email VARCHAR(100) COMMENT '邮箱',
    phone VARCHAR(20) COMMENT '联系电话',
    role VARCHAR(20) NOT NULL DEFAULT 'USER' COMMENT '角色：ADMIN-管理员, USER-普通用户',
    is_active TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否激活：1-是, 0-否',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 插入管理员用户（密码：admin123）
INSERT INTO users (username, password, real_name, email, role) VALUES
('admin', 'pbkdf2_sha256$720000$test$test', '系统管理员', 'admin@example.com', 'ADMIN'),
('superadmin', 'pbkdf2_sha256$720000$test$test', '超级管理员', 'superadmin@example.com', 'ADMIN');

-- 插入普通用户（密码：user123）
INSERT INTO users (username, password, real_name, email, role) VALUES
('zhangsan', 'pbkdf2_sha256$720000$test$test', '张三', 'zhangsan@example.com', 'USER'),
('lisi', 'pbkdf2_sha256$720000$test$test', '李四', 'lisi@example.com', 'USER'),
('wangwu', 'pbkdf2_sha256$720000$test$test', '王五', 'wangwu@example.com', 'USER');

-- =====================================================
-- 2. 影片类型表 (movie_types)
-- =====================================================
CREATE TABLE movie_types (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE COMMENT '类型名称',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='影片类型表';

-- 插入5个影片类型
INSERT INTO movie_types (name) VALUES
('动作'),
('科幻'),
('爱情'),
('喜剧'),
('动画');

-- =====================================================
-- 3. 影片表 (movies)
-- =====================================================
CREATE TABLE movies (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL COMMENT '影片名称',
    director VARCHAR(100) COMMENT '导演',
    actors VARCHAR(500) COMMENT '主演（多人用逗号分隔）',
    release_date DATE COMMENT '上映时间',
    duration INT COMMENT '片长（分钟）',
    type_id BIGINT COMMENT '类型ID',
    poster_url VARCHAR(500) COMMENT '海报URL',
    description TEXT COMMENT '简介',
    box_office_total DECIMAL(15,2) DEFAULT 0.00 COMMENT '累计票房（万元）',
    status VARCHAR(20) DEFAULT 'RELEASED' COMMENT '状态：RELEASED-已上映, COMING-即将上映, OFF-已下映',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (type_id) REFERENCES movie_types(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='影片表';

-- 插入10部影片
INSERT INTO movies (title, director, actors, release_date, duration, type_id, poster_url, description, box_office_total, status) VALUES
('流浪地球3', '郭帆', '吴京,刘德华,李雪健', '2026-02-06', 180, 2, 'https://example.com/poster1.jpg', '人类继续探索太阳系危机的故事', 0.00, 'RELEASED'),
('长津湖之水门桥', '陈凯歌', '吴京,易烊千玺,段奕宏', '2025-12-30', 150, 1, 'https://example.com/poster2.jpg', '抗美援朝战争史诗续作', 5200.00, 'RELEASED'),
('你好，李焕英', '贾玲', '贾玲,张小斐,沈腾', '2025-12-31', 128, 4, 'https://example.com/poster3.jpg', '穿越时空的温情喜剧', 3800.00, 'RELEASED'),
('复仇者联盟6', '凯文·费奇', '小罗伯特·唐尼,克里斯·埃文斯,斯嘉丽·约翰逊', '2026-05-01', 180, 2, 'https://example.com/poster4.jpg', '漫威宇宙最终篇章', 0.00, 'COMING'),
('满江红', '张艺谋', '沈腾,易烊千玺,张译', '2025-11-20', 140, 1, 'https://example.com/poster5.jpg', '南宋抗金英雄传奇', 4500.00, 'RELEASED'),
('熊出没·狂野大陆', '丁亮', '光头强,熊大,熊二', '2026-01-22', 95, 5, 'https://example.com/poster6.jpg', '光头强加入冒险之旅', 2800.00, 'RELEASED'),
('第二十条', '张艺谋', '雷佳音,马丽,赵丽颖', '2025-10-01', 130, 4, 'https://example.com/poster7.jpg', '法律与人情的抉择', 3200.00, 'RELEASED'),
('封神第二部', '乌尔善', '费翔,李雪健,陈坤', '2026-07-10', 160, 1, 'https://example.com/poster8.jpg', '封神演义神话史诗', 0.00, 'COMING'),
('爱情神话', '邵艺辉', '马伊琍,吴越,倪虹洁', '2025-12-08', 115, 3, 'https://example.com/poster9.jpg', '都市爱情轻喜剧', 1800.00, 'RELEASED'),
('飞驰人生2', '韩寒', '沈腾,尹正,张本煜', '2026-02-07', 125, 4, 'https://example.com/poster10.jpg', '赛车手重返赛场的故事', 0.00, 'RELEASED');

-- =====================================================
-- 4. 地域表 (regions)
-- =====================================================
CREATE TABLE regions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL COMMENT '地域名称（省份/城市）',
    parent_id BIGINT DEFAULT NULL COMMENT '父级ID（如果是城市则有父级省份）',
    level VARCHAR(20) DEFAULT 'PROVINCE' COMMENT '层级：PROVINCE-省份, CITY-城市',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (parent_id) REFERENCES regions(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='地域表';

-- 插入5个省份
INSERT INTO regions (name, level) VALUES
('北京市', 'PROVINCE'),
('上海市', 'PROVINCE'),
('广东省', 'PROVINCE'),
('江苏省', 'PROVINCE'),
('浙江省', 'PROVINCE');

-- =====================================================
-- 5. 影院表 (cinemas)
-- =====================================================
CREATE TABLE cinemas (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL COMMENT '影院名称',
    address VARCHAR(500) COMMENT '地址',
    phone VARCHAR(50) COMMENT '联系电话',
    region_id BIGINT COMMENT '所属区域ID',
    screen_count INT DEFAULT 1 COMMENT '屏幕数量',
    seats_count INT DEFAULT 100 COMMENT '座位数量',
    is_active TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否营业：1-是, 0-否',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (region_id) REFERENCES regions(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='影院表';

-- 插入8家影院
INSERT INTO cinemas (name, address, phone, region_id, screen_count, seats_count) VALUES
('北京万达影城CBD店', '北京市朝阳区建国路93号万达广场B座3层', '010-88888801', 1, 12, 2000),
('北京耀莱成龙影城', '北京市海淀区中关村大街18号科贸电子城5层', '010-88888802', 1, 10, 1800),
('上海万达影城五角场店', '上海市杨浦区政通路189号万达广场3层', '021-88888801', 2, 15, 2500),
('上海百丽宫影城环贸店', '上海市徐汇区淮海中路999号环贸广场6层', '021-88888802', 2, 8, 1200),
('广州飞扬影城正佳店', '广州市天河区天河路228号正佳广场7层', '020-88888801', 3, 10, 1600),
('深圳万象影城华润店', '深圳市南山区深南大道9668号万象天地', '020-88888802', 3, 12, 2000),
('南京万达影城新街口店', '南京市秦淮区中山南路49号新街口万达广场', '025-88888801', 4, 10, 1800),
('杭州百老汇影城万象城店', '杭州市江干区四季青街道富春路万象城', '0571-88888801', 5, 8, 1400);

-- =====================================================
-- 6. 票房记录表 (boxoffice_records)
-- =====================================================
CREATE TABLE boxoffice_records (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    movie_id BIGINT NOT NULL COMMENT '影片ID',
    cinema_id BIGINT NOT NULL COMMENT '影院ID',
    record_date DATE NOT NULL COMMENT '记录日期',
    daily_box_office DECIMAL(15,2) NOT NULL DEFAULT 0.00 COMMENT '当日票房（元）',
    screening_count INT NOT NULL DEFAULT 0 COMMENT '排片场次',
    audience_count INT NOT NULL DEFAULT 0 COMMENT '观影人次',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (movie_id) REFERENCES movies(id),
    FOREIGN KEY (cinema_id) REFERENCES cinemas(id),
    UNIQUE KEY unique_movie_cinema_date (movie_id, cinema_id, record_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='票房记录表';

-- 插入30条票房记录（覆盖3部影片，时间跨度7天）
-- 流浪地球3（movie_id=1）
INSERT INTO boxoffice_records (movie_id, cinema_id, record_date, daily_box_office, screening_count, audience_count) VALUES
(1, 1, '2026-02-04', 125000.00, 48, 3200),
(1, 2, '2026-02-04', 98000.00, 36, 2500),
(1, 3, '2026-02-04', 156000.00, 52, 4100),
(1, 4, '2026-02-04', 87000.00, 32, 2200),
(1, 5, '2026-02-04', 112000.00, 42, 2900),
(1, 6, '2026-02-04', 135000.00, 48, 3500),
(1, 7, '2026-02-04', 95000.00, 38, 2400),
(1, 8, '2026-02-04', 82000.00, 30, 2100),
(1, 1, '2026-02-05', 142000.00, 52, 3600),
(1, 2, '2026-02-05', 108000.00, 40, 2800),
(1, 3, '2026-02-05', 178000.00, 58, 4600),
(1, 4, '2026-02-05', 95000.00, 35, 2400),
(1, 1, '2026-02-06', 168000.00, 58, 4200),
(1, 2, '2026-02-06', 125000.00, 45, 3200),
(1, 3, '2026-02-06', 195000.00, 62, 5000),
(1, 4, '2026-02-06', 108000.00, 40, 2750),
(1, 1, '2026-02-07', 152000.00, 55, 3900),
(1, 2, '2026-02-07', 115000.00, 42, 2950),
(1, 3, '2026-02-07', 185000.00, 60, 4750),
(1, 4, '2026-02-07', 102000.00, 38, 2600),
(1, 5, '2026-02-07', 128000.00, 48, 3300),
(1, 6, '2026-02-07', 145000.00, 52, 3750),
(1, 7, '2026-02-07', 108000.00, 42, 2750),
(1, 8, '2026-02-07', 95000.00, 36, 2400);

-- 长津湖之水门桥（movie_id=2）
INSERT INTO boxoffice_records (movie_id, cinema_id, record_date, daily_box_office, screening_count, audience_count) VALUES
(2, 1, '2026-02-04', 85000.00, 32, 2100),
(2, 3, '2026-02-04', 112000.00, 42, 2800),
(2, 5, '2026-02-04', 78000.00, 28, 1950),
(2, 1, '2026-02-05', 92000.00, 35, 2280),
(2, 3, '2026-02-05', 125000.00, 46, 3100),
(2, 5, '2026-02-05', 85000.00, 31, 2100);

-- 你好，李焕英（movie_id=3）
INSERT INTO boxoffice_records (movie_id, cinema_id, record_date, daily_box_office, screening_count, audience_count) VALUES
(3, 1, '2026-02-04', 72000.00, 28, 1850),
(3, 3, '2026-02-04', 95000.00, 36, 2420),
(3, 6, '2026-02-04', 68000.00, 26, 1720),
(3, 1, '2026-02-05', 78000.00, 30, 1980),
(3, 3, '2026-02-05', 102000.00, 38, 2580);

-- =====================================================
-- 创建索引优化查询性能
-- =====================================================
CREATE INDEX idx_movies_type ON movies(type_id);
CREATE INDEX idx_movies_status ON movies(status);
CREATE INDEX idx_cinemas_region ON cinemas(region_id);
CREATE INDEX idx_boxoffice_movie_date ON boxoffice_records(movie_id, record_date);
CREATE INDEX idx_boxoffice_cinema_date ON boxoffice_records(cinema_id, record_date);
CREATE INDEX idx_boxoffice_date ON boxoffice_records(record_date);

-- =====================================================
-- 验证查询
-- =====================================================
-- SELECT '用户表' as table_name, COUNT(*) as count FROM users;
-- SELECT '影片类型表' as table_name, COUNT(*) as count FROM movie_types;
-- SELECT '影片表' as table_name, COUNT(*) as count FROM movies;
-- SELECT '地域表' as table_name, COUNT(*) as count FROM regions;
-- SELECT '影院表' as table_name, COUNT(*) as count FROM cinemas;
-- SELECT '票房记录表' as table_name, COUNT(*) as count FROM boxoffice_records;
