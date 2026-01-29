/*
    菜谱数据分析系统 - 数据库初始化脚本
    数据库类型: MySQL
    适用版本: 8.0+
*/

CREATE DATABASE IF NOT EXISTS recipe_analysis_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE recipe_analysis_db;

-- 1. 用户主表
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `username` VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    `password` VARCHAR(255) NOT NULL COMMENT '加密后的密码',
    `email` VARCHAR(100) UNIQUE COMMENT '邮箱',
    `role` ENUM('admin', 'user') DEFAULT 'user' COMMENT '角色: 管理员/普通用户',
    `status` TINYINT DEFAULT 1 COMMENT '状态: 1-启用, 0-禁用',
    `last_login` DATETIME DEFAULT NULL COMMENT '最后登录时间',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB COMMENT='用户主表';

-- 2. 用户信息扩展表
CREATE TABLE IF NOT EXISTS `user_profiles` (
    `user_id` INT PRIMARY KEY COMMENT '关联用户ID',
    `nickname` VARCHAR(50) COMMENT '昵称',
    `avatar` VARCHAR(255) COMMENT '头像URL',
    `bio` TEXT COMMENT '个人简介',
    `gender` TINYINT DEFAULT 0 COMMENT '性别: 0-未知, 1-男, 2-女',
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB COMMENT='用户信息扩展表';

-- 3. 菜谱分类表
CREATE TABLE IF NOT EXISTS `categories` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `name` VARCHAR(50) NOT NULL COMMENT '分类名称',
    `parent_id` INT DEFAULT NULL COMMENT '父分类ID',
    `level` TINYINT DEFAULT 1 COMMENT '层级',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB COMMENT='菜谱分类表';

-- 4. 食材库表
CREATE TABLE IF NOT EXISTS `ingredients` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `name` VARCHAR(100) NOT NULL UNIQUE COMMENT '食材名称',
    `description` TEXT COMMENT '食材描述/营养价值',
    `category` VARCHAR(50) COMMENT '食材分类',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB COMMENT='食材资料管理表';

-- 5. 菜谱主表
CREATE TABLE IF NOT EXISTS `recipes` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `title` VARCHAR(255) NOT NULL COMMENT '菜谱标题',
    `cover_image` VARCHAR(255) COMMENT '成品图URL',
    `description` TEXT COMMENT '菜谱描述',
    `difficulty` ENUM('easy', 'medium', 'hard') DEFAULT 'medium' COMMENT '难度等级',
    `taste` VARCHAR(50) COMMENT '口味标签',
    `cooking_time` INT COMMENT '烹饪时长(分钟)',
    `category_id` INT COMMENT '所属分类',
    `view_count` INT DEFAULT 0 COMMENT '浏览次数',
    `collect_count` INT DEFAULT 0 COMMENT '收藏次数',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_category` (`category_id`),
    INDEX `idx_difficulty` (`difficulty`),
    FOREIGN KEY (`category_id`) REFERENCES `categories`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB COMMENT='菜谱主数据表';

-- 6. 菜谱-食材关联表
CREATE TABLE IF NOT EXISTS `recipe_ingredients` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `recipe_id` INT NOT NULL COMMENT '关联菜谱ID',
    `ingredient_id` INT NOT NULL COMMENT '关联食材ID',
    `quantity` VARCHAR(50) COMMENT '用量/单位',
    `is_main` TINYINT DEFAULT 1 COMMENT '是否为主料: 1-是, 0-辅料',
    FOREIGN KEY (`recipe_id`) REFERENCES `recipes`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`ingredient_id`) REFERENCES `ingredients`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB COMMENT='菜谱-食材关联表';

-- 7. 菜谱步骤表
CREATE TABLE IF NOT EXISTS `recipe_steps` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `recipe_id` INT NOT NULL COMMENT '关联菜谱ID',
    `step_number` TINYINT NOT NULL COMMENT '步骤序号',
    `content` TEXT NOT NULL COMMENT '步骤描述',
    `image` VARCHAR(255) COMMENT '步骤图URL',
    FOREIGN KEY (`recipe_id`) REFERENCES `recipes`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB COMMENT='菜谱烹饪步骤表';

-- 8. 用户收藏表
CREATE TABLE IF NOT EXISTS `user_favorites` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL COMMENT '用户ID',
    `recipe_id` INT NOT NULL COMMENT '菜谱ID',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY `uk_user_recipe` (`user_id`, `recipe_id`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`recipe_id`) REFERENCES `recipes`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB COMMENT='用户收藏关联表';

-- 9. 用户行为日志表 (核心分析数据源)
CREATE TABLE IF NOT EXISTS `user_behavior_logs` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT COMMENT '用户ID(游客可为空)',
    `action_type` ENUM('login', 'view', 'search', 'collect', 'share') NOT NULL COMMENT '行为类型',
    `target_id` INT COMMENT '行为目标ID(如菜谱ID)',
    `search_keyword` VARCHAR(255) COMMENT '搜索关键词',
    `duration` INT DEFAULT 0 COMMENT '停留时长(秒)',
    `ip_address` VARCHAR(45) COMMENT 'IP地址',
    `user_agent` TEXT COMMENT '浏览器/设备信息',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_action_time` (`action_type`, `created_at`),
    INDEX `idx_user_action` (`user_id`, `action_type`)
) ENGINE=InnoDB COMMENT='用户行为分析原始日志表';
