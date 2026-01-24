-- Enterprise HRMS Database Schema
-- Created: 2024-01-23

-- 创建数据库
CREATE DATABASE IF NOT EXISTS hrms_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE hrms_db;

-- 默认表将由 Django migrations 自动创建
-- 此脚本仅用于初始化数据库
