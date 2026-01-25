/*
 Navicat Premium Dump SQL

 Source Server         : localhost@mysql-8.0.26
 Source Server Type    : MySQL
 Source Server Version : 80026 (8.0.26)
 Source Host           : localhost:3307
 Source Schema         : hrms_db

 Target Server Type    : MySQL
 Target Server Version : 80026 (8.0.26)
 File Encoding         : 65001

 Date: 25/01/2026 19:42:46
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for accounts_rolepermission
-- ----------------------------
DROP TABLE IF EXISTS `accounts_rolepermission`;
CREATE TABLE `accounts_rolepermission`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `role` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `menu_permissions` json NOT NULL,
  `button_permissions` json NOT NULL,
  `data_permission` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `attendance_permission` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `salary_permission` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `can_access_datacenter` tinyint(1) NOT NULL,
  `can_access_performance` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `role`(`role` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of accounts_rolepermission
-- ----------------------------
INSERT INTO `accounts_rolepermission` VALUES (1, 'employee', '[\"employeeDashboard\", \"profile\", \"departments\", \"posts\", \"attendance\", \"approval\", \"salary\", \"myPerformance\", \"notices\"]', '[\"checkIn\", \"checkOut\", \"applyLeave\", \"applyOvertime\", \"viewSalary\"]', 'self', 'self', 'self', 0, 1, '2026-01-25 06:18:05.928470', '2026-01-25 11:18:10.864077');
INSERT INTO `accounts_rolepermission` VALUES (2, 'hr', '[\"dashboard\", \"employees\", \"departments\", \"posts\", \"onboarding\", \"resignation\", \"attendance\", \"approval\", \"salary\", \"salaryException\", \"performanceReview\", \"performanceTemplate\", \"notices\"]', '[\"createEmployee\", \"editEmployee\", \"deleteEmployee\", \"approveLeave\", \"approveOvertime\", \"calculateSalary\", \"publishSalary\", \"createNotice\"]', 'all', 'all', 'all', 1, 1, '2026-01-25 06:18:05.931487', '2026-01-25 11:18:10.865077');
INSERT INTO `accounts_rolepermission` VALUES (3, 'admin', '[\"dashboard\", \"users\", \"permissionConfig\", \"securityConfig\", \"dataCenter\", \"noticeManagement\", \"salaryException\", \"profile\"]', '[\"manageUsers\", \"resetPassword\", \"configurePermissions\", \"viewSalary\"]', 'all', 'all', 'all', 1, 1, '2026-01-25 06:18:05.934544', '2026-01-25 11:18:10.867459');

-- ----------------------------
-- Table structure for accounts_systemconfig
-- ----------------------------
DROP TABLE IF EXISTS `accounts_systemconfig`;
CREATE TABLE `accounts_systemconfig`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `require_registration_approval` tinyint(1) NOT NULL,
  `password_min_length` int UNSIGNED NOT NULL,
  `password_require_uppercase` tinyint(1) NOT NULL,
  `password_require_lowercase` tinyint(1) NOT NULL,
  `password_require_number` tinyint(1) NOT NULL,
  `password_require_special` tinyint(1) NOT NULL,
  `max_login_attempts` int UNSIGNED NOT NULL,
  `login_lockout_duration` int UNSIGNED NOT NULL,
  `session_timeout` int UNSIGNED NOT NULL,
  `allow_multiple_sessions` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  CONSTRAINT `accounts_systemconfig_chk_1` CHECK (`password_min_length` >= 0),
  CONSTRAINT `accounts_systemconfig_chk_2` CHECK (`max_login_attempts` >= 0),
  CONSTRAINT `accounts_systemconfig_chk_3` CHECK (`login_lockout_duration` >= 0),
  CONSTRAINT `accounts_systemconfig_chk_4` CHECK (`session_timeout` >= 0)
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of accounts_systemconfig
-- ----------------------------
INSERT INTO `accounts_systemconfig` VALUES (1, 0, 6, 0, 1, 1, 0, 5, 30, 120, 1, '2026-01-25 09:38:48.100085', '2026-01-25 09:41:45.061112');

-- ----------------------------
-- Table structure for accounts_user
-- ----------------------------
DROP TABLE IF EXISTS `accounts_user`;
CREATE TABLE `accounts_user`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `phone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `real_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE,
  UNIQUE INDEX `phone`(`phone` ASC) USING BTREE,
  UNIQUE INDEX `email`(`email` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 101 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of accounts_user
-- ----------------------------
INSERT INTO `accounts_user` VALUES (1, 'pbkdf2_sha256$1000000$8Sc2LuIb1jGR2f7nweasNd$Td4h4FnAfZzUTcZ+9axtZZxRWgPV5WY1WY6QDtG0JqA=', '2026-01-24 16:10:19.000000', 1, 'admin', '', '', 1, 1, '2024-01-01 00:00:00.000000', '18199987365', 'admin', '系统管理员', 'admin@hrms.com');
INSERT INTO `accounts_user` VALUES (2, 'pbkdf2_sha256$1000000$lDNodM8tMbW3RLVSajVdl8$QMcvAzSPhPPYUf9s/7MjW1UdqYMSm/z9Oi8VwMIYzB8=', '2026-01-24 16:10:19.000000', 0, 'hr001', '', '', 1, 1, '2024-01-15 00:00:00.000000', '13800000002', 'hr', '张人事', 'hr001@hrms.com');
INSERT INTO `accounts_user` VALUES (3, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'hr002', '', '', 1, 1, '2024-02-01 00:00:00.000000', '13800000003', 'hr', '李人事', 'hr002@hrms.com');
INSERT INTO `accounts_user` VALUES (4, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'hr003', '', '', 1, 1, '2024-03-01 00:00:00.000000', '13800000004', 'hr', '王人事', 'hr003@hrms.com');
INSERT INTO `accounts_user` VALUES (5, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0001', '', '', 0, 0, '2024-01-10 00:00:00.000000', '13800000005', 'employee', '张伟', 'zhangwei@hrms.com');
INSERT INTO `accounts_user` VALUES (6, 'pbkdf2_sha256$1000000$3W9gXgjFkew9z0ZA5qsdQw$NChcoZJSGWAOO4usxEqug/+Isl4gYJwklf3gQNAxO2Y=', '2026-01-24 16:10:19.000000', 0, 'emp0002', '', '', 0, 1, '2024-01-15 00:00:00.000000', '13800000006', 'employee', '李娜', 'lina@hrms.com');
INSERT INTO `accounts_user` VALUES (7, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0003', '', '', 0, 1, '2024-02-01 00:00:00.000000', '13800000007', 'employee', '王强', 'wangqiang@hrms.com');
INSERT INTO `accounts_user` VALUES (8, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0004', '', '', 0, 1, '2024-02-10 00:00:00.000000', '13800000008', 'employee', '刘洋', 'liuyang@hrms.com');
INSERT INTO `accounts_user` VALUES (9, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0005', '', '', 0, 1, '2024-02-20 00:00:00.000000', '13800000009', 'employee', '陈静', 'chenjing@hrms.com');
INSERT INTO `accounts_user` VALUES (10, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0006', '', '', 0, 1, '2024-03-01 00:00:00.000000', '13800000010', 'employee', '赵磊', 'zhaolei@hrms.com');
INSERT INTO `accounts_user` VALUES (11, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0007', '', '', 0, 1, '2024-03-05 00:00:00.000000', '13800000011', 'employee', '吴敏', 'wumin@hrms.com');
INSERT INTO `accounts_user` VALUES (12, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0008', '', '', 0, 1, '2024-03-10 00:00:00.000000', '13800000012', 'employee', '周杰', 'zhoujie@hrms.com');
INSERT INTO `accounts_user` VALUES (13, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0009', '', '', 0, 1, '2024-03-15 00:00:00.000000', '13800000013', 'employee', '徐丽', 'xuli@hrms.com');
INSERT INTO `accounts_user` VALUES (14, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0010', '', '', 0, 1, '2024-03-20 00:00:00.000000', '13800000014', 'employee', '孙鹏', 'sunpeng@hrms.com');
INSERT INTO `accounts_user` VALUES (15, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0011', '', '', 0, 1, '2024-04-01 00:00:00.000000', '13800000015', 'employee', '马艳', 'mayan@hrms.com');
INSERT INTO `accounts_user` VALUES (16, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0012', '', '', 0, 1, '2024-04-05 00:00:00.000000', '13800000016', 'employee', '朱浩', 'zhuhao@hrms.com');
INSERT INTO `accounts_user` VALUES (17, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0013', '', '', 0, 1, '2024-04-10 00:00:00.000000', '13800000017', 'employee', '胡芳', 'hufang@hrms.com');
INSERT INTO `accounts_user` VALUES (18, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0014', '', '', 0, 1, '2024-04-15 00:00:00.000000', '13800000018', 'employee', '林宇', 'linyu@hrms.com');
INSERT INTO `accounts_user` VALUES (19, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0015', '', '', 0, 1, '2024-04-20 00:00:00.000000', '13800000019', 'employee', '韩梅', 'hanmei@hrms.com');
INSERT INTO `accounts_user` VALUES (20, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0016', '', '', 0, 1, '2024-05-01 00:00:00.000000', '13800000020', 'employee', '高健', 'gaojian@hrms.com');
INSERT INTO `accounts_user` VALUES (21, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0017', '', '', 0, 1, '2024-05-05 00:00:00.000000', '13800000021', 'employee', '谢婷', 'xieting@hrms.com');
INSERT INTO `accounts_user` VALUES (22, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0018', '', '', 0, 1, '2024-05-10 00:00:00.000000', '13800000022', 'employee', '唐伟', 'tangwei@hrms.com');
INSERT INTO `accounts_user` VALUES (23, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0019', '', '', 0, 1, '2024-05-15 00:00:00.000000', '13800000023', 'employee', '董雪', 'dongxue@hrms.com');
INSERT INTO `accounts_user` VALUES (24, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0020', '', '', 0, 1, '2024-05-20 00:00:00.000000', '13800000024', 'employee', '冯涛', 'fengtao@hrms.com');
INSERT INTO `accounts_user` VALUES (25, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0021', '', '', 0, 1, '2024-01-20 00:00:00.000000', '13800000025', 'employee', '曹鹏', 'caopeng@hrms.com');
INSERT INTO `accounts_user` VALUES (26, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0022', '', '', 0, 1, '2024-02-15 00:00:00.000000', '13800000026', 'employee', '邓琴', 'dengqin@hrms.com');
INSERT INTO `accounts_user` VALUES (27, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0023', '', '', 0, 1, '2024-03-01 00:00:00.000000', '13800000027', 'employee', '苏磊', 'sulei@hrms.com');
INSERT INTO `accounts_user` VALUES (28, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0024', '', '', 0, 1, '2024-03-20 00:00:00.000000', '13800000028', 'employee', '杨帆', 'yangfan@hrms.com');
INSERT INTO `accounts_user` VALUES (29, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0025', '', '', 0, 1, '2024-04-01 00:00:00.000000', '13800000029', 'employee', '于慧', 'yuhui@hrms.com');
INSERT INTO `accounts_user` VALUES (30, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0026', '', '', 0, 1, '2024-04-15 00:00:00.000000', '13800000030', 'employee', '何刚', 'hegang@hrms.com');
INSERT INTO `accounts_user` VALUES (31, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0027', '', '', 0, 1, '2024-05-01 00:00:00.000000', '13800000031', 'employee', '吕娜', 'lvna@hrms.com');
INSERT INTO `accounts_user` VALUES (32, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0028', '', '', 0, 1, '2024-05-10 00:00:00.000000', '13800000032', 'employee', '潘明', 'panming@hrms.com');
INSERT INTO `accounts_user` VALUES (33, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0029', '', '', 0, 1, '2024-05-20 00:00:00.000000', '13800000033', 'employee', '罗娟', 'luojuan@hrms.com');
INSERT INTO `accounts_user` VALUES (34, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0030', '', '', 0, 1, '2024-06-01 00:00:00.000000', '13800000034', 'employee', '肖鹏', 'xiaopeng@hrms.com');
INSERT INTO `accounts_user` VALUES (35, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0031', '', '', 0, 1, '2024-01-25 00:00:00.000000', '13800000035', 'employee', '梁伟', 'liangwei@hrms.com');
INSERT INTO `accounts_user` VALUES (36, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0032', '', '', 0, 1, '2024-02-20 00:00:00.000000', '13800000036', 'employee', '田莉', 'tianli@hrms.com');
INSERT INTO `accounts_user` VALUES (37, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0033', '', '', 0, 1, '2024-03-10 00:00:00.000000', '13800000037', 'employee', '蒋明', 'jiangming@hrms.com');
INSERT INTO `accounts_user` VALUES (38, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0034', '', '', 0, 1, '2024-03-25 00:00:00.000000', '13800000038', 'employee', '雷艳', 'leiyan@hrms.com');
INSERT INTO `accounts_user` VALUES (39, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0035', '', '', 0, 1, '2024-04-05 00:00:00.000000', '13800000039', 'employee', '段强', 'duanqiang@hrms.com');
INSERT INTO `accounts_user` VALUES (40, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0036', '', '', 0, 1, '2024-04-20 00:00:00.000000', '13800000040', 'employee', '武娜', 'wuna@hrms.com');
INSERT INTO `accounts_user` VALUES (41, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0037', '', '', 0, 1, '2024-05-05 00:00:00.000000', '13800000041', 'employee', '贺鹏', 'hepeng@hrms.com');
INSERT INTO `accounts_user` VALUES (42, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0038', '', '', 0, 1, '2024-05-15 00:00:00.000000', '13800000042', 'employee', '康芳', 'kangfang@hrms.com');
INSERT INTO `accounts_user` VALUES (43, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0039', '', '', 0, 1, '2024-06-01 00:00:00.000000', '13800000043', 'employee', '姚磊', 'yaolei@hrms.com');
INSERT INTO `accounts_user` VALUES (44, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0040', '', '', 0, 1, '2024-06-10 00:00:00.000000', '13800000044', 'employee', '姜莉', 'jiangli@hrms.com');
INSERT INTO `accounts_user` VALUES (45, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0041', '', '', 0, 1, '2024-02-01 00:00:00.000000', '13800000045', 'employee', '范明', 'fanming@hrms.com');
INSERT INTO `accounts_user` VALUES (46, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0042', '', '', 0, 1, '2024-03-01 00:00:00.000000', '13800000046', 'employee', '丁倩', 'dingqian@hrms.com');
INSERT INTO `accounts_user` VALUES (47, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0043', '', '', 0, 1, '2024-04-01 00:00:00.000000', '13800000047', 'employee', '魏强', 'weiqiang@hrms.com');
INSERT INTO `accounts_user` VALUES (48, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0044', '', '', 0, 1, '2024-05-01 00:00:00.000000', '13800000048', 'employee', '秦艳', 'qinyan@hrms.com');
INSERT INTO `accounts_user` VALUES (49, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0045', '', '', 0, 1, '2024-06-01 00:00:00.000000', '13800000049', 'employee', '彭鹏', 'pengpeng@hrms.com');
INSERT INTO `accounts_user` VALUES (50, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0046', '', '', 0, 1, '2024-01-10 00:00:00.000000', '13800000050', 'employee', '邵杰', 'shaojie@hrms.com');
INSERT INTO `accounts_user` VALUES (51, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0047', '', '', 0, 1, '2024-02-15 00:00:00.000000', '13800000051', 'employee', '阎丽', 'yanli@hrms.com');
INSERT INTO `accounts_user` VALUES (52, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0048', '', '', 0, 1, '2024-03-01 00:00:00.000000', '13800000052', 'employee', '薛磊', 'xuelei@hrms.com');
INSERT INTO `accounts_user` VALUES (53, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0049', '', '', 0, 1, '2024-03-20 00:00:00.000000', '13800000053', 'employee', '余娜', 'yuna@hrms.com');
INSERT INTO `accounts_user` VALUES (54, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0050', '', '', 0, 1, '2024-04-05 00:00:00.000000', '13800000054', 'employee', '郝鹏', 'haopeng@hrms.com');
INSERT INTO `accounts_user` VALUES (55, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0051', '', '', 0, 1, '2024-04-20 00:00:00.000000', '13800000055', 'employee', '侯芳', 'houfang@hrms.com');
INSERT INTO `accounts_user` VALUES (56, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0052', '', '', 0, 1, '2024-05-05 00:00:00.000000', '13800000056', 'employee', '毛强', 'maoqiang@hrms.com');
INSERT INTO `accounts_user` VALUES (57, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0053', '', '', 0, 1, '2024-05-20 00:00:00.000000', '13800000057', 'employee', '郭倩', 'guoqian@hrms.com');
INSERT INTO `accounts_user` VALUES (58, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0054', '', '', 0, 1, '2024-01-20 00:00:00.000000', '13800000058', 'employee', '戴伟', 'daiwei@hrms.com');
INSERT INTO `accounts_user` VALUES (59, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0055', '', '', 0, 1, '2024-02-10 00:00:00.000000', '13800000059', 'employee', '任莉', 'renli@hrms.com');
INSERT INTO `accounts_user` VALUES (60, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0056', '', '', 0, 1, '2024-02-28 00:00:00.000000', '13800000060', 'employee', '袁明', 'yuanming@hrms.com');
INSERT INTO `accounts_user` VALUES (61, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0057', '', '', 0, 1, '2024-03-15 00:00:00.000000', '13800000061', 'employee', '金艳', 'jinyan@hrms.com');
INSERT INTO `accounts_user` VALUES (62, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0058', '', '', 0, 1, '2024-04-01 00:00:00.000000', '13800000062', 'employee', '戚强', 'qiqiang@hrms.com');
INSERT INTO `accounts_user` VALUES (63, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0059', '', '', 0, 1, '2024-04-15 00:00:00.000000', '13800000063', 'employee', '谢娜', 'xiena@hrms.com');
INSERT INTO `accounts_user` VALUES (64, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0060', '', '', 0, 1, '2024-04-30 00:00:00.000000', '13800000064', 'employee', '喻鹏', 'yupeng@hrms.com');
INSERT INTO `accounts_user` VALUES (65, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0061', '', '', 0, 1, '2024-05-10 00:00:00.000000', '13800000065', 'employee', '柏芳', 'baifang@hrms.com');
INSERT INTO `accounts_user` VALUES (66, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0062', '', '', 0, 1, '2024-05-25 00:00:00.000000', '13800000066', 'employee', '丛强', 'congqiang@hrms.com');
INSERT INTO `accounts_user` VALUES (67, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0063', '', '', 0, 1, '2024-06-05 00:00:00.000000', '13800000067', 'employee', '赖倩', 'laiqian@hrms.com');
INSERT INTO `accounts_user` VALUES (68, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0064', '', '', 0, 1, '2024-02-01 00:00:00.000000', '13800000068', 'employee', '葛伟', 'gewei@hrms.com');
INSERT INTO `accounts_user` VALUES (69, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0065', '', '', 0, 1, '2024-02-20 00:00:00.000000', '13800000069', 'employee', '瞿莉', 'quli@hrms.com');
INSERT INTO `accounts_user` VALUES (70, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0066', '', '', 0, 1, '2024-03-10 00:00:00.000000', '13800000070', 'employee', '童明', 'tongming@hrms.com');
INSERT INTO `accounts_user` VALUES (71, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0067', '', '', 0, 1, '2024-03-25 00:00:00.000000', '13800000071', 'employee', '向艳', 'xiangyan@hrms.com');
INSERT INTO `accounts_user` VALUES (72, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0068', '', '', 0, 1, '2024-04-10 00:00:00.000000', '13800000072', 'employee', '卜强', 'buqiang@hrms.com');
INSERT INTO `accounts_user` VALUES (73, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0069', '', '', 0, 1, '2024-04-25 00:00:00.000000', '13800000073', 'employee', '燕娜', 'yanna@hrms.com');
INSERT INTO `accounts_user` VALUES (74, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0070', '', '', 0, 1, '2024-05-05 00:00:00.000000', '13800000074', 'employee', '门鹏', 'menpeng@hrms.com');
INSERT INTO `accounts_user` VALUES (75, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0071', '', '', 0, 1, '2024-05-20 00:00:00.000000', '13800000075', 'employee', '农芳', 'nongfang@hrms.com');
INSERT INTO `accounts_user` VALUES (76, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0072', '', '', 0, 1, '2024-01-15 00:00:00.000000', '13800000076', 'employee', '苍伟', 'cangwei@hrms.com');
INSERT INTO `accounts_user` VALUES (77, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0073', '', '', 0, 1, '2024-02-01 00:00:00.000000', '13800000077', 'employee', '樊莉', 'fanli@hrms.com');
INSERT INTO `accounts_user` VALUES (78, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0074', '', '', 0, 1, '2024-02-20 00:00:00.000000', '13800000078', 'employee', '利明', 'liming@hrms.com');
INSERT INTO `accounts_user` VALUES (79, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0075', '', '', 0, 1, '2024-03-10 00:00:00.000000', '13800000079', 'employee', '贵艳', 'guiyan@hrms.com');
INSERT INTO `accounts_user` VALUES (80, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0076', '', '', 0, 1, '2024-03-25 00:00:00.000000', '13800000080', 'employee', '农强', 'nongqiang@hrms.com');
INSERT INTO `accounts_user` VALUES (81, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0077', '', '', 0, 1, '2024-04-05 00:00:00.000000', '13800000081', 'employee', '凡娜', 'fanna@hrms.com');
INSERT INTO `accounts_user` VALUES (82, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0078', '', '', 0, 1, '2024-04-20 00:00:00.000000', '13800000082', 'employee', '黎鹏', 'lipeng@hrms.com');
INSERT INTO `accounts_user` VALUES (83, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0079', '', '', 0, 1, '2024-05-05 00:00:00.000000', '13800000083', 'employee', '苗芳', 'miaofang@hrms.com');
INSERT INTO `accounts_user` VALUES (84, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0080', '', '', 0, 1, '2024-01-20 00:00:00.000000', '13800000084', 'employee', '禹伟', 'yuwei@hrms.com');
INSERT INTO `accounts_user` VALUES (85, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0081', '', '', 0, 1, '2024-02-15 00:00:00.000000', '13800000085', 'employee', '巴莉', 'bali@hrms.com');
INSERT INTO `accounts_user` VALUES (86, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0082', '', '', 0, 1, '2024-03-01 00:00:00.000000', '13800000086', 'employee', '蒙明', 'mengming@hrms.com');
INSERT INTO `accounts_user` VALUES (87, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0083', '', '', 0, 1, '2024-03-20 00:00:00.000000', '13800000087', 'employee', '泉艳', 'quanyan@hrms.com');
INSERT INTO `accounts_user` VALUES (88, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0084', '', '', 0, 1, '2024-04-10 00:00:00.000000', '13800000088', 'employee', '敬强', 'jingqiang@hrms.com');
INSERT INTO `accounts_user` VALUES (89, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0085', '', '', 0, 1, '2024-02-01 00:00:00.000000', '13800000089', 'employee', '湛伟', 'zhanwei@hrms.com');
INSERT INTO `accounts_user` VALUES (90, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0086', '', '', 0, 1, '2024-03-01 00:00:00.000000', '13800000090', 'employee', '晏莉', 'yanli2@hrms.com');
INSERT INTO `accounts_user` VALUES (91, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0087', '', '', 0, 1, '2024-06-01 00:00:00.000000', '13800000091', 'employee', '巩伟', 'gongwei@hrms.com');
INSERT INTO `accounts_user` VALUES (92, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0088', '', '', 0, 1, '2024-06-05 00:00:00.000000', '13800000092', 'employee', '仲莉', 'zhongli@hrms.com');
INSERT INTO `accounts_user` VALUES (93, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0089', '', '', 0, 1, '2024-06-10 00:00:00.000000', '13800000093', 'employee', '毕明', 'biming@hrms.com');
INSERT INTO `accounts_user` VALUES (94, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0090', '', '', 0, 1, '2024-06-15 00:00:00.000000', '13800000094', 'employee', '景艳', 'jingyan@hrms.com');
INSERT INTO `accounts_user` VALUES (95, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0091', '', '', 0, 1, '2024-06-20 00:00:00.000000', '13800000095', 'employee', '晏强', 'yanqiang@hrms.com');
INSERT INTO `accounts_user` VALUES (96, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0092', '', '', 0, 1, '2024-06-25 00:00:00.000000', '13800000096', 'employee', '诸娜', 'zhuna@hrms.com');
INSERT INTO `accounts_user` VALUES (97, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0093', '', '', 0, 1, '2024-06-28 00:00:00.000000', '13800000097', 'employee', '屠鹏', 'tupeng@hrms.com');
INSERT INTO `accounts_user` VALUES (98, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0094', '', '', 0, 1, '2024-06-30 00:00:00.000000', '13800000098', 'employee', '鞠芳', 'jufang@hrms.com');
INSERT INTO `accounts_user` VALUES (99, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0095', '', '', 0, 1, '2024-07-01 00:00:00.000000', '13800000099', 'employee', '仰伟', 'yangwei@hrms.com');
INSERT INTO `accounts_user` VALUES (100, 'pbkdf2_sha256$1000000$lOIncR9jA2MJEekyudOSDO$7lK14sVM4WrLkfuuT+1RQCRMzA02fO3YLKKTzV11MZ0=', '2026-01-24 16:10:19.000000', 0, 'emp0096', '', '', 0, 1, '2024-07-05 00:00:00.000000', '13800000100', 'hr', '麦莉', 'maili@hrms.com');

-- ----------------------------
-- Table structure for accounts_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `accounts_user_groups`;
CREATE TABLE `accounts_user_groups`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `accounts_user_groups_user_id_group_id_59c0b32f_uniq`(`user_id` ASC, `group_id` ASC) USING BTREE,
  INDEX `accounts_user_groups_group_id_bd11a704_fk_auth_group_id`(`group_id` ASC) USING BTREE,
  CONSTRAINT `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `accounts_user_groups_user_id_52b62117_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of accounts_user_groups
-- ----------------------------

-- ----------------------------
-- Table structure for accounts_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `accounts_user_user_permissions`;
CREATE TABLE `accounts_user_user_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq`(`user_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `accounts_user_user_p_permission_id_113bb443_fk_auth_perm`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `accounts_user_user_p_user_id_e4f0a161_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of accounts_user_user_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for accounts_usereditrequest
-- ----------------------------
DROP TABLE IF EXISTS `accounts_usereditrequest`;
CREATE TABLE `accounts_usereditrequest`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `edit_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `old_value` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `new_value` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `reason` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `reviewer_comment` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `reviewer_id` bigint NULL DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `accounts_usereditreq_reviewer_id_c8450615_fk_accounts_`(`reviewer_id` ASC) USING BTREE,
  INDEX `accounts_usereditrequest_user_id_cc6cea50_fk_accounts_user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `accounts_usereditreq_reviewer_id_c8450615_fk_accounts_` FOREIGN KEY (`reviewer_id`) REFERENCES `accounts_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `accounts_usereditrequest_user_id_cc6cea50_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of accounts_usereditrequest
-- ----------------------------
INSERT INTO `accounts_usereditrequest` VALUES (1, 'phone', '13800000001', '18199987365', '新手机号', 'approved', '', '2026-01-25 02:58:48.366856', '2026-01-25 02:59:02.691481', 1, 1);
INSERT INTO `accounts_usereditrequest` VALUES (2, 'phone', '13800000006', '13132145678', '新手机号', 'pending', '', '2026-01-25 03:07:21.764428', '2026-01-25 03:07:21.764428', NULL, 6);
INSERT INTO `accounts_usereditrequest` VALUES (3, 'email', 'lina@hrms.com', 'lina993@qq.com', '新邮箱', 'pending', '', '2026-01-25 03:07:57.535313', '2026-01-25 03:07:57.535313', NULL, 6);

-- ----------------------------
-- Table structure for approval_approvalrequest
-- ----------------------------
DROP TABLE IF EXISTS `approval_approvalrequest`;
CREATE TABLE `approval_approvalrequest`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `request_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `leave_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `start_time` datetime(6) NOT NULL,
  `end_time` datetime(6) NOT NULL,
  `reason` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `hours` decimal(5, 1) NULL DEFAULT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `approver_reason` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `approver_id` bigint NULL DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `approval_approvalreq_approver_id_f0b65eba_fk_accounts_`(`approver_id` ASC) USING BTREE,
  INDEX `approval_approvalrequest_user_id_e2504f14_fk_accounts_user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `approval_approvalreq_approver_id_f0b65eba_fk_accounts_` FOREIGN KEY (`approver_id`) REFERENCES `accounts_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `approval_approvalrequest_user_id_e2504f14_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of approval_approvalrequest
-- ----------------------------
INSERT INTO `approval_approvalrequest` VALUES (1, 'leave', 'personal', '2026-01-23 16:00:00.000000', '2026-01-24 16:00:00.000000', '测试事假', NULL, 'approved', '通过', '2026-01-24 12:07:24.802552', '2026-01-24 12:09:59.328108', 1, 1);
INSERT INTO `approval_approvalrequest` VALUES (2, 'overtime', NULL, '2026-01-23 16:00:00.000000', '2026-01-24 16:00:00.000000', '123', 2.0, 'approved', '通过', '2026-01-24 12:07:55.087964', '2026-01-24 12:10:09.251437', 1, 1);
INSERT INTO `approval_approvalrequest` VALUES (3, 'leave', 'personal', '2026-01-23 16:00:00.000000', '2026-01-24 16:00:00.000000', '111', NULL, 'pending', NULL, '2026-01-24 12:10:43.421461', '2026-01-24 12:10:43.421461', NULL, 1);
INSERT INTO `approval_approvalrequest` VALUES (4, 'leave', 'personal', '2026-01-23 16:00:00.000000', '2026-01-24 16:00:00.000000', '嘿嘿', NULL, 'pending', NULL, '2026-01-24 12:13:27.232338', '2026-01-24 12:13:27.232338', NULL, 1);
INSERT INTO `approval_approvalrequest` VALUES (5, 'leave', 'personal', '2026-01-23 16:00:00.000000', '2026-01-24 16:00:00.000000', '请假交材料', NULL, 'pending', NULL, '2026-01-24 15:59:01.754148', '2026-01-24 15:59:01.754148', NULL, 6);

-- ----------------------------
-- Table structure for attendance_attendance
-- ----------------------------
DROP TABLE IF EXISTS `attendance_attendance`;
CREATE TABLE `attendance_attendance`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `check_in_time` time(6) NULL DEFAULT NULL,
  `check_out_time` time(6) NULL DEFAULT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `attendance_attendance_user_id_date_407a5a02_uniq`(`user_id` ASC, `date` ASC) USING BTREE,
  INDEX `attendance_attendance_date_3c949aa8`(`date` ASC) USING BTREE,
  CONSTRAINT `attendance_attendance_user_id_2bd82a2c_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2020 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of attendance_attendance
-- ----------------------------
INSERT INTO `attendance_attendance` VALUES (1, '2026-01-24', '16:10:58.000000', NULL, 'late', '2026-01-24 08:10:58.695201', '2026-01-24 09:26:05.293782', 1);
INSERT INTO `attendance_attendance` VALUES (2, '2024-12-02', '08:55:06.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 5);
INSERT INTO `attendance_attendance` VALUES (3, '2024-12-02', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 6);
INSERT INTO `attendance_attendance` VALUES (4, '2024-12-02', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 7);
INSERT INTO `attendance_attendance` VALUES (5, '2024-12-02', '08:55:00.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 8);
INSERT INTO `attendance_attendance` VALUES (6, '2024-12-02', '09:05:14.000000', NULL, 'late', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 9);
INSERT INTO `attendance_attendance` VALUES (7, '2024-12-02', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 10);
INSERT INTO `attendance_attendance` VALUES (8, '2024-12-02', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 11);
INSERT INTO `attendance_attendance` VALUES (9, '2024-12-02', '08:55:07.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 12);
INSERT INTO `attendance_attendance` VALUES (10, '2024-12-02', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 13);
INSERT INTO `attendance_attendance` VALUES (11, '2024-12-02', '08:55:02.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 14);
INSERT INTO `attendance_attendance` VALUES (12, '2024-12-02', '08:55:05.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 15);
INSERT INTO `attendance_attendance` VALUES (13, '2024-12-02', '08:55:02.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 16);
INSERT INTO `attendance_attendance` VALUES (14, '2024-12-02', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 17);
INSERT INTO `attendance_attendance` VALUES (15, '2024-12-02', '08:55:08.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 18);
INSERT INTO `attendance_attendance` VALUES (16, '2024-12-02', '08:55:00.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 19);
INSERT INTO `attendance_attendance` VALUES (17, '2024-12-02', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 20);
INSERT INTO `attendance_attendance` VALUES (18, '2024-12-02', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 21);
INSERT INTO `attendance_attendance` VALUES (19, '2024-12-02', '08:55:07.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 22);
INSERT INTO `attendance_attendance` VALUES (20, '2024-12-02', '08:55:07.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 23);
INSERT INTO `attendance_attendance` VALUES (21, '2024-12-02', NULL, '17:45:07.000000', 'early', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 24);
INSERT INTO `attendance_attendance` VALUES (22, '2024-12-02', '09:05:03.000000', NULL, 'late', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 25);
INSERT INTO `attendance_attendance` VALUES (23, '2024-12-02', NULL, '17:45:04.000000', 'early', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 26);
INSERT INTO `attendance_attendance` VALUES (24, '2024-12-02', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 27);
INSERT INTO `attendance_attendance` VALUES (25, '2024-12-02', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 28);
INSERT INTO `attendance_attendance` VALUES (26, '2024-12-02', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 29);
INSERT INTO `attendance_attendance` VALUES (27, '2024-12-02', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 30);
INSERT INTO `attendance_attendance` VALUES (28, '2024-12-02', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 31);
INSERT INTO `attendance_attendance` VALUES (29, '2024-12-02', '08:55:06.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 32);
INSERT INTO `attendance_attendance` VALUES (30, '2024-12-02', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 33);
INSERT INTO `attendance_attendance` VALUES (31, '2024-12-02', '08:55:07.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 34);
INSERT INTO `attendance_attendance` VALUES (32, '2024-12-02', '08:55:00.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 35);
INSERT INTO `attendance_attendance` VALUES (33, '2024-12-02', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 36);
INSERT INTO `attendance_attendance` VALUES (34, '2024-12-02', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 37);
INSERT INTO `attendance_attendance` VALUES (35, '2024-12-02', '09:05:10.000000', NULL, 'late', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 38);
INSERT INTO `attendance_attendance` VALUES (36, '2024-12-02', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 39);
INSERT INTO `attendance_attendance` VALUES (37, '2024-12-02', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 40);
INSERT INTO `attendance_attendance` VALUES (38, '2024-12-02', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 41);
INSERT INTO `attendance_attendance` VALUES (39, '2024-12-02', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 42);
INSERT INTO `attendance_attendance` VALUES (40, '2024-12-02', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 43);
INSERT INTO `attendance_attendance` VALUES (41, '2024-12-02', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 44);
INSERT INTO `attendance_attendance` VALUES (42, '2024-12-02', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 45);
INSERT INTO `attendance_attendance` VALUES (43, '2024-12-02', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 46);
INSERT INTO `attendance_attendance` VALUES (44, '2024-12-02', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 47);
INSERT INTO `attendance_attendance` VALUES (45, '2024-12-02', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 48);
INSERT INTO `attendance_attendance` VALUES (46, '2024-12-02', '08:55:06.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 49);
INSERT INTO `attendance_attendance` VALUES (47, '2024-12-02', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 50);
INSERT INTO `attendance_attendance` VALUES (48, '2024-12-02', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 51);
INSERT INTO `attendance_attendance` VALUES (49, '2024-12-02', '08:55:01.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 52);
INSERT INTO `attendance_attendance` VALUES (50, '2024-12-02', '08:55:08.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 53);
INSERT INTO `attendance_attendance` VALUES (51, '2024-12-02', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 54);
INSERT INTO `attendance_attendance` VALUES (52, '2024-12-02', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 55);
INSERT INTO `attendance_attendance` VALUES (53, '2024-12-02', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 56);
INSERT INTO `attendance_attendance` VALUES (54, '2024-12-02', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 57);
INSERT INTO `attendance_attendance` VALUES (55, '2024-12-02', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 58);
INSERT INTO `attendance_attendance` VALUES (56, '2024-12-02', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 59);
INSERT INTO `attendance_attendance` VALUES (57, '2024-12-02', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 60);
INSERT INTO `attendance_attendance` VALUES (58, '2024-12-02', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 61);
INSERT INTO `attendance_attendance` VALUES (59, '2024-12-02', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 62);
INSERT INTO `attendance_attendance` VALUES (60, '2024-12-02', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 63);
INSERT INTO `attendance_attendance` VALUES (61, '2024-12-02', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 64);
INSERT INTO `attendance_attendance` VALUES (62, '2024-12-02', '08:55:06.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 65);
INSERT INTO `attendance_attendance` VALUES (63, '2024-12-02', '09:05:29.000000', NULL, 'late', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 66);
INSERT INTO `attendance_attendance` VALUES (64, '2024-12-02', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 67);
INSERT INTO `attendance_attendance` VALUES (65, '2024-12-02', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 68);
INSERT INTO `attendance_attendance` VALUES (66, '2024-12-02', '09:05:10.000000', NULL, 'late', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 69);
INSERT INTO `attendance_attendance` VALUES (67, '2024-12-02', '08:55:00.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 70);
INSERT INTO `attendance_attendance` VALUES (68, '2024-12-02', '08:55:07.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 71);
INSERT INTO `attendance_attendance` VALUES (69, '2024-12-02', '09:05:26.000000', NULL, 'late', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 72);
INSERT INTO `attendance_attendance` VALUES (70, '2024-12-02', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 73);
INSERT INTO `attendance_attendance` VALUES (71, '2024-12-02', '08:55:05.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 74);
INSERT INTO `attendance_attendance` VALUES (72, '2024-12-02', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 75);
INSERT INTO `attendance_attendance` VALUES (73, '2024-12-02', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 76);
INSERT INTO `attendance_attendance` VALUES (74, '2024-12-02', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 77);
INSERT INTO `attendance_attendance` VALUES (75, '2024-12-02', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 78);
INSERT INTO `attendance_attendance` VALUES (76, '2024-12-02', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 79);
INSERT INTO `attendance_attendance` VALUES (77, '2024-12-02', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 80);
INSERT INTO `attendance_attendance` VALUES (78, '2024-12-02', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 81);
INSERT INTO `attendance_attendance` VALUES (79, '2024-12-02', NULL, NULL, 'absent', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 82);
INSERT INTO `attendance_attendance` VALUES (80, '2024-12-02', '08:55:10.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 83);
INSERT INTO `attendance_attendance` VALUES (81, '2024-12-02', '08:55:08.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 84);
INSERT INTO `attendance_attendance` VALUES (82, '2024-12-02', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 85);
INSERT INTO `attendance_attendance` VALUES (83, '2024-12-02', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 86);
INSERT INTO `attendance_attendance` VALUES (84, '2024-12-02', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 87);
INSERT INTO `attendance_attendance` VALUES (85, '2024-12-02', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 88);
INSERT INTO `attendance_attendance` VALUES (86, '2024-12-02', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 89);
INSERT INTO `attendance_attendance` VALUES (87, '2024-12-02', '08:55:00.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 90);
INSERT INTO `attendance_attendance` VALUES (88, '2024-12-02', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 91);
INSERT INTO `attendance_attendance` VALUES (89, '2024-12-02', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 92);
INSERT INTO `attendance_attendance` VALUES (90, '2024-12-02', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 93);
INSERT INTO `attendance_attendance` VALUES (91, '2024-12-02', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 94);
INSERT INTO `attendance_attendance` VALUES (92, '2024-12-02', '08:55:08.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 95);
INSERT INTO `attendance_attendance` VALUES (93, '2024-12-02', '08:55:07.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 96);
INSERT INTO `attendance_attendance` VALUES (94, '2024-12-02', '09:05:28.000000', NULL, 'late', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 97);
INSERT INTO `attendance_attendance` VALUES (95, '2024-12-02', NULL, '17:45:10.000000', 'early', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 98);
INSERT INTO `attendance_attendance` VALUES (96, '2024-12-02', '09:05:25.000000', NULL, 'late', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 99);
INSERT INTO `attendance_attendance` VALUES (97, '2024-12-02', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 100);
INSERT INTO `attendance_attendance` VALUES (98, '2024-12-03', '08:55:08.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 5);
INSERT INTO `attendance_attendance` VALUES (99, '2024-12-03', '08:55:09.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 6);
INSERT INTO `attendance_attendance` VALUES (100, '2024-12-03', '09:05:29.000000', NULL, 'late', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 7);
INSERT INTO `attendance_attendance` VALUES (101, '2024-12-03', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 8);
INSERT INTO `attendance_attendance` VALUES (102, '2024-12-03', '08:55:00.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 9);
INSERT INTO `attendance_attendance` VALUES (103, '2024-12-03', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 10);
INSERT INTO `attendance_attendance` VALUES (104, '2024-12-03', '08:55:10.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 11);
INSERT INTO `attendance_attendance` VALUES (105, '2024-12-03', '09:05:14.000000', NULL, 'late', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 12);
INSERT INTO `attendance_attendance` VALUES (106, '2024-12-03', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 13);
INSERT INTO `attendance_attendance` VALUES (107, '2024-12-03', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 14);
INSERT INTO `attendance_attendance` VALUES (108, '2024-12-03', NULL, NULL, 'absent', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 15);
INSERT INTO `attendance_attendance` VALUES (109, '2024-12-03', NULL, '17:45:09.000000', 'early', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 16);
INSERT INTO `attendance_attendance` VALUES (110, '2024-12-03', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 17);
INSERT INTO `attendance_attendance` VALUES (111, '2024-12-03', '08:55:00.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 18);
INSERT INTO `attendance_attendance` VALUES (112, '2024-12-03', '09:05:29.000000', NULL, 'late', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 19);
INSERT INTO `attendance_attendance` VALUES (113, '2024-12-03', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 20);
INSERT INTO `attendance_attendance` VALUES (114, '2024-12-03', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 21);
INSERT INTO `attendance_attendance` VALUES (115, '2024-12-03', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 22);
INSERT INTO `attendance_attendance` VALUES (116, '2024-12-03', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 23);
INSERT INTO `attendance_attendance` VALUES (117, '2024-12-03', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 24);
INSERT INTO `attendance_attendance` VALUES (118, '2024-12-03', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 25);
INSERT INTO `attendance_attendance` VALUES (119, '2024-12-03', '09:05:15.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 26);
INSERT INTO `attendance_attendance` VALUES (120, '2024-12-03', '08:55:00.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 27);
INSERT INTO `attendance_attendance` VALUES (121, '2024-12-03', '08:55:07.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 28);
INSERT INTO `attendance_attendance` VALUES (122, '2024-12-03', '09:05:16.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 29);
INSERT INTO `attendance_attendance` VALUES (123, '2024-12-03', NULL, '17:45:02.000000', 'early', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 30);
INSERT INTO `attendance_attendance` VALUES (124, '2024-12-03', '08:55:03.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 31);
INSERT INTO `attendance_attendance` VALUES (125, '2024-12-03', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 32);
INSERT INTO `attendance_attendance` VALUES (126, '2024-12-03', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 33);
INSERT INTO `attendance_attendance` VALUES (127, '2024-12-03', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 34);
INSERT INTO `attendance_attendance` VALUES (128, '2024-12-03', '09:05:26.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 35);
INSERT INTO `attendance_attendance` VALUES (129, '2024-12-03', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 36);
INSERT INTO `attendance_attendance` VALUES (130, '2024-12-03', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 37);
INSERT INTO `attendance_attendance` VALUES (131, '2024-12-03', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 38);
INSERT INTO `attendance_attendance` VALUES (132, '2024-12-03', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 39);
INSERT INTO `attendance_attendance` VALUES (133, '2024-12-03', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 40);
INSERT INTO `attendance_attendance` VALUES (134, '2024-12-03', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 41);
INSERT INTO `attendance_attendance` VALUES (135, '2024-12-03', '08:55:01.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 42);
INSERT INTO `attendance_attendance` VALUES (136, '2024-12-03', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 43);
INSERT INTO `attendance_attendance` VALUES (137, '2024-12-03', '08:55:10.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 44);
INSERT INTO `attendance_attendance` VALUES (138, '2024-12-03', '08:55:05.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 45);
INSERT INTO `attendance_attendance` VALUES (139, '2024-12-03', '08:55:00.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 46);
INSERT INTO `attendance_attendance` VALUES (140, '2024-12-03', '08:55:03.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 47);
INSERT INTO `attendance_attendance` VALUES (141, '2024-12-03', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 48);
INSERT INTO `attendance_attendance` VALUES (142, '2024-12-03', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 49);
INSERT INTO `attendance_attendance` VALUES (143, '2024-12-03', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 50);
INSERT INTO `attendance_attendance` VALUES (144, '2024-12-03', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 51);
INSERT INTO `attendance_attendance` VALUES (145, '2024-12-03', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 52);
INSERT INTO `attendance_attendance` VALUES (146, '2024-12-03', '09:05:07.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 53);
INSERT INTO `attendance_attendance` VALUES (147, '2024-12-03', '08:55:10.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 54);
INSERT INTO `attendance_attendance` VALUES (148, '2024-12-03', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 55);
INSERT INTO `attendance_attendance` VALUES (149, '2024-12-03', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 56);
INSERT INTO `attendance_attendance` VALUES (150, '2024-12-03', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 57);
INSERT INTO `attendance_attendance` VALUES (151, '2024-12-03', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 58);
INSERT INTO `attendance_attendance` VALUES (152, '2024-12-03', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 59);
INSERT INTO `attendance_attendance` VALUES (153, '2024-12-03', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 60);
INSERT INTO `attendance_attendance` VALUES (154, '2024-12-03', '08:55:01.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 61);
INSERT INTO `attendance_attendance` VALUES (155, '2024-12-03', NULL, NULL, 'absent', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 62);
INSERT INTO `attendance_attendance` VALUES (156, '2024-12-03', '08:55:02.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 63);
INSERT INTO `attendance_attendance` VALUES (157, '2024-12-03', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 64);
INSERT INTO `attendance_attendance` VALUES (158, '2024-12-03', '09:05:18.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 65);
INSERT INTO `attendance_attendance` VALUES (159, '2024-12-03', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 66);
INSERT INTO `attendance_attendance` VALUES (160, '2024-12-03', '09:05:21.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 67);
INSERT INTO `attendance_attendance` VALUES (161, '2024-12-03', '08:55:04.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 68);
INSERT INTO `attendance_attendance` VALUES (162, '2024-12-03', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 69);
INSERT INTO `attendance_attendance` VALUES (163, '2024-12-03', '08:55:04.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 70);
INSERT INTO `attendance_attendance` VALUES (164, '2024-12-03', '09:05:13.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 71);
INSERT INTO `attendance_attendance` VALUES (165, '2024-12-03', '08:55:01.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 72);
INSERT INTO `attendance_attendance` VALUES (166, '2024-12-03', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 73);
INSERT INTO `attendance_attendance` VALUES (167, '2024-12-03', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 74);
INSERT INTO `attendance_attendance` VALUES (168, '2024-12-03', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 75);
INSERT INTO `attendance_attendance` VALUES (169, '2024-12-03', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 76);
INSERT INTO `attendance_attendance` VALUES (170, '2024-12-03', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 77);
INSERT INTO `attendance_attendance` VALUES (171, '2024-12-03', '08:55:07.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 78);
INSERT INTO `attendance_attendance` VALUES (172, '2024-12-03', '08:55:07.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 79);
INSERT INTO `attendance_attendance` VALUES (173, '2024-12-03', '08:55:02.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 80);
INSERT INTO `attendance_attendance` VALUES (174, '2024-12-03', '09:05:09.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 81);
INSERT INTO `attendance_attendance` VALUES (175, '2024-12-03', '09:05:17.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 82);
INSERT INTO `attendance_attendance` VALUES (176, '2024-12-03', '08:55:03.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 83);
INSERT INTO `attendance_attendance` VALUES (177, '2024-12-03', '08:55:10.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 84);
INSERT INTO `attendance_attendance` VALUES (178, '2024-12-03', '09:05:14.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 85);
INSERT INTO `attendance_attendance` VALUES (179, '2024-12-03', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 86);
INSERT INTO `attendance_attendance` VALUES (180, '2024-12-03', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 87);
INSERT INTO `attendance_attendance` VALUES (181, '2024-12-03', '09:05:09.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 88);
INSERT INTO `attendance_attendance` VALUES (182, '2024-12-03', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 89);
INSERT INTO `attendance_attendance` VALUES (183, '2024-12-03', NULL, NULL, 'absent', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 90);
INSERT INTO `attendance_attendance` VALUES (184, '2024-12-03', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 91);
INSERT INTO `attendance_attendance` VALUES (185, '2024-12-03', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 92);
INSERT INTO `attendance_attendance` VALUES (186, '2024-12-03', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 93);
INSERT INTO `attendance_attendance` VALUES (187, '2024-12-03', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 94);
INSERT INTO `attendance_attendance` VALUES (188, '2024-12-03', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 95);
INSERT INTO `attendance_attendance` VALUES (189, '2024-12-03', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 96);
INSERT INTO `attendance_attendance` VALUES (190, '2024-12-03', '08:55:10.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 97);
INSERT INTO `attendance_attendance` VALUES (191, '2024-12-03', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 98);
INSERT INTO `attendance_attendance` VALUES (192, '2024-12-03', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 99);
INSERT INTO `attendance_attendance` VALUES (193, '2024-12-03', '08:55:03.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 100);
INSERT INTO `attendance_attendance` VALUES (194, '2024-12-04', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 5);
INSERT INTO `attendance_attendance` VALUES (195, '2024-12-04', '08:55:03.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 6);
INSERT INTO `attendance_attendance` VALUES (196, '2024-12-04', '08:55:06.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 7);
INSERT INTO `attendance_attendance` VALUES (197, '2024-12-04', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 8);
INSERT INTO `attendance_attendance` VALUES (198, '2024-12-04', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 9);
INSERT INTO `attendance_attendance` VALUES (199, '2024-12-04', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 10);
INSERT INTO `attendance_attendance` VALUES (200, '2024-12-04', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 11);
INSERT INTO `attendance_attendance` VALUES (201, '2024-12-04', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 12);
INSERT INTO `attendance_attendance` VALUES (202, '2024-12-04', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 13);
INSERT INTO `attendance_attendance` VALUES (203, '2024-12-04', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 14);
INSERT INTO `attendance_attendance` VALUES (204, '2024-12-04', '08:55:08.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 15);
INSERT INTO `attendance_attendance` VALUES (205, '2024-12-04', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 16);
INSERT INTO `attendance_attendance` VALUES (206, '2024-12-04', '08:55:08.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 17);
INSERT INTO `attendance_attendance` VALUES (207, '2024-12-04', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 18);
INSERT INTO `attendance_attendance` VALUES (208, '2024-12-04', '08:55:08.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 19);
INSERT INTO `attendance_attendance` VALUES (209, '2024-12-04', '08:55:02.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 20);
INSERT INTO `attendance_attendance` VALUES (210, '2024-12-04', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 21);
INSERT INTO `attendance_attendance` VALUES (211, '2024-12-04', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 22);
INSERT INTO `attendance_attendance` VALUES (212, '2024-12-04', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 23);
INSERT INTO `attendance_attendance` VALUES (213, '2024-12-04', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 24);
INSERT INTO `attendance_attendance` VALUES (214, '2024-12-04', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 25);
INSERT INTO `attendance_attendance` VALUES (215, '2024-12-04', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 26);
INSERT INTO `attendance_attendance` VALUES (216, '2024-12-04', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 27);
INSERT INTO `attendance_attendance` VALUES (217, '2024-12-04', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 28);
INSERT INTO `attendance_attendance` VALUES (218, '2024-12-04', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 29);
INSERT INTO `attendance_attendance` VALUES (219, '2024-12-04', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 30);
INSERT INTO `attendance_attendance` VALUES (220, '2024-12-04', '09:05:28.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 31);
INSERT INTO `attendance_attendance` VALUES (221, '2024-12-04', '09:05:20.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 32);
INSERT INTO `attendance_attendance` VALUES (222, '2024-12-04', '08:55:04.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 33);
INSERT INTO `attendance_attendance` VALUES (223, '2024-12-04', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 34);
INSERT INTO `attendance_attendance` VALUES (224, '2024-12-04', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 35);
INSERT INTO `attendance_attendance` VALUES (225, '2024-12-04', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 36);
INSERT INTO `attendance_attendance` VALUES (226, '2024-12-04', '08:55:05.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 37);
INSERT INTO `attendance_attendance` VALUES (227, '2024-12-04', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 38);
INSERT INTO `attendance_attendance` VALUES (228, '2024-12-04', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 39);
INSERT INTO `attendance_attendance` VALUES (229, '2024-12-04', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 40);
INSERT INTO `attendance_attendance` VALUES (230, '2024-12-04', '08:55:06.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 41);
INSERT INTO `attendance_attendance` VALUES (231, '2024-12-04', '08:55:00.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 42);
INSERT INTO `attendance_attendance` VALUES (232, '2024-12-04', NULL, '17:45:10.000000', 'early', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 43);
INSERT INTO `attendance_attendance` VALUES (233, '2024-12-04', NULL, NULL, 'absent', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 44);
INSERT INTO `attendance_attendance` VALUES (234, '2024-12-04', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 45);
INSERT INTO `attendance_attendance` VALUES (235, '2024-12-04', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 46);
INSERT INTO `attendance_attendance` VALUES (236, '2024-12-04', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 47);
INSERT INTO `attendance_attendance` VALUES (237, '2024-12-04', '08:55:00.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 48);
INSERT INTO `attendance_attendance` VALUES (238, '2024-12-04', '08:55:04.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 49);
INSERT INTO `attendance_attendance` VALUES (239, '2024-12-04', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 50);
INSERT INTO `attendance_attendance` VALUES (240, '2024-12-04', '08:55:06.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 51);
INSERT INTO `attendance_attendance` VALUES (241, '2024-12-04', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 52);
INSERT INTO `attendance_attendance` VALUES (242, '2024-12-04', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 53);
INSERT INTO `attendance_attendance` VALUES (243, '2024-12-04', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 54);
INSERT INTO `attendance_attendance` VALUES (244, '2024-12-04', '08:55:06.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 55);
INSERT INTO `attendance_attendance` VALUES (245, '2024-12-04', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 56);
INSERT INTO `attendance_attendance` VALUES (246, '2024-12-04', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 57);
INSERT INTO `attendance_attendance` VALUES (247, '2024-12-04', '09:05:09.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 58);
INSERT INTO `attendance_attendance` VALUES (248, '2024-12-04', '08:55:07.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 59);
INSERT INTO `attendance_attendance` VALUES (249, '2024-12-04', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 60);
INSERT INTO `attendance_attendance` VALUES (250, '2024-12-04', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 61);
INSERT INTO `attendance_attendance` VALUES (251, '2024-12-04', '08:55:07.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 62);
INSERT INTO `attendance_attendance` VALUES (252, '2024-12-04', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 63);
INSERT INTO `attendance_attendance` VALUES (253, '2024-12-04', '08:55:05.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 64);
INSERT INTO `attendance_attendance` VALUES (254, '2024-12-04', '08:55:10.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 65);
INSERT INTO `attendance_attendance` VALUES (255, '2024-12-04', '08:55:10.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 66);
INSERT INTO `attendance_attendance` VALUES (256, '2024-12-04', '08:55:08.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 67);
INSERT INTO `attendance_attendance` VALUES (257, '2024-12-04', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 68);
INSERT INTO `attendance_attendance` VALUES (258, '2024-12-04', '08:55:10.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 69);
INSERT INTO `attendance_attendance` VALUES (259, '2024-12-04', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 70);
INSERT INTO `attendance_attendance` VALUES (260, '2024-12-04', '08:55:05.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 71);
INSERT INTO `attendance_attendance` VALUES (261, '2024-12-04', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 72);
INSERT INTO `attendance_attendance` VALUES (262, '2024-12-04', '09:05:16.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 73);
INSERT INTO `attendance_attendance` VALUES (263, '2024-12-04', '08:55:04.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 74);
INSERT INTO `attendance_attendance` VALUES (264, '2024-12-04', NULL, NULL, 'absent', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 75);
INSERT INTO `attendance_attendance` VALUES (265, '2024-12-04', '08:55:09.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 76);
INSERT INTO `attendance_attendance` VALUES (266, '2024-12-04', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 77);
INSERT INTO `attendance_attendance` VALUES (267, '2024-12-04', '08:55:04.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 78);
INSERT INTO `attendance_attendance` VALUES (268, '2024-12-04', '08:55:02.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 79);
INSERT INTO `attendance_attendance` VALUES (269, '2024-12-04', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 80);
INSERT INTO `attendance_attendance` VALUES (270, '2024-12-04', '08:55:00.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 81);
INSERT INTO `attendance_attendance` VALUES (271, '2024-12-04', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 82);
INSERT INTO `attendance_attendance` VALUES (272, '2024-12-04', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 83);
INSERT INTO `attendance_attendance` VALUES (273, '2024-12-04', '08:55:10.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 84);
INSERT INTO `attendance_attendance` VALUES (274, '2024-12-04', '08:55:03.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 85);
INSERT INTO `attendance_attendance` VALUES (275, '2024-12-04', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 86);
INSERT INTO `attendance_attendance` VALUES (276, '2024-12-04', '09:05:02.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 87);
INSERT INTO `attendance_attendance` VALUES (277, '2024-12-04', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 88);
INSERT INTO `attendance_attendance` VALUES (278, '2024-12-04', '08:55:07.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 89);
INSERT INTO `attendance_attendance` VALUES (279, '2024-12-04', '08:55:03.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 90);
INSERT INTO `attendance_attendance` VALUES (280, '2024-12-04', '08:55:06.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 91);
INSERT INTO `attendance_attendance` VALUES (281, '2024-12-04', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 92);
INSERT INTO `attendance_attendance` VALUES (282, '2024-12-04', '08:55:00.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 93);
INSERT INTO `attendance_attendance` VALUES (283, '2024-12-04', '08:55:06.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 94);
INSERT INTO `attendance_attendance` VALUES (284, '2024-12-04', '09:05:21.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 95);
INSERT INTO `attendance_attendance` VALUES (285, '2024-12-04', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 96);
INSERT INTO `attendance_attendance` VALUES (286, '2024-12-04', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 97);
INSERT INTO `attendance_attendance` VALUES (287, '2024-12-04', '08:55:10.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 98);
INSERT INTO `attendance_attendance` VALUES (288, '2024-12-04', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 99);
INSERT INTO `attendance_attendance` VALUES (289, '2024-12-04', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 100);
INSERT INTO `attendance_attendance` VALUES (290, '2024-12-05', '08:55:09.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 5);
INSERT INTO `attendance_attendance` VALUES (291, '2024-12-05', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 6);
INSERT INTO `attendance_attendance` VALUES (292, '2024-12-05', '08:55:06.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 7);
INSERT INTO `attendance_attendance` VALUES (293, '2024-12-05', '09:05:20.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 8);
INSERT INTO `attendance_attendance` VALUES (294, '2024-12-05', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 9);
INSERT INTO `attendance_attendance` VALUES (295, '2024-12-05', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 10);
INSERT INTO `attendance_attendance` VALUES (296, '2024-12-05', '08:55:06.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 11);
INSERT INTO `attendance_attendance` VALUES (297, '2024-12-05', '08:55:03.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 12);
INSERT INTO `attendance_attendance` VALUES (298, '2024-12-05', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 13);
INSERT INTO `attendance_attendance` VALUES (299, '2024-12-05', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 14);
INSERT INTO `attendance_attendance` VALUES (300, '2024-12-05', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 15);
INSERT INTO `attendance_attendance` VALUES (301, '2024-12-05', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 16);
INSERT INTO `attendance_attendance` VALUES (302, '2024-12-05', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 17);
INSERT INTO `attendance_attendance` VALUES (303, '2024-12-05', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 18);
INSERT INTO `attendance_attendance` VALUES (304, '2024-12-05', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 19);
INSERT INTO `attendance_attendance` VALUES (305, '2024-12-05', NULL, NULL, 'absent', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 20);
INSERT INTO `attendance_attendance` VALUES (306, '2024-12-05', '08:55:00.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 21);
INSERT INTO `attendance_attendance` VALUES (307, '2024-12-05', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 22);
INSERT INTO `attendance_attendance` VALUES (308, '2024-12-05', '09:05:03.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 23);
INSERT INTO `attendance_attendance` VALUES (309, '2024-12-05', '08:55:07.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 24);
INSERT INTO `attendance_attendance` VALUES (310, '2024-12-05', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 25);
INSERT INTO `attendance_attendance` VALUES (311, '2024-12-05', '08:55:09.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 26);
INSERT INTO `attendance_attendance` VALUES (312, '2024-12-05', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 27);
INSERT INTO `attendance_attendance` VALUES (313, '2024-12-05', '08:55:08.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 28);
INSERT INTO `attendance_attendance` VALUES (314, '2024-12-05', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 29);
INSERT INTO `attendance_attendance` VALUES (315, '2024-12-05', '08:55:00.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 30);
INSERT INTO `attendance_attendance` VALUES (316, '2024-12-05', '08:55:07.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 31);
INSERT INTO `attendance_attendance` VALUES (317, '2024-12-05', '08:55:08.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 32);
INSERT INTO `attendance_attendance` VALUES (318, '2024-12-05', '08:55:05.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 33);
INSERT INTO `attendance_attendance` VALUES (319, '2024-12-05', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 34);
INSERT INTO `attendance_attendance` VALUES (320, '2024-12-05', '08:55:00.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 35);
INSERT INTO `attendance_attendance` VALUES (321, '2024-12-05', '08:55:03.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 36);
INSERT INTO `attendance_attendance` VALUES (322, '2024-12-05', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 37);
INSERT INTO `attendance_attendance` VALUES (323, '2024-12-05', NULL, NULL, 'absent', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 38);
INSERT INTO `attendance_attendance` VALUES (324, '2024-12-05', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 39);
INSERT INTO `attendance_attendance` VALUES (325, '2024-12-05', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 40);
INSERT INTO `attendance_attendance` VALUES (326, '2024-12-05', '09:05:19.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 41);
INSERT INTO `attendance_attendance` VALUES (327, '2024-12-05', '08:55:01.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 42);
INSERT INTO `attendance_attendance` VALUES (328, '2024-12-05', '08:55:08.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 43);
INSERT INTO `attendance_attendance` VALUES (329, '2024-12-05', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 44);
INSERT INTO `attendance_attendance` VALUES (330, '2024-12-05', '08:55:01.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 45);
INSERT INTO `attendance_attendance` VALUES (331, '2024-12-05', '08:55:01.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 46);
INSERT INTO `attendance_attendance` VALUES (332, '2024-12-05', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 47);
INSERT INTO `attendance_attendance` VALUES (333, '2024-12-05', NULL, NULL, 'absent', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 48);
INSERT INTO `attendance_attendance` VALUES (334, '2024-12-05', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 49);
INSERT INTO `attendance_attendance` VALUES (335, '2024-12-05', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 50);
INSERT INTO `attendance_attendance` VALUES (336, '2024-12-05', NULL, '17:45:09.000000', 'early', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 51);
INSERT INTO `attendance_attendance` VALUES (337, '2024-12-05', '08:55:10.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 52);
INSERT INTO `attendance_attendance` VALUES (338, '2024-12-05', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 53);
INSERT INTO `attendance_attendance` VALUES (339, '2024-12-05', '08:55:01.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 54);
INSERT INTO `attendance_attendance` VALUES (340, '2024-12-05', '08:55:01.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 55);
INSERT INTO `attendance_attendance` VALUES (341, '2024-12-05', '08:55:10.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 56);
INSERT INTO `attendance_attendance` VALUES (342, '2024-12-05', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 57);
INSERT INTO `attendance_attendance` VALUES (343, '2024-12-05', '08:55:01.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 58);
INSERT INTO `attendance_attendance` VALUES (344, '2024-12-05', '08:55:10.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 59);
INSERT INTO `attendance_attendance` VALUES (345, '2024-12-05', '08:55:07.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 60);
INSERT INTO `attendance_attendance` VALUES (346, '2024-12-05', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 61);
INSERT INTO `attendance_attendance` VALUES (347, '2024-12-05', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 62);
INSERT INTO `attendance_attendance` VALUES (348, '2024-12-05', '08:55:07.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 63);
INSERT INTO `attendance_attendance` VALUES (349, '2024-12-05', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 64);
INSERT INTO `attendance_attendance` VALUES (350, '2024-12-05', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 65);
INSERT INTO `attendance_attendance` VALUES (351, '2024-12-05', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 66);
INSERT INTO `attendance_attendance` VALUES (352, '2024-12-05', '08:55:07.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 67);
INSERT INTO `attendance_attendance` VALUES (353, '2024-12-05', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 68);
INSERT INTO `attendance_attendance` VALUES (354, '2024-12-05', NULL, '17:45:03.000000', 'early', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 69);
INSERT INTO `attendance_attendance` VALUES (355, '2024-12-05', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 70);
INSERT INTO `attendance_attendance` VALUES (356, '2024-12-05', '08:55:03.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 71);
INSERT INTO `attendance_attendance` VALUES (357, '2024-12-05', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 72);
INSERT INTO `attendance_attendance` VALUES (358, '2024-12-05', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 73);
INSERT INTO `attendance_attendance` VALUES (359, '2024-12-05', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 74);
INSERT INTO `attendance_attendance` VALUES (360, '2024-12-05', '08:55:06.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 75);
INSERT INTO `attendance_attendance` VALUES (361, '2024-12-05', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 76);
INSERT INTO `attendance_attendance` VALUES (362, '2024-12-05', NULL, NULL, 'absent', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 77);
INSERT INTO `attendance_attendance` VALUES (363, '2024-12-05', '08:55:09.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 78);
INSERT INTO `attendance_attendance` VALUES (364, '2024-12-05', '08:55:03.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 79);
INSERT INTO `attendance_attendance` VALUES (365, '2024-12-05', '09:05:26.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 80);
INSERT INTO `attendance_attendance` VALUES (366, '2024-12-05', '08:55:02.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 81);
INSERT INTO `attendance_attendance` VALUES (367, '2024-12-05', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 82);
INSERT INTO `attendance_attendance` VALUES (368, '2024-12-05', '08:55:06.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 83);
INSERT INTO `attendance_attendance` VALUES (369, '2024-12-05', '09:05:14.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 84);
INSERT INTO `attendance_attendance` VALUES (370, '2024-12-05', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 85);
INSERT INTO `attendance_attendance` VALUES (371, '2024-12-05', '08:55:01.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 86);
INSERT INTO `attendance_attendance` VALUES (372, '2024-12-05', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 87);
INSERT INTO `attendance_attendance` VALUES (373, '2024-12-05', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 88);
INSERT INTO `attendance_attendance` VALUES (374, '2024-12-05', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 89);
INSERT INTO `attendance_attendance` VALUES (375, '2024-12-05', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 90);
INSERT INTO `attendance_attendance` VALUES (376, '2024-12-05', '08:55:05.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 91);
INSERT INTO `attendance_attendance` VALUES (377, '2024-12-05', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 92);
INSERT INTO `attendance_attendance` VALUES (378, '2024-12-05', NULL, '17:45:04.000000', 'early', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 93);
INSERT INTO `attendance_attendance` VALUES (379, '2024-12-05', '09:05:15.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 94);
INSERT INTO `attendance_attendance` VALUES (380, '2024-12-05', '08:55:05.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 95);
INSERT INTO `attendance_attendance` VALUES (381, '2024-12-05', '08:55:00.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 96);
INSERT INTO `attendance_attendance` VALUES (382, '2024-12-05', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 97);
INSERT INTO `attendance_attendance` VALUES (383, '2024-12-05', '08:55:00.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 98);
INSERT INTO `attendance_attendance` VALUES (384, '2024-12-05', '08:55:01.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 99);
INSERT INTO `attendance_attendance` VALUES (385, '2024-12-05', '08:55:02.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 100);
INSERT INTO `attendance_attendance` VALUES (386, '2024-12-06', '08:55:08.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 5);
INSERT INTO `attendance_attendance` VALUES (387, '2024-12-06', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 6);
INSERT INTO `attendance_attendance` VALUES (388, '2024-12-06', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 7);
INSERT INTO `attendance_attendance` VALUES (389, '2024-12-06', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 8);
INSERT INTO `attendance_attendance` VALUES (390, '2024-12-06', NULL, NULL, 'absent', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 9);
INSERT INTO `attendance_attendance` VALUES (391, '2024-12-06', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 10);
INSERT INTO `attendance_attendance` VALUES (392, '2024-12-06', '08:55:00.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 11);
INSERT INTO `attendance_attendance` VALUES (393, '2024-12-06', '09:05:04.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 12);
INSERT INTO `attendance_attendance` VALUES (394, '2024-12-06', '08:55:01.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 13);
INSERT INTO `attendance_attendance` VALUES (395, '2024-12-06', '09:05:09.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 14);
INSERT INTO `attendance_attendance` VALUES (396, '2024-12-06', NULL, '17:45:08.000000', 'early', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 15);
INSERT INTO `attendance_attendance` VALUES (397, '2024-12-06', '08:55:02.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 16);
INSERT INTO `attendance_attendance` VALUES (398, '2024-12-06', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 17);
INSERT INTO `attendance_attendance` VALUES (399, '2024-12-06', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 18);
INSERT INTO `attendance_attendance` VALUES (400, '2024-12-06', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 19);
INSERT INTO `attendance_attendance` VALUES (401, '2024-12-06', '08:55:02.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 20);
INSERT INTO `attendance_attendance` VALUES (402, '2024-12-06', '08:55:08.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 21);
INSERT INTO `attendance_attendance` VALUES (403, '2024-12-06', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 22);
INSERT INTO `attendance_attendance` VALUES (404, '2024-12-06', '08:55:01.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 23);
INSERT INTO `attendance_attendance` VALUES (405, '2024-12-06', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 24);
INSERT INTO `attendance_attendance` VALUES (406, '2024-12-06', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 25);
INSERT INTO `attendance_attendance` VALUES (407, '2024-12-06', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 26);
INSERT INTO `attendance_attendance` VALUES (408, '2024-12-06', '08:55:02.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 27);
INSERT INTO `attendance_attendance` VALUES (409, '2024-12-06', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 28);
INSERT INTO `attendance_attendance` VALUES (410, '2024-12-06', '08:55:09.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 29);
INSERT INTO `attendance_attendance` VALUES (411, '2024-12-06', '08:55:07.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 30);
INSERT INTO `attendance_attendance` VALUES (412, '2024-12-06', '08:55:07.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 31);
INSERT INTO `attendance_attendance` VALUES (413, '2024-12-06', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 32);
INSERT INTO `attendance_attendance` VALUES (414, '2024-12-06', '08:55:01.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 33);
INSERT INTO `attendance_attendance` VALUES (415, '2024-12-06', '09:05:14.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 34);
INSERT INTO `attendance_attendance` VALUES (416, '2024-12-06', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 35);
INSERT INTO `attendance_attendance` VALUES (417, '2024-12-06', '08:55:10.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 36);
INSERT INTO `attendance_attendance` VALUES (418, '2024-12-06', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 37);
INSERT INTO `attendance_attendance` VALUES (419, '2024-12-06', '08:55:00.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 38);
INSERT INTO `attendance_attendance` VALUES (420, '2024-12-06', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 39);
INSERT INTO `attendance_attendance` VALUES (421, '2024-12-06', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 40);
INSERT INTO `attendance_attendance` VALUES (422, '2024-12-06', '08:55:05.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 41);
INSERT INTO `attendance_attendance` VALUES (423, '2024-12-06', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 42);
INSERT INTO `attendance_attendance` VALUES (424, '2024-12-06', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 43);
INSERT INTO `attendance_attendance` VALUES (425, '2024-12-06', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 44);
INSERT INTO `attendance_attendance` VALUES (426, '2024-12-06', '08:55:04.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 45);
INSERT INTO `attendance_attendance` VALUES (427, '2024-12-06', '08:55:05.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 46);
INSERT INTO `attendance_attendance` VALUES (428, '2024-12-06', '08:55:04.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 47);
INSERT INTO `attendance_attendance` VALUES (429, '2024-12-06', '08:55:06.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 48);
INSERT INTO `attendance_attendance` VALUES (430, '2024-12-06', '08:55:09.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 49);
INSERT INTO `attendance_attendance` VALUES (431, '2024-12-06', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 50);
INSERT INTO `attendance_attendance` VALUES (432, '2024-12-06', '09:05:16.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 51);
INSERT INTO `attendance_attendance` VALUES (433, '2024-12-06', '08:55:03.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 52);
INSERT INTO `attendance_attendance` VALUES (434, '2024-12-06', '08:55:01.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 53);
INSERT INTO `attendance_attendance` VALUES (435, '2024-12-06', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 54);
INSERT INTO `attendance_attendance` VALUES (436, '2024-12-06', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 55);
INSERT INTO `attendance_attendance` VALUES (437, '2024-12-06', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 56);
INSERT INTO `attendance_attendance` VALUES (438, '2024-12-06', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 57);
INSERT INTO `attendance_attendance` VALUES (439, '2024-12-06', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 58);
INSERT INTO `attendance_attendance` VALUES (440, '2024-12-06', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 59);
INSERT INTO `attendance_attendance` VALUES (441, '2024-12-06', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 60);
INSERT INTO `attendance_attendance` VALUES (442, '2024-12-06', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 61);
INSERT INTO `attendance_attendance` VALUES (443, '2024-12-06', '08:55:06.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 62);
INSERT INTO `attendance_attendance` VALUES (444, '2024-12-06', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 63);
INSERT INTO `attendance_attendance` VALUES (445, '2024-12-06', '08:55:05.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 64);
INSERT INTO `attendance_attendance` VALUES (446, '2024-12-06', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 65);
INSERT INTO `attendance_attendance` VALUES (447, '2024-12-06', '08:55:07.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 66);
INSERT INTO `attendance_attendance` VALUES (448, '2024-12-06', '09:05:23.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 67);
INSERT INTO `attendance_attendance` VALUES (449, '2024-12-06', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 68);
INSERT INTO `attendance_attendance` VALUES (450, '2024-12-06', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 69);
INSERT INTO `attendance_attendance` VALUES (451, '2024-12-06', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 70);
INSERT INTO `attendance_attendance` VALUES (452, '2024-12-06', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 71);
INSERT INTO `attendance_attendance` VALUES (453, '2024-12-06', '08:55:06.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 72);
INSERT INTO `attendance_attendance` VALUES (454, '2024-12-06', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 73);
INSERT INTO `attendance_attendance` VALUES (455, '2024-12-06', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 74);
INSERT INTO `attendance_attendance` VALUES (456, '2024-12-06', '08:55:02.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 75);
INSERT INTO `attendance_attendance` VALUES (457, '2024-12-06', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 76);
INSERT INTO `attendance_attendance` VALUES (458, '2024-12-06', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 77);
INSERT INTO `attendance_attendance` VALUES (459, '2024-12-06', '08:55:07.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 78);
INSERT INTO `attendance_attendance` VALUES (460, '2024-12-06', '08:55:00.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 79);
INSERT INTO `attendance_attendance` VALUES (461, '2024-12-06', NULL, '17:45:08.000000', 'early', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 80);
INSERT INTO `attendance_attendance` VALUES (462, '2024-12-06', '08:55:08.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 81);
INSERT INTO `attendance_attendance` VALUES (463, '2024-12-06', '09:05:17.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 82);
INSERT INTO `attendance_attendance` VALUES (464, '2024-12-06', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 83);
INSERT INTO `attendance_attendance` VALUES (465, '2024-12-06', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 84);
INSERT INTO `attendance_attendance` VALUES (466, '2024-12-06', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 85);
INSERT INTO `attendance_attendance` VALUES (467, '2024-12-06', NULL, '17:45:03.000000', 'early', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 86);
INSERT INTO `attendance_attendance` VALUES (468, '2024-12-06', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 87);
INSERT INTO `attendance_attendance` VALUES (469, '2024-12-06', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 88);
INSERT INTO `attendance_attendance` VALUES (470, '2024-12-06', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 89);
INSERT INTO `attendance_attendance` VALUES (471, '2024-12-06', '08:55:10.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 90);
INSERT INTO `attendance_attendance` VALUES (472, '2024-12-06', '09:05:10.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 91);
INSERT INTO `attendance_attendance` VALUES (473, '2024-12-06', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 92);
INSERT INTO `attendance_attendance` VALUES (474, '2024-12-06', '08:55:00.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 93);
INSERT INTO `attendance_attendance` VALUES (475, '2024-12-06', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 94);
INSERT INTO `attendance_attendance` VALUES (476, '2024-12-06', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 95);
INSERT INTO `attendance_attendance` VALUES (477, '2024-12-06', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 96);
INSERT INTO `attendance_attendance` VALUES (478, '2024-12-06', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 97);
INSERT INTO `attendance_attendance` VALUES (479, '2024-12-06', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 98);
INSERT INTO `attendance_attendance` VALUES (480, '2024-12-06', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 99);
INSERT INTO `attendance_attendance` VALUES (481, '2024-12-06', '08:55:06.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 100);
INSERT INTO `attendance_attendance` VALUES (482, '2024-12-09', '08:55:08.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 5);
INSERT INTO `attendance_attendance` VALUES (483, '2024-12-09', '08:55:01.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 6);
INSERT INTO `attendance_attendance` VALUES (484, '2024-12-09', '08:55:03.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 7);
INSERT INTO `attendance_attendance` VALUES (485, '2024-12-09', '08:55:05.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 8);
INSERT INTO `attendance_attendance` VALUES (486, '2024-12-09', '08:55:01.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 9);
INSERT INTO `attendance_attendance` VALUES (487, '2024-12-09', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 10);
INSERT INTO `attendance_attendance` VALUES (488, '2024-12-09', '09:05:22.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 11);
INSERT INTO `attendance_attendance` VALUES (489, '2024-12-09', '09:05:04.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 12);
INSERT INTO `attendance_attendance` VALUES (490, '2024-12-09', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 13);
INSERT INTO `attendance_attendance` VALUES (491, '2024-12-09', '08:55:10.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 14);
INSERT INTO `attendance_attendance` VALUES (492, '2024-12-09', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 15);
INSERT INTO `attendance_attendance` VALUES (493, '2024-12-09', '09:05:20.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 16);
INSERT INTO `attendance_attendance` VALUES (494, '2024-12-09', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 17);
INSERT INTO `attendance_attendance` VALUES (495, '2024-12-09', '08:55:08.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 18);
INSERT INTO `attendance_attendance` VALUES (496, '2024-12-09', '09:05:05.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 19);
INSERT INTO `attendance_attendance` VALUES (497, '2024-12-09', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 20);
INSERT INTO `attendance_attendance` VALUES (498, '2024-12-09', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 21);
INSERT INTO `attendance_attendance` VALUES (499, '2024-12-09', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 22);
INSERT INTO `attendance_attendance` VALUES (500, '2024-12-09', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 23);
INSERT INTO `attendance_attendance` VALUES (501, '2024-12-09', '08:55:02.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 24);
INSERT INTO `attendance_attendance` VALUES (502, '2024-12-09', '08:55:05.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 25);
INSERT INTO `attendance_attendance` VALUES (503, '2024-12-09', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 26);
INSERT INTO `attendance_attendance` VALUES (504, '2024-12-09', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 27);
INSERT INTO `attendance_attendance` VALUES (505, '2024-12-09', '09:05:17.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 28);
INSERT INTO `attendance_attendance` VALUES (506, '2024-12-09', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 29);
INSERT INTO `attendance_attendance` VALUES (507, '2024-12-09', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 30);
INSERT INTO `attendance_attendance` VALUES (508, '2024-12-09', '09:05:06.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 31);
INSERT INTO `attendance_attendance` VALUES (509, '2024-12-09', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 32);
INSERT INTO `attendance_attendance` VALUES (510, '2024-12-09', '09:05:19.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 33);
INSERT INTO `attendance_attendance` VALUES (511, '2024-12-09', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 34);
INSERT INTO `attendance_attendance` VALUES (512, '2024-12-09', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 35);
INSERT INTO `attendance_attendance` VALUES (513, '2024-12-09', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 36);
INSERT INTO `attendance_attendance` VALUES (514, '2024-12-09', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 37);
INSERT INTO `attendance_attendance` VALUES (515, '2024-12-09', NULL, '17:45:08.000000', 'early', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 38);
INSERT INTO `attendance_attendance` VALUES (516, '2024-12-09', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 39);
INSERT INTO `attendance_attendance` VALUES (517, '2024-12-09', '08:55:06.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 40);
INSERT INTO `attendance_attendance` VALUES (518, '2024-12-09', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 41);
INSERT INTO `attendance_attendance` VALUES (519, '2024-12-09', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 42);
INSERT INTO `attendance_attendance` VALUES (520, '2024-12-09', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 43);
INSERT INTO `attendance_attendance` VALUES (521, '2024-12-09', '09:05:17.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 44);
INSERT INTO `attendance_attendance` VALUES (522, '2024-12-09', '08:55:09.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 45);
INSERT INTO `attendance_attendance` VALUES (523, '2024-12-09', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 46);
INSERT INTO `attendance_attendance` VALUES (524, '2024-12-09', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 47);
INSERT INTO `attendance_attendance` VALUES (525, '2024-12-09', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 48);
INSERT INTO `attendance_attendance` VALUES (526, '2024-12-09', '08:55:06.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 49);
INSERT INTO `attendance_attendance` VALUES (527, '2024-12-09', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 50);
INSERT INTO `attendance_attendance` VALUES (528, '2024-12-09', '09:05:18.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 51);
INSERT INTO `attendance_attendance` VALUES (529, '2024-12-09', '08:55:09.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 52);
INSERT INTO `attendance_attendance` VALUES (530, '2024-12-09', '09:05:27.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 53);
INSERT INTO `attendance_attendance` VALUES (531, '2024-12-09', NULL, '17:45:01.000000', 'early', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 54);
INSERT INTO `attendance_attendance` VALUES (532, '2024-12-09', '08:55:00.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 55);
INSERT INTO `attendance_attendance` VALUES (533, '2024-12-09', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 56);
INSERT INTO `attendance_attendance` VALUES (534, '2024-12-09', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 57);
INSERT INTO `attendance_attendance` VALUES (535, '2024-12-09', '09:05:14.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 58);
INSERT INTO `attendance_attendance` VALUES (536, '2024-12-09', '08:55:01.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 59);
INSERT INTO `attendance_attendance` VALUES (537, '2024-12-09', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 60);
INSERT INTO `attendance_attendance` VALUES (538, '2024-12-09', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 61);
INSERT INTO `attendance_attendance` VALUES (539, '2024-12-09', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 62);
INSERT INTO `attendance_attendance` VALUES (540, '2024-12-09', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 63);
INSERT INTO `attendance_attendance` VALUES (541, '2024-12-09', '08:55:06.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 64);
INSERT INTO `attendance_attendance` VALUES (542, '2024-12-09', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 65);
INSERT INTO `attendance_attendance` VALUES (543, '2024-12-09', NULL, '17:45:07.000000', 'early', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 66);
INSERT INTO `attendance_attendance` VALUES (544, '2024-12-09', '08:55:01.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 67);
INSERT INTO `attendance_attendance` VALUES (545, '2024-12-09', '08:55:04.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 68);
INSERT INTO `attendance_attendance` VALUES (546, '2024-12-09', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 69);
INSERT INTO `attendance_attendance` VALUES (547, '2024-12-09', '08:55:05.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 70);
INSERT INTO `attendance_attendance` VALUES (548, '2024-12-09', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 71);
INSERT INTO `attendance_attendance` VALUES (549, '2024-12-09', '08:55:08.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 72);
INSERT INTO `attendance_attendance` VALUES (550, '2024-12-09', '09:05:26.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 73);
INSERT INTO `attendance_attendance` VALUES (551, '2024-12-09', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 74);
INSERT INTO `attendance_attendance` VALUES (552, '2024-12-09', NULL, '17:45:00.000000', 'early', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 75);
INSERT INTO `attendance_attendance` VALUES (553, '2024-12-09', '08:55:08.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 76);
INSERT INTO `attendance_attendance` VALUES (554, '2024-12-09', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 77);
INSERT INTO `attendance_attendance` VALUES (555, '2024-12-09', '08:55:06.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 78);
INSERT INTO `attendance_attendance` VALUES (556, '2024-12-09', '08:55:00.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 79);
INSERT INTO `attendance_attendance` VALUES (557, '2024-12-09', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 80);
INSERT INTO `attendance_attendance` VALUES (558, '2024-12-09', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 81);
INSERT INTO `attendance_attendance` VALUES (559, '2024-12-09', '08:55:03.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 82);
INSERT INTO `attendance_attendance` VALUES (560, '2024-12-09', '08:55:00.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 83);
INSERT INTO `attendance_attendance` VALUES (561, '2024-12-09', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 84);
INSERT INTO `attendance_attendance` VALUES (562, '2024-12-09', '09:05:13.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 85);
INSERT INTO `attendance_attendance` VALUES (563, '2024-12-09', '08:55:02.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 86);
INSERT INTO `attendance_attendance` VALUES (564, '2024-12-09', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 87);
INSERT INTO `attendance_attendance` VALUES (565, '2024-12-09', '08:55:00.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 88);
INSERT INTO `attendance_attendance` VALUES (566, '2024-12-09', '08:55:00.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 89);
INSERT INTO `attendance_attendance` VALUES (567, '2024-12-09', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 90);
INSERT INTO `attendance_attendance` VALUES (568, '2024-12-09', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 91);
INSERT INTO `attendance_attendance` VALUES (569, '2024-12-09', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 92);
INSERT INTO `attendance_attendance` VALUES (570, '2024-12-09', '08:55:00.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 93);
INSERT INTO `attendance_attendance` VALUES (571, '2024-12-09', '09:05:17.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 94);
INSERT INTO `attendance_attendance` VALUES (572, '2024-12-09', '08:55:06.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 95);
INSERT INTO `attendance_attendance` VALUES (573, '2024-12-09', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 96);
INSERT INTO `attendance_attendance` VALUES (574, '2024-12-09', '09:05:29.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 97);
INSERT INTO `attendance_attendance` VALUES (575, '2024-12-09', NULL, NULL, 'absent', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 98);
INSERT INTO `attendance_attendance` VALUES (576, '2024-12-09', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 99);
INSERT INTO `attendance_attendance` VALUES (577, '2024-12-09', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 100);
INSERT INTO `attendance_attendance` VALUES (578, '2024-12-10', '08:55:07.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 5);
INSERT INTO `attendance_attendance` VALUES (579, '2024-12-10', '09:05:21.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 6);
INSERT INTO `attendance_attendance` VALUES (580, '2024-12-10', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 7);
INSERT INTO `attendance_attendance` VALUES (581, '2024-12-10', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 8);
INSERT INTO `attendance_attendance` VALUES (582, '2024-12-10', '08:55:10.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 9);
INSERT INTO `attendance_attendance` VALUES (583, '2024-12-10', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 10);
INSERT INTO `attendance_attendance` VALUES (584, '2024-12-10', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 11);
INSERT INTO `attendance_attendance` VALUES (585, '2024-12-10', '08:55:07.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 12);
INSERT INTO `attendance_attendance` VALUES (586, '2024-12-10', '09:05:14.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 13);
INSERT INTO `attendance_attendance` VALUES (587, '2024-12-10', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 14);
INSERT INTO `attendance_attendance` VALUES (588, '2024-12-10', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 15);
INSERT INTO `attendance_attendance` VALUES (589, '2024-12-10', '09:05:05.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 16);
INSERT INTO `attendance_attendance` VALUES (590, '2024-12-10', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 17);
INSERT INTO `attendance_attendance` VALUES (591, '2024-12-10', '08:55:06.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 18);
INSERT INTO `attendance_attendance` VALUES (592, '2024-12-10', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 19);
INSERT INTO `attendance_attendance` VALUES (593, '2024-12-10', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 20);
INSERT INTO `attendance_attendance` VALUES (594, '2024-12-10', '09:05:09.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 21);
INSERT INTO `attendance_attendance` VALUES (595, '2024-12-10', '08:55:09.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 22);
INSERT INTO `attendance_attendance` VALUES (596, '2024-12-10', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 23);
INSERT INTO `attendance_attendance` VALUES (597, '2024-12-10', '08:55:10.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 24);
INSERT INTO `attendance_attendance` VALUES (598, '2024-12-10', '09:05:10.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 25);
INSERT INTO `attendance_attendance` VALUES (599, '2024-12-10', NULL, '17:45:09.000000', 'early', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 26);
INSERT INTO `attendance_attendance` VALUES (600, '2024-12-10', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 27);
INSERT INTO `attendance_attendance` VALUES (601, '2024-12-10', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 28);
INSERT INTO `attendance_attendance` VALUES (602, '2024-12-10', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 29);
INSERT INTO `attendance_attendance` VALUES (603, '2024-12-10', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 30);
INSERT INTO `attendance_attendance` VALUES (604, '2024-12-10', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 31);
INSERT INTO `attendance_attendance` VALUES (605, '2024-12-10', '09:05:18.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 32);
INSERT INTO `attendance_attendance` VALUES (606, '2024-12-10', '08:55:02.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 33);
INSERT INTO `attendance_attendance` VALUES (607, '2024-12-10', '08:55:01.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 34);
INSERT INTO `attendance_attendance` VALUES (608, '2024-12-10', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 35);
INSERT INTO `attendance_attendance` VALUES (609, '2024-12-10', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 36);
INSERT INTO `attendance_attendance` VALUES (610, '2024-12-10', '08:55:08.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 37);
INSERT INTO `attendance_attendance` VALUES (611, '2024-12-10', '08:55:03.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 38);
INSERT INTO `attendance_attendance` VALUES (612, '2024-12-10', '08:55:08.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 39);
INSERT INTO `attendance_attendance` VALUES (613, '2024-12-10', '08:55:06.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 40);
INSERT INTO `attendance_attendance` VALUES (614, '2024-12-10', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 41);
INSERT INTO `attendance_attendance` VALUES (615, '2024-12-10', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 42);
INSERT INTO `attendance_attendance` VALUES (616, '2024-12-10', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 43);
INSERT INTO `attendance_attendance` VALUES (617, '2024-12-10', '08:55:10.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 44);
INSERT INTO `attendance_attendance` VALUES (618, '2024-12-10', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 45);
INSERT INTO `attendance_attendance` VALUES (619, '2024-12-10', '08:55:07.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 46);
INSERT INTO `attendance_attendance` VALUES (620, '2024-12-10', '09:05:23.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 47);
INSERT INTO `attendance_attendance` VALUES (621, '2024-12-10', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 48);
INSERT INTO `attendance_attendance` VALUES (622, '2024-12-10', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 49);
INSERT INTO `attendance_attendance` VALUES (623, '2024-12-10', '08:55:01.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 50);
INSERT INTO `attendance_attendance` VALUES (624, '2024-12-10', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 51);
INSERT INTO `attendance_attendance` VALUES (625, '2024-12-10', NULL, NULL, 'absent', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 52);
INSERT INTO `attendance_attendance` VALUES (626, '2024-12-10', '09:05:12.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 53);
INSERT INTO `attendance_attendance` VALUES (627, '2024-12-10', '08:55:00.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 54);
INSERT INTO `attendance_attendance` VALUES (628, '2024-12-10', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 55);
INSERT INTO `attendance_attendance` VALUES (629, '2024-12-10', '08:55:10.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 56);
INSERT INTO `attendance_attendance` VALUES (630, '2024-12-10', NULL, NULL, 'absent', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 57);
INSERT INTO `attendance_attendance` VALUES (631, '2024-12-10', '08:55:10.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 58);
INSERT INTO `attendance_attendance` VALUES (632, '2024-12-10', NULL, '17:45:01.000000', 'early', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 59);
INSERT INTO `attendance_attendance` VALUES (633, '2024-12-10', '08:55:10.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 60);
INSERT INTO `attendance_attendance` VALUES (634, '2024-12-10', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 61);
INSERT INTO `attendance_attendance` VALUES (635, '2024-12-10', '08:55:09.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 62);
INSERT INTO `attendance_attendance` VALUES (636, '2024-12-10', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 63);
INSERT INTO `attendance_attendance` VALUES (637, '2024-12-10', '08:55:07.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 64);
INSERT INTO `attendance_attendance` VALUES (638, '2024-12-10', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 65);
INSERT INTO `attendance_attendance` VALUES (639, '2024-12-10', '08:55:10.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 66);
INSERT INTO `attendance_attendance` VALUES (640, '2024-12-10', '08:55:10.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 67);
INSERT INTO `attendance_attendance` VALUES (641, '2024-12-10', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 68);
INSERT INTO `attendance_attendance` VALUES (642, '2024-12-10', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 69);
INSERT INTO `attendance_attendance` VALUES (643, '2024-12-10', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 70);
INSERT INTO `attendance_attendance` VALUES (644, '2024-12-10', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 71);
INSERT INTO `attendance_attendance` VALUES (645, '2024-12-10', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 72);
INSERT INTO `attendance_attendance` VALUES (646, '2024-12-10', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 73);
INSERT INTO `attendance_attendance` VALUES (647, '2024-12-10', '09:05:09.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 74);
INSERT INTO `attendance_attendance` VALUES (648, '2024-12-10', '08:55:08.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 75);
INSERT INTO `attendance_attendance` VALUES (649, '2024-12-10', '08:55:06.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 76);
INSERT INTO `attendance_attendance` VALUES (650, '2024-12-10', '08:55:02.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 77);
INSERT INTO `attendance_attendance` VALUES (651, '2024-12-10', '08:55:10.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 78);
INSERT INTO `attendance_attendance` VALUES (652, '2024-12-10', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 79);
INSERT INTO `attendance_attendance` VALUES (653, '2024-12-10', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 80);
INSERT INTO `attendance_attendance` VALUES (654, '2024-12-10', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 81);
INSERT INTO `attendance_attendance` VALUES (655, '2024-12-10', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 82);
INSERT INTO `attendance_attendance` VALUES (656, '2024-12-10', '08:55:10.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 83);
INSERT INTO `attendance_attendance` VALUES (657, '2024-12-10', '08:55:05.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 84);
INSERT INTO `attendance_attendance` VALUES (658, '2024-12-10', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 85);
INSERT INTO `attendance_attendance` VALUES (659, '2024-12-10', '09:05:04.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 86);
INSERT INTO `attendance_attendance` VALUES (660, '2024-12-10', '08:55:00.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 87);
INSERT INTO `attendance_attendance` VALUES (661, '2024-12-10', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 88);
INSERT INTO `attendance_attendance` VALUES (662, '2024-12-10', '09:05:17.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 89);
INSERT INTO `attendance_attendance` VALUES (663, '2024-12-10', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 90);
INSERT INTO `attendance_attendance` VALUES (664, '2024-12-10', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 91);
INSERT INTO `attendance_attendance` VALUES (665, '2024-12-10', '08:55:09.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 92);
INSERT INTO `attendance_attendance` VALUES (666, '2024-12-10', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 93);
INSERT INTO `attendance_attendance` VALUES (667, '2024-12-10', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 94);
INSERT INTO `attendance_attendance` VALUES (668, '2024-12-10', '08:55:01.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 95);
INSERT INTO `attendance_attendance` VALUES (669, '2024-12-10', '09:05:06.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 96);
INSERT INTO `attendance_attendance` VALUES (670, '2024-12-10', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 97);
INSERT INTO `attendance_attendance` VALUES (671, '2024-12-10', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 98);
INSERT INTO `attendance_attendance` VALUES (672, '2024-12-10', '09:05:30.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 99);
INSERT INTO `attendance_attendance` VALUES (673, '2024-12-10', '08:55:00.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 100);
INSERT INTO `attendance_attendance` VALUES (674, '2024-12-11', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 5);
INSERT INTO `attendance_attendance` VALUES (675, '2024-12-11', '08:55:08.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 6);
INSERT INTO `attendance_attendance` VALUES (676, '2024-12-11', '08:55:03.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 7);
INSERT INTO `attendance_attendance` VALUES (677, '2024-12-11', '08:55:05.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 8);
INSERT INTO `attendance_attendance` VALUES (678, '2024-12-11', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 9);
INSERT INTO `attendance_attendance` VALUES (679, '2024-12-11', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 10);
INSERT INTO `attendance_attendance` VALUES (680, '2024-12-11', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 11);
INSERT INTO `attendance_attendance` VALUES (681, '2024-12-11', '08:55:06.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 12);
INSERT INTO `attendance_attendance` VALUES (682, '2024-12-11', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 13);
INSERT INTO `attendance_attendance` VALUES (683, '2024-12-11', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 14);
INSERT INTO `attendance_attendance` VALUES (684, '2024-12-11', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 15);
INSERT INTO `attendance_attendance` VALUES (685, '2024-12-11', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 16);
INSERT INTO `attendance_attendance` VALUES (686, '2024-12-11', '08:55:04.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 17);
INSERT INTO `attendance_attendance` VALUES (687, '2024-12-11', '08:55:10.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 18);
INSERT INTO `attendance_attendance` VALUES (688, '2024-12-11', '08:55:10.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 19);
INSERT INTO `attendance_attendance` VALUES (689, '2024-12-11', '08:55:02.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 20);
INSERT INTO `attendance_attendance` VALUES (690, '2024-12-11', '08:55:01.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 21);
INSERT INTO `attendance_attendance` VALUES (691, '2024-12-11', '08:55:07.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 22);
INSERT INTO `attendance_attendance` VALUES (692, '2024-12-11', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 23);
INSERT INTO `attendance_attendance` VALUES (693, '2024-12-11', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 24);
INSERT INTO `attendance_attendance` VALUES (694, '2024-12-11', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 25);
INSERT INTO `attendance_attendance` VALUES (695, '2024-12-11', '08:55:08.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 26);
INSERT INTO `attendance_attendance` VALUES (696, '2024-12-11', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 27);
INSERT INTO `attendance_attendance` VALUES (697, '2024-12-11', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 28);
INSERT INTO `attendance_attendance` VALUES (698, '2024-12-11', '08:55:10.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 29);
INSERT INTO `attendance_attendance` VALUES (699, '2024-12-11', '08:55:07.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 30);
INSERT INTO `attendance_attendance` VALUES (700, '2024-12-11', NULL, '17:45:06.000000', 'early', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 31);
INSERT INTO `attendance_attendance` VALUES (701, '2024-12-11', '08:55:01.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 32);
INSERT INTO `attendance_attendance` VALUES (702, '2024-12-11', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 33);
INSERT INTO `attendance_attendance` VALUES (703, '2024-12-11', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 34);
INSERT INTO `attendance_attendance` VALUES (704, '2024-12-11', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 35);
INSERT INTO `attendance_attendance` VALUES (705, '2024-12-11', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 36);
INSERT INTO `attendance_attendance` VALUES (706, '2024-12-11', '08:55:08.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 37);
INSERT INTO `attendance_attendance` VALUES (707, '2024-12-11', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 38);
INSERT INTO `attendance_attendance` VALUES (708, '2024-12-11', NULL, '17:45:05.000000', 'early', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 39);
INSERT INTO `attendance_attendance` VALUES (709, '2024-12-11', '08:55:08.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 40);
INSERT INTO `attendance_attendance` VALUES (710, '2024-12-11', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 41);
INSERT INTO `attendance_attendance` VALUES (711, '2024-12-11', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 42);
INSERT INTO `attendance_attendance` VALUES (712, '2024-12-11', '08:55:00.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 43);
INSERT INTO `attendance_attendance` VALUES (713, '2024-12-11', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 44);
INSERT INTO `attendance_attendance` VALUES (714, '2024-12-11', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 45);
INSERT INTO `attendance_attendance` VALUES (715, '2024-12-11', '08:55:00.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 46);
INSERT INTO `attendance_attendance` VALUES (716, '2024-12-11', '09:05:03.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 47);
INSERT INTO `attendance_attendance` VALUES (717, '2024-12-11', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 48);
INSERT INTO `attendance_attendance` VALUES (718, '2024-12-11', '08:55:02.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 49);
INSERT INTO `attendance_attendance` VALUES (719, '2024-12-11', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 50);
INSERT INTO `attendance_attendance` VALUES (720, '2024-12-11', '08:55:00.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 51);
INSERT INTO `attendance_attendance` VALUES (721, '2024-12-11', '08:55:03.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 52);
INSERT INTO `attendance_attendance` VALUES (722, '2024-12-11', '09:05:14.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 53);
INSERT INTO `attendance_attendance` VALUES (723, '2024-12-11', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 54);
INSERT INTO `attendance_attendance` VALUES (724, '2024-12-11', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 55);
INSERT INTO `attendance_attendance` VALUES (725, '2024-12-11', '08:55:08.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 56);
INSERT INTO `attendance_attendance` VALUES (726, '2024-12-11', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 57);
INSERT INTO `attendance_attendance` VALUES (727, '2024-12-11', '09:05:00.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 58);
INSERT INTO `attendance_attendance` VALUES (728, '2024-12-11', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 59);
INSERT INTO `attendance_attendance` VALUES (729, '2024-12-11', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 60);
INSERT INTO `attendance_attendance` VALUES (730, '2024-12-11', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 61);
INSERT INTO `attendance_attendance` VALUES (731, '2024-12-11', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 62);
INSERT INTO `attendance_attendance` VALUES (732, '2024-12-11', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 63);
INSERT INTO `attendance_attendance` VALUES (733, '2024-12-11', '08:55:01.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 64);
INSERT INTO `attendance_attendance` VALUES (734, '2024-12-11', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 65);
INSERT INTO `attendance_attendance` VALUES (735, '2024-12-11', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 66);
INSERT INTO `attendance_attendance` VALUES (736, '2024-12-11', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 67);
INSERT INTO `attendance_attendance` VALUES (737, '2024-12-11', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 68);
INSERT INTO `attendance_attendance` VALUES (738, '2024-12-11', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 69);
INSERT INTO `attendance_attendance` VALUES (739, '2024-12-11', '09:05:10.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 70);
INSERT INTO `attendance_attendance` VALUES (740, '2024-12-11', NULL, '17:45:07.000000', 'early', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 71);
INSERT INTO `attendance_attendance` VALUES (741, '2024-12-11', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 72);
INSERT INTO `attendance_attendance` VALUES (742, '2024-12-11', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 73);
INSERT INTO `attendance_attendance` VALUES (743, '2024-12-11', '08:55:05.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 74);
INSERT INTO `attendance_attendance` VALUES (744, '2024-12-11', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 75);
INSERT INTO `attendance_attendance` VALUES (745, '2024-12-11', '08:55:06.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 76);
INSERT INTO `attendance_attendance` VALUES (746, '2024-12-11', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 77);
INSERT INTO `attendance_attendance` VALUES (747, '2024-12-11', '08:55:10.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 78);
INSERT INTO `attendance_attendance` VALUES (748, '2024-12-11', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 79);
INSERT INTO `attendance_attendance` VALUES (749, '2024-12-11', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 80);
INSERT INTO `attendance_attendance` VALUES (750, '2024-12-11', '08:55:01.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 81);
INSERT INTO `attendance_attendance` VALUES (751, '2024-12-11', '08:55:08.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 82);
INSERT INTO `attendance_attendance` VALUES (752, '2024-12-11', '08:55:03.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 83);
INSERT INTO `attendance_attendance` VALUES (753, '2024-12-11', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 84);
INSERT INTO `attendance_attendance` VALUES (754, '2024-12-11', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 85);
INSERT INTO `attendance_attendance` VALUES (755, '2024-12-11', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 86);
INSERT INTO `attendance_attendance` VALUES (756, '2024-12-11', '09:05:27.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 87);
INSERT INTO `attendance_attendance` VALUES (757, '2024-12-11', '09:05:17.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 88);
INSERT INTO `attendance_attendance` VALUES (758, '2024-12-11', '08:55:03.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 89);
INSERT INTO `attendance_attendance` VALUES (759, '2024-12-11', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 90);
INSERT INTO `attendance_attendance` VALUES (760, '2024-12-11', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 91);
INSERT INTO `attendance_attendance` VALUES (761, '2024-12-11', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 92);
INSERT INTO `attendance_attendance` VALUES (762, '2024-12-11', '08:55:09.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 93);
INSERT INTO `attendance_attendance` VALUES (763, '2024-12-11', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 94);
INSERT INTO `attendance_attendance` VALUES (764, '2024-12-11', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 95);
INSERT INTO `attendance_attendance` VALUES (765, '2024-12-11', '09:05:07.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 96);
INSERT INTO `attendance_attendance` VALUES (766, '2024-12-11', '08:55:00.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 97);
INSERT INTO `attendance_attendance` VALUES (767, '2024-12-11', '08:55:07.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 98);
INSERT INTO `attendance_attendance` VALUES (768, '2024-12-11', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 99);
INSERT INTO `attendance_attendance` VALUES (769, '2024-12-11', '09:05:12.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 100);
INSERT INTO `attendance_attendance` VALUES (770, '2024-12-12', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 5);
INSERT INTO `attendance_attendance` VALUES (771, '2024-12-12', NULL, '17:45:09.000000', 'early', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 6);
INSERT INTO `attendance_attendance` VALUES (772, '2024-12-12', '08:55:00.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 7);
INSERT INTO `attendance_attendance` VALUES (773, '2024-12-12', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 8);
INSERT INTO `attendance_attendance` VALUES (774, '2024-12-12', '08:55:00.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 9);
INSERT INTO `attendance_attendance` VALUES (775, '2024-12-12', '08:55:01.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 10);
INSERT INTO `attendance_attendance` VALUES (776, '2024-12-12', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 11);
INSERT INTO `attendance_attendance` VALUES (777, '2024-12-12', '09:05:15.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 12);
INSERT INTO `attendance_attendance` VALUES (778, '2024-12-12', '09:05:04.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 13);
INSERT INTO `attendance_attendance` VALUES (779, '2024-12-12', '09:05:29.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 14);
INSERT INTO `attendance_attendance` VALUES (780, '2024-12-12', '08:55:00.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 15);
INSERT INTO `attendance_attendance` VALUES (781, '2024-12-12', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 16);
INSERT INTO `attendance_attendance` VALUES (782, '2024-12-12', NULL, '17:45:04.000000', 'early', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 17);
INSERT INTO `attendance_attendance` VALUES (783, '2024-12-12', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 18);
INSERT INTO `attendance_attendance` VALUES (784, '2024-12-12', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 19);
INSERT INTO `attendance_attendance` VALUES (785, '2024-12-12', NULL, '17:45:09.000000', 'early', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 20);
INSERT INTO `attendance_attendance` VALUES (786, '2024-12-12', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 21);
INSERT INTO `attendance_attendance` VALUES (787, '2024-12-12', '08:55:06.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 22);
INSERT INTO `attendance_attendance` VALUES (788, '2024-12-12', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 23);
INSERT INTO `attendance_attendance` VALUES (789, '2024-12-12', NULL, '17:45:03.000000', 'early', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 24);
INSERT INTO `attendance_attendance` VALUES (790, '2024-12-12', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 25);
INSERT INTO `attendance_attendance` VALUES (791, '2024-12-12', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 26);
INSERT INTO `attendance_attendance` VALUES (792, '2024-12-12', '08:55:10.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 27);
INSERT INTO `attendance_attendance` VALUES (793, '2024-12-12', '08:55:04.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 28);
INSERT INTO `attendance_attendance` VALUES (794, '2024-12-12', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 29);
INSERT INTO `attendance_attendance` VALUES (795, '2024-12-12', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 30);
INSERT INTO `attendance_attendance` VALUES (796, '2024-12-12', NULL, '17:45:03.000000', 'early', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 31);
INSERT INTO `attendance_attendance` VALUES (797, '2024-12-12', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 32);
INSERT INTO `attendance_attendance` VALUES (798, '2024-12-12', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 33);
INSERT INTO `attendance_attendance` VALUES (799, '2024-12-12', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 34);
INSERT INTO `attendance_attendance` VALUES (800, '2024-12-12', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 35);
INSERT INTO `attendance_attendance` VALUES (801, '2024-12-12', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 36);
INSERT INTO `attendance_attendance` VALUES (802, '2024-12-12', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 37);
INSERT INTO `attendance_attendance` VALUES (803, '2024-12-12', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 38);
INSERT INTO `attendance_attendance` VALUES (804, '2024-12-12', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 39);
INSERT INTO `attendance_attendance` VALUES (805, '2024-12-12', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 40);
INSERT INTO `attendance_attendance` VALUES (806, '2024-12-12', '08:55:10.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 41);
INSERT INTO `attendance_attendance` VALUES (807, '2024-12-12', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 42);
INSERT INTO `attendance_attendance` VALUES (808, '2024-12-12', '08:55:00.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 43);
INSERT INTO `attendance_attendance` VALUES (809, '2024-12-12', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 44);
INSERT INTO `attendance_attendance` VALUES (810, '2024-12-12', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 45);
INSERT INTO `attendance_attendance` VALUES (811, '2024-12-12', '09:05:23.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 46);
INSERT INTO `attendance_attendance` VALUES (812, '2024-12-12', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 47);
INSERT INTO `attendance_attendance` VALUES (813, '2024-12-12', '08:55:05.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 48);
INSERT INTO `attendance_attendance` VALUES (814, '2024-12-12', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 49);
INSERT INTO `attendance_attendance` VALUES (815, '2024-12-12', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 50);
INSERT INTO `attendance_attendance` VALUES (816, '2024-12-12', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 51);
INSERT INTO `attendance_attendance` VALUES (817, '2024-12-12', '08:55:03.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 52);
INSERT INTO `attendance_attendance` VALUES (818, '2024-12-12', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 53);
INSERT INTO `attendance_attendance` VALUES (819, '2024-12-12', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 54);
INSERT INTO `attendance_attendance` VALUES (820, '2024-12-12', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 55);
INSERT INTO `attendance_attendance` VALUES (821, '2024-12-12', '08:55:02.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 56);
INSERT INTO `attendance_attendance` VALUES (822, '2024-12-12', '09:05:04.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 57);
INSERT INTO `attendance_attendance` VALUES (823, '2024-12-12', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 58);
INSERT INTO `attendance_attendance` VALUES (824, '2024-12-12', NULL, NULL, 'absent', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 59);
INSERT INTO `attendance_attendance` VALUES (825, '2024-12-12', '09:05:09.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 60);
INSERT INTO `attendance_attendance` VALUES (826, '2024-12-12', '09:05:17.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 61);
INSERT INTO `attendance_attendance` VALUES (827, '2024-12-12', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 62);
INSERT INTO `attendance_attendance` VALUES (828, '2024-12-12', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 63);
INSERT INTO `attendance_attendance` VALUES (829, '2024-12-12', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 64);
INSERT INTO `attendance_attendance` VALUES (830, '2024-12-12', '09:05:21.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 65);
INSERT INTO `attendance_attendance` VALUES (831, '2024-12-12', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 66);
INSERT INTO `attendance_attendance` VALUES (832, '2024-12-12', '09:05:29.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 67);
INSERT INTO `attendance_attendance` VALUES (833, '2024-12-12', '08:55:02.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 68);
INSERT INTO `attendance_attendance` VALUES (834, '2024-12-12', '08:55:03.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 69);
INSERT INTO `attendance_attendance` VALUES (835, '2024-12-12', '08:55:10.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 70);
INSERT INTO `attendance_attendance` VALUES (836, '2024-12-12', '08:55:09.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 71);
INSERT INTO `attendance_attendance` VALUES (837, '2024-12-12', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 72);
INSERT INTO `attendance_attendance` VALUES (838, '2024-12-12', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 73);
INSERT INTO `attendance_attendance` VALUES (839, '2024-12-12', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 74);
INSERT INTO `attendance_attendance` VALUES (840, '2024-12-12', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 75);
INSERT INTO `attendance_attendance` VALUES (841, '2024-12-12', '08:55:08.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 76);
INSERT INTO `attendance_attendance` VALUES (842, '2024-12-12', '09:05:15.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 77);
INSERT INTO `attendance_attendance` VALUES (843, '2024-12-12', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 78);
INSERT INTO `attendance_attendance` VALUES (844, '2024-12-12', '08:55:02.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 79);
INSERT INTO `attendance_attendance` VALUES (845, '2024-12-12', '08:55:08.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 80);
INSERT INTO `attendance_attendance` VALUES (846, '2024-12-12', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 81);
INSERT INTO `attendance_attendance` VALUES (847, '2024-12-12', '08:55:01.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 82);
INSERT INTO `attendance_attendance` VALUES (848, '2024-12-12', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 83);
INSERT INTO `attendance_attendance` VALUES (849, '2024-12-12', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 84);
INSERT INTO `attendance_attendance` VALUES (850, '2024-12-12', '08:55:05.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 85);
INSERT INTO `attendance_attendance` VALUES (851, '2024-12-12', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 86);
INSERT INTO `attendance_attendance` VALUES (852, '2024-12-12', '08:55:07.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 87);
INSERT INTO `attendance_attendance` VALUES (853, '2024-12-12', '08:55:02.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 88);
INSERT INTO `attendance_attendance` VALUES (854, '2024-12-12', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 89);
INSERT INTO `attendance_attendance` VALUES (855, '2024-12-12', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 90);
INSERT INTO `attendance_attendance` VALUES (856, '2024-12-12', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 91);
INSERT INTO `attendance_attendance` VALUES (857, '2024-12-12', '08:55:01.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 92);
INSERT INTO `attendance_attendance` VALUES (858, '2024-12-12', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 93);
INSERT INTO `attendance_attendance` VALUES (859, '2024-12-12', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 94);
INSERT INTO `attendance_attendance` VALUES (860, '2024-12-12', '09:05:20.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 95);
INSERT INTO `attendance_attendance` VALUES (861, '2024-12-12', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 96);
INSERT INTO `attendance_attendance` VALUES (862, '2024-12-12', '08:55:05.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 97);
INSERT INTO `attendance_attendance` VALUES (863, '2024-12-12', '08:55:10.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 98);
INSERT INTO `attendance_attendance` VALUES (864, '2024-12-12', '09:05:11.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 99);
INSERT INTO `attendance_attendance` VALUES (865, '2024-12-12', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 100);
INSERT INTO `attendance_attendance` VALUES (866, '2024-12-13', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 5);
INSERT INTO `attendance_attendance` VALUES (867, '2024-12-13', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 6);
INSERT INTO `attendance_attendance` VALUES (868, '2024-12-13', NULL, '17:45:08.000000', 'early', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 7);
INSERT INTO `attendance_attendance` VALUES (869, '2024-12-13', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 8);
INSERT INTO `attendance_attendance` VALUES (870, '2024-12-13', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 9);
INSERT INTO `attendance_attendance` VALUES (871, '2024-12-13', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 10);
INSERT INTO `attendance_attendance` VALUES (872, '2024-12-13', NULL, NULL, 'absent', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 11);
INSERT INTO `attendance_attendance` VALUES (873, '2024-12-13', '08:55:10.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 12);
INSERT INTO `attendance_attendance` VALUES (874, '2024-12-13', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 13);
INSERT INTO `attendance_attendance` VALUES (875, '2024-12-13', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 14);
INSERT INTO `attendance_attendance` VALUES (876, '2024-12-13', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 15);
INSERT INTO `attendance_attendance` VALUES (877, '2024-12-13', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 16);
INSERT INTO `attendance_attendance` VALUES (878, '2024-12-13', '08:55:05.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 17);
INSERT INTO `attendance_attendance` VALUES (879, '2024-12-13', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 18);
INSERT INTO `attendance_attendance` VALUES (880, '2024-12-13', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 19);
INSERT INTO `attendance_attendance` VALUES (881, '2024-12-13', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 20);
INSERT INTO `attendance_attendance` VALUES (882, '2024-12-13', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 21);
INSERT INTO `attendance_attendance` VALUES (883, '2024-12-13', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 22);
INSERT INTO `attendance_attendance` VALUES (884, '2024-12-13', '08:55:07.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 23);
INSERT INTO `attendance_attendance` VALUES (885, '2024-12-13', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 24);
INSERT INTO `attendance_attendance` VALUES (886, '2024-12-13', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 25);
INSERT INTO `attendance_attendance` VALUES (887, '2024-12-13', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 26);
INSERT INTO `attendance_attendance` VALUES (888, '2024-12-13', '09:05:20.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 27);
INSERT INTO `attendance_attendance` VALUES (889, '2024-12-13', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 28);
INSERT INTO `attendance_attendance` VALUES (890, '2024-12-13', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 29);
INSERT INTO `attendance_attendance` VALUES (891, '2024-12-13', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 30);
INSERT INTO `attendance_attendance` VALUES (892, '2024-12-13', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 31);
INSERT INTO `attendance_attendance` VALUES (893, '2024-12-13', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 32);
INSERT INTO `attendance_attendance` VALUES (894, '2024-12-13', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 33);
INSERT INTO `attendance_attendance` VALUES (895, '2024-12-13', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 34);
INSERT INTO `attendance_attendance` VALUES (896, '2024-12-13', '08:55:02.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 35);
INSERT INTO `attendance_attendance` VALUES (897, '2024-12-13', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 36);
INSERT INTO `attendance_attendance` VALUES (898, '2024-12-13', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 37);
INSERT INTO `attendance_attendance` VALUES (899, '2024-12-13', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 38);
INSERT INTO `attendance_attendance` VALUES (900, '2024-12-13', NULL, '17:45:05.000000', 'early', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 39);
INSERT INTO `attendance_attendance` VALUES (901, '2024-12-13', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 40);
INSERT INTO `attendance_attendance` VALUES (902, '2024-12-13', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 41);
INSERT INTO `attendance_attendance` VALUES (903, '2024-12-13', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 42);
INSERT INTO `attendance_attendance` VALUES (904, '2024-12-13', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 43);
INSERT INTO `attendance_attendance` VALUES (905, '2024-12-13', '09:05:26.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 44);
INSERT INTO `attendance_attendance` VALUES (906, '2024-12-13', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 45);
INSERT INTO `attendance_attendance` VALUES (907, '2024-12-13', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 46);
INSERT INTO `attendance_attendance` VALUES (908, '2024-12-13', '08:55:01.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 47);
INSERT INTO `attendance_attendance` VALUES (909, '2024-12-13', '09:05:15.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 48);
INSERT INTO `attendance_attendance` VALUES (910, '2024-12-13', '09:05:26.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 49);
INSERT INTO `attendance_attendance` VALUES (911, '2024-12-13', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 50);
INSERT INTO `attendance_attendance` VALUES (912, '2024-12-13', '08:55:09.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 51);
INSERT INTO `attendance_attendance` VALUES (913, '2024-12-13', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 52);
INSERT INTO `attendance_attendance` VALUES (914, '2024-12-13', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 53);
INSERT INTO `attendance_attendance` VALUES (915, '2024-12-13', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 54);
INSERT INTO `attendance_attendance` VALUES (916, '2024-12-13', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 55);
INSERT INTO `attendance_attendance` VALUES (917, '2024-12-13', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 56);
INSERT INTO `attendance_attendance` VALUES (918, '2024-12-13', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 57);
INSERT INTO `attendance_attendance` VALUES (919, '2024-12-13', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 58);
INSERT INTO `attendance_attendance` VALUES (920, '2024-12-13', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 59);
INSERT INTO `attendance_attendance` VALUES (921, '2024-12-13', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 60);
INSERT INTO `attendance_attendance` VALUES (922, '2024-12-13', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 61);
INSERT INTO `attendance_attendance` VALUES (923, '2024-12-13', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 62);
INSERT INTO `attendance_attendance` VALUES (924, '2024-12-13', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 63);
INSERT INTO `attendance_attendance` VALUES (925, '2024-12-13', NULL, '17:45:10.000000', 'early', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 64);
INSERT INTO `attendance_attendance` VALUES (926, '2024-12-13', NULL, NULL, 'absent', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 65);
INSERT INTO `attendance_attendance` VALUES (927, '2024-12-13', NULL, '17:45:08.000000', 'early', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 66);
INSERT INTO `attendance_attendance` VALUES (928, '2024-12-13', '08:55:08.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 67);
INSERT INTO `attendance_attendance` VALUES (929, '2024-12-13', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 68);
INSERT INTO `attendance_attendance` VALUES (930, '2024-12-13', '09:05:04.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 69);
INSERT INTO `attendance_attendance` VALUES (931, '2024-12-13', '09:05:06.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 70);
INSERT INTO `attendance_attendance` VALUES (932, '2024-12-13', '08:55:05.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 71);
INSERT INTO `attendance_attendance` VALUES (933, '2024-12-13', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 72);
INSERT INTO `attendance_attendance` VALUES (934, '2024-12-13', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 73);
INSERT INTO `attendance_attendance` VALUES (935, '2024-12-13', '08:55:03.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 74);
INSERT INTO `attendance_attendance` VALUES (936, '2024-12-13', '08:55:03.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 75);
INSERT INTO `attendance_attendance` VALUES (937, '2024-12-13', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 76);
INSERT INTO `attendance_attendance` VALUES (938, '2024-12-13', '08:55:05.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 77);
INSERT INTO `attendance_attendance` VALUES (939, '2024-12-13', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 78);
INSERT INTO `attendance_attendance` VALUES (940, '2024-12-13', '08:55:10.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 79);
INSERT INTO `attendance_attendance` VALUES (941, '2024-12-13', '08:55:06.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 80);
INSERT INTO `attendance_attendance` VALUES (942, '2024-12-13', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 81);
INSERT INTO `attendance_attendance` VALUES (943, '2024-12-13', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 82);
INSERT INTO `attendance_attendance` VALUES (944, '2024-12-13', '08:55:02.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 83);
INSERT INTO `attendance_attendance` VALUES (945, '2024-12-13', '09:05:03.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 84);
INSERT INTO `attendance_attendance` VALUES (946, '2024-12-13', '08:55:01.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 85);
INSERT INTO `attendance_attendance` VALUES (947, '2024-12-13', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 86);
INSERT INTO `attendance_attendance` VALUES (948, '2024-12-13', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 87);
INSERT INTO `attendance_attendance` VALUES (949, '2024-12-13', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 88);
INSERT INTO `attendance_attendance` VALUES (950, '2024-12-13', '08:55:07.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 89);
INSERT INTO `attendance_attendance` VALUES (951, '2024-12-13', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 90);
INSERT INTO `attendance_attendance` VALUES (952, '2024-12-13', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 91);
INSERT INTO `attendance_attendance` VALUES (953, '2024-12-13', '08:55:06.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 92);
INSERT INTO `attendance_attendance` VALUES (954, '2024-12-13', '08:55:07.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 93);
INSERT INTO `attendance_attendance` VALUES (955, '2024-12-13', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 94);
INSERT INTO `attendance_attendance` VALUES (956, '2024-12-13', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 95);
INSERT INTO `attendance_attendance` VALUES (957, '2024-12-13', NULL, NULL, 'absent', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 96);
INSERT INTO `attendance_attendance` VALUES (958, '2024-12-13', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 97);
INSERT INTO `attendance_attendance` VALUES (959, '2024-12-13', NULL, '17:45:01.000000', 'early', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 98);
INSERT INTO `attendance_attendance` VALUES (960, '2024-12-13', '08:55:02.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 99);
INSERT INTO `attendance_attendance` VALUES (961, '2024-12-13', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 100);
INSERT INTO `attendance_attendance` VALUES (962, '2024-12-16', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 5);
INSERT INTO `attendance_attendance` VALUES (963, '2024-12-16', NULL, NULL, 'absent', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 6);
INSERT INTO `attendance_attendance` VALUES (964, '2024-12-16', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 7);
INSERT INTO `attendance_attendance` VALUES (965, '2024-12-16', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 8);
INSERT INTO `attendance_attendance` VALUES (966, '2024-12-16', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 9);
INSERT INTO `attendance_attendance` VALUES (967, '2024-12-16', '08:55:02.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 10);
INSERT INTO `attendance_attendance` VALUES (968, '2024-12-16', '08:55:01.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 11);
INSERT INTO `attendance_attendance` VALUES (969, '2024-12-16', '08:55:01.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 12);
INSERT INTO `attendance_attendance` VALUES (970, '2024-12-16', '08:55:06.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 13);
INSERT INTO `attendance_attendance` VALUES (971, '2024-12-16', '09:05:26.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 14);
INSERT INTO `attendance_attendance` VALUES (972, '2024-12-16', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 15);
INSERT INTO `attendance_attendance` VALUES (973, '2024-12-16', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 16);
INSERT INTO `attendance_attendance` VALUES (974, '2024-12-16', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 17);
INSERT INTO `attendance_attendance` VALUES (975, '2024-12-16', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 18);
INSERT INTO `attendance_attendance` VALUES (976, '2024-12-16', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 19);
INSERT INTO `attendance_attendance` VALUES (977, '2024-12-16', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 20);
INSERT INTO `attendance_attendance` VALUES (978, '2024-12-16', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 21);
INSERT INTO `attendance_attendance` VALUES (979, '2024-12-16', '08:55:10.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 22);
INSERT INTO `attendance_attendance` VALUES (980, '2024-12-16', NULL, '17:45:02.000000', 'early', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 23);
INSERT INTO `attendance_attendance` VALUES (981, '2024-12-16', '08:55:06.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 24);
INSERT INTO `attendance_attendance` VALUES (982, '2024-12-16', '08:55:01.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 25);
INSERT INTO `attendance_attendance` VALUES (983, '2024-12-16', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 26);
INSERT INTO `attendance_attendance` VALUES (984, '2024-12-16', '08:55:10.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 27);
INSERT INTO `attendance_attendance` VALUES (985, '2024-12-16', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 28);
INSERT INTO `attendance_attendance` VALUES (986, '2024-12-16', NULL, NULL, 'absent', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 29);
INSERT INTO `attendance_attendance` VALUES (987, '2024-12-16', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 30);
INSERT INTO `attendance_attendance` VALUES (988, '2024-12-16', '08:55:09.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 31);
INSERT INTO `attendance_attendance` VALUES (989, '2024-12-16', '09:05:26.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 32);
INSERT INTO `attendance_attendance` VALUES (990, '2024-12-16', '08:55:06.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 33);
INSERT INTO `attendance_attendance` VALUES (991, '2024-12-16', '08:55:05.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 34);
INSERT INTO `attendance_attendance` VALUES (992, '2024-12-16', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 35);
INSERT INTO `attendance_attendance` VALUES (993, '2024-12-16', '08:55:00.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 36);
INSERT INTO `attendance_attendance` VALUES (994, '2024-12-16', '08:55:00.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 37);
INSERT INTO `attendance_attendance` VALUES (995, '2024-12-16', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 38);
INSERT INTO `attendance_attendance` VALUES (996, '2024-12-16', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 39);
INSERT INTO `attendance_attendance` VALUES (997, '2024-12-16', '08:55:03.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 40);
INSERT INTO `attendance_attendance` VALUES (998, '2024-12-16', '08:55:07.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 41);
INSERT INTO `attendance_attendance` VALUES (999, '2024-12-16', NULL, NULL, 'absent', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 42);
INSERT INTO `attendance_attendance` VALUES (1000, '2024-12-16', '08:55:06.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 43);
INSERT INTO `attendance_attendance` VALUES (1001, '2024-12-16', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 44);
INSERT INTO `attendance_attendance` VALUES (1002, '2024-12-16', '08:55:02.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 45);
INSERT INTO `attendance_attendance` VALUES (1003, '2024-12-16', '09:05:05.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 46);
INSERT INTO `attendance_attendance` VALUES (1004, '2024-12-16', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 47);
INSERT INTO `attendance_attendance` VALUES (1005, '2024-12-16', '08:55:00.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 48);
INSERT INTO `attendance_attendance` VALUES (1006, '2024-12-16', '09:05:22.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 49);
INSERT INTO `attendance_attendance` VALUES (1007, '2024-12-16', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 50);
INSERT INTO `attendance_attendance` VALUES (1008, '2024-12-16', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 51);
INSERT INTO `attendance_attendance` VALUES (1009, '2024-12-16', '08:55:01.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 52);
INSERT INTO `attendance_attendance` VALUES (1010, '2024-12-16', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 53);
INSERT INTO `attendance_attendance` VALUES (1011, '2024-12-16', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 54);
INSERT INTO `attendance_attendance` VALUES (1012, '2024-12-16', NULL, '17:45:08.000000', 'early', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 55);
INSERT INTO `attendance_attendance` VALUES (1013, '2024-12-16', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 56);
INSERT INTO `attendance_attendance` VALUES (1014, '2024-12-16', '09:05:05.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 57);
INSERT INTO `attendance_attendance` VALUES (1015, '2024-12-16', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 58);
INSERT INTO `attendance_attendance` VALUES (1016, '2024-12-16', '09:05:15.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 59);
INSERT INTO `attendance_attendance` VALUES (1017, '2024-12-16', NULL, '17:45:03.000000', 'early', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 60);
INSERT INTO `attendance_attendance` VALUES (1018, '2024-12-16', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 61);
INSERT INTO `attendance_attendance` VALUES (1019, '2024-12-16', '08:55:01.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 62);
INSERT INTO `attendance_attendance` VALUES (1020, '2024-12-16', '08:55:00.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 63);
INSERT INTO `attendance_attendance` VALUES (1021, '2024-12-16', '08:55:00.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 64);
INSERT INTO `attendance_attendance` VALUES (1022, '2024-12-16', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 65);
INSERT INTO `attendance_attendance` VALUES (1023, '2024-12-16', '08:55:10.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 66);
INSERT INTO `attendance_attendance` VALUES (1024, '2024-12-16', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 67);
INSERT INTO `attendance_attendance` VALUES (1025, '2024-12-16', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 68);
INSERT INTO `attendance_attendance` VALUES (1026, '2024-12-16', '08:55:02.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 69);
INSERT INTO `attendance_attendance` VALUES (1027, '2024-12-16', '08:55:00.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 70);
INSERT INTO `attendance_attendance` VALUES (1028, '2024-12-16', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 71);
INSERT INTO `attendance_attendance` VALUES (1029, '2024-12-16', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 72);
INSERT INTO `attendance_attendance` VALUES (1030, '2024-12-16', '09:05:19.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 73);
INSERT INTO `attendance_attendance` VALUES (1031, '2024-12-16', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 74);
INSERT INTO `attendance_attendance` VALUES (1032, '2024-12-16', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 75);
INSERT INTO `attendance_attendance` VALUES (1033, '2024-12-16', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 76);
INSERT INTO `attendance_attendance` VALUES (1034, '2024-12-16', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 77);
INSERT INTO `attendance_attendance` VALUES (1035, '2024-12-16', '09:05:13.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 78);
INSERT INTO `attendance_attendance` VALUES (1036, '2024-12-16', '08:55:09.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 79);
INSERT INTO `attendance_attendance` VALUES (1037, '2024-12-16', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 80);
INSERT INTO `attendance_attendance` VALUES (1038, '2024-12-16', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 81);
INSERT INTO `attendance_attendance` VALUES (1039, '2024-12-16', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 82);
INSERT INTO `attendance_attendance` VALUES (1040, '2024-12-16', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 83);
INSERT INTO `attendance_attendance` VALUES (1041, '2024-12-16', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 84);
INSERT INTO `attendance_attendance` VALUES (1042, '2024-12-16', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 85);
INSERT INTO `attendance_attendance` VALUES (1043, '2024-12-16', NULL, '17:45:01.000000', 'early', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 86);
INSERT INTO `attendance_attendance` VALUES (1044, '2024-12-16', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 87);
INSERT INTO `attendance_attendance` VALUES (1045, '2024-12-16', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 88);
INSERT INTO `attendance_attendance` VALUES (1046, '2024-12-16', '08:55:01.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 89);
INSERT INTO `attendance_attendance` VALUES (1047, '2024-12-16', '08:55:03.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 90);
INSERT INTO `attendance_attendance` VALUES (1048, '2024-12-16', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 91);
INSERT INTO `attendance_attendance` VALUES (1049, '2024-12-16', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 92);
INSERT INTO `attendance_attendance` VALUES (1050, '2024-12-16', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 93);
INSERT INTO `attendance_attendance` VALUES (1051, '2024-12-16', '08:55:06.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 94);
INSERT INTO `attendance_attendance` VALUES (1052, '2024-12-16', NULL, '17:45:04.000000', 'early', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 95);
INSERT INTO `attendance_attendance` VALUES (1053, '2024-12-16', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 96);
INSERT INTO `attendance_attendance` VALUES (1054, '2024-12-16', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 97);
INSERT INTO `attendance_attendance` VALUES (1055, '2024-12-16', '09:05:14.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 98);
INSERT INTO `attendance_attendance` VALUES (1056, '2024-12-16', '08:55:04.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 99);
INSERT INTO `attendance_attendance` VALUES (1057, '2024-12-16', '09:05:26.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 100);
INSERT INTO `attendance_attendance` VALUES (1058, '2024-12-17', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 5);
INSERT INTO `attendance_attendance` VALUES (1059, '2024-12-17', NULL, '17:45:04.000000', 'early', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 6);
INSERT INTO `attendance_attendance` VALUES (1060, '2024-12-17', '08:55:10.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 7);
INSERT INTO `attendance_attendance` VALUES (1061, '2024-12-17', '09:05:03.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 8);
INSERT INTO `attendance_attendance` VALUES (1062, '2024-12-17', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 9);
INSERT INTO `attendance_attendance` VALUES (1063, '2024-12-17', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 10);
INSERT INTO `attendance_attendance` VALUES (1064, '2024-12-17', '08:55:07.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 11);
INSERT INTO `attendance_attendance` VALUES (1065, '2024-12-17', '08:55:02.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 12);
INSERT INTO `attendance_attendance` VALUES (1066, '2024-12-17', '08:55:08.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 13);
INSERT INTO `attendance_attendance` VALUES (1067, '2024-12-17', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 14);
INSERT INTO `attendance_attendance` VALUES (1068, '2024-12-17', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 15);
INSERT INTO `attendance_attendance` VALUES (1069, '2024-12-17', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 16);
INSERT INTO `attendance_attendance` VALUES (1070, '2024-12-17', '08:55:00.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 17);
INSERT INTO `attendance_attendance` VALUES (1071, '2024-12-17', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 18);
INSERT INTO `attendance_attendance` VALUES (1072, '2024-12-17', '08:55:02.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 19);
INSERT INTO `attendance_attendance` VALUES (1073, '2024-12-17', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 20);
INSERT INTO `attendance_attendance` VALUES (1074, '2024-12-17', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 21);
INSERT INTO `attendance_attendance` VALUES (1075, '2024-12-17', '08:55:08.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 22);
INSERT INTO `attendance_attendance` VALUES (1076, '2024-12-17', '08:55:00.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 23);
INSERT INTO `attendance_attendance` VALUES (1077, '2024-12-17', '08:55:04.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 24);
INSERT INTO `attendance_attendance` VALUES (1078, '2024-12-17', '09:05:24.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 25);
INSERT INTO `attendance_attendance` VALUES (1079, '2024-12-17', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 26);
INSERT INTO `attendance_attendance` VALUES (1080, '2024-12-17', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 27);
INSERT INTO `attendance_attendance` VALUES (1081, '2024-12-17', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 28);
INSERT INTO `attendance_attendance` VALUES (1082, '2024-12-17', '08:55:02.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 29);
INSERT INTO `attendance_attendance` VALUES (1083, '2024-12-17', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 30);
INSERT INTO `attendance_attendance` VALUES (1084, '2024-12-17', '09:05:17.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 31);
INSERT INTO `attendance_attendance` VALUES (1085, '2024-12-17', '08:55:00.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 32);
INSERT INTO `attendance_attendance` VALUES (1086, '2024-12-17', '08:55:00.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 33);
INSERT INTO `attendance_attendance` VALUES (1087, '2024-12-17', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 34);
INSERT INTO `attendance_attendance` VALUES (1088, '2024-12-17', '08:55:03.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 35);
INSERT INTO `attendance_attendance` VALUES (1089, '2024-12-17', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 36);
INSERT INTO `attendance_attendance` VALUES (1090, '2024-12-17', '09:05:21.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 37);
INSERT INTO `attendance_attendance` VALUES (1091, '2024-12-17', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 38);
INSERT INTO `attendance_attendance` VALUES (1092, '2024-12-17', '08:55:05.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 39);
INSERT INTO `attendance_attendance` VALUES (1093, '2024-12-17', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 40);
INSERT INTO `attendance_attendance` VALUES (1094, '2024-12-17', '08:55:06.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 41);
INSERT INTO `attendance_attendance` VALUES (1095, '2024-12-17', '09:05:04.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 42);
INSERT INTO `attendance_attendance` VALUES (1096, '2024-12-17', '09:05:26.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 43);
INSERT INTO `attendance_attendance` VALUES (1097, '2024-12-17', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 44);
INSERT INTO `attendance_attendance` VALUES (1098, '2024-12-17', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 45);
INSERT INTO `attendance_attendance` VALUES (1099, '2024-12-17', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 46);
INSERT INTO `attendance_attendance` VALUES (1100, '2024-12-17', '08:55:07.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 47);
INSERT INTO `attendance_attendance` VALUES (1101, '2024-12-17', '08:55:09.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 48);
INSERT INTO `attendance_attendance` VALUES (1102, '2024-12-17', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 49);
INSERT INTO `attendance_attendance` VALUES (1103, '2024-12-17', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 50);
INSERT INTO `attendance_attendance` VALUES (1104, '2024-12-17', '08:55:09.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 51);
INSERT INTO `attendance_attendance` VALUES (1105, '2024-12-17', NULL, '17:45:02.000000', 'early', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 52);
INSERT INTO `attendance_attendance` VALUES (1106, '2024-12-17', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 53);
INSERT INTO `attendance_attendance` VALUES (1107, '2024-12-17', '09:05:19.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 54);
INSERT INTO `attendance_attendance` VALUES (1108, '2024-12-17', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 55);
INSERT INTO `attendance_attendance` VALUES (1109, '2024-12-17', '08:55:01.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 56);
INSERT INTO `attendance_attendance` VALUES (1110, '2024-12-17', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 57);
INSERT INTO `attendance_attendance` VALUES (1111, '2024-12-17', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 58);
INSERT INTO `attendance_attendance` VALUES (1112, '2024-12-17', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 59);
INSERT INTO `attendance_attendance` VALUES (1113, '2024-12-17', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 60);
INSERT INTO `attendance_attendance` VALUES (1114, '2024-12-17', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 61);
INSERT INTO `attendance_attendance` VALUES (1115, '2024-12-17', '08:55:00.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 62);
INSERT INTO `attendance_attendance` VALUES (1116, '2024-12-17', '08:55:01.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 63);
INSERT INTO `attendance_attendance` VALUES (1117, '2024-12-17', '09:05:03.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 64);
INSERT INTO `attendance_attendance` VALUES (1118, '2024-12-17', '08:55:05.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 65);
INSERT INTO `attendance_attendance` VALUES (1119, '2024-12-17', '08:55:07.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 66);
INSERT INTO `attendance_attendance` VALUES (1120, '2024-12-17', '08:55:01.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 67);
INSERT INTO `attendance_attendance` VALUES (1121, '2024-12-17', '08:55:07.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 68);
INSERT INTO `attendance_attendance` VALUES (1122, '2024-12-17', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 69);
INSERT INTO `attendance_attendance` VALUES (1123, '2024-12-17', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 70);
INSERT INTO `attendance_attendance` VALUES (1124, '2024-12-17', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 71);
INSERT INTO `attendance_attendance` VALUES (1125, '2024-12-17', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 72);
INSERT INTO `attendance_attendance` VALUES (1126, '2024-12-17', '08:55:06.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 73);
INSERT INTO `attendance_attendance` VALUES (1127, '2024-12-17', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 74);
INSERT INTO `attendance_attendance` VALUES (1128, '2024-12-17', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 75);
INSERT INTO `attendance_attendance` VALUES (1129, '2024-12-17', '08:55:01.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 76);
INSERT INTO `attendance_attendance` VALUES (1130, '2024-12-17', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 77);
INSERT INTO `attendance_attendance` VALUES (1131, '2024-12-17', '08:55:02.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 78);
INSERT INTO `attendance_attendance` VALUES (1132, '2024-12-17', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 79);
INSERT INTO `attendance_attendance` VALUES (1133, '2024-12-17', '08:55:08.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 80);
INSERT INTO `attendance_attendance` VALUES (1134, '2024-12-17', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 81);
INSERT INTO `attendance_attendance` VALUES (1135, '2024-12-17', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 82);
INSERT INTO `attendance_attendance` VALUES (1136, '2024-12-17', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 83);
INSERT INTO `attendance_attendance` VALUES (1137, '2024-12-17', '09:05:17.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 84);
INSERT INTO `attendance_attendance` VALUES (1138, '2024-12-17', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 85);
INSERT INTO `attendance_attendance` VALUES (1139, '2024-12-17', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 86);
INSERT INTO `attendance_attendance` VALUES (1140, '2024-12-17', '09:05:29.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 87);
INSERT INTO `attendance_attendance` VALUES (1141, '2024-12-17', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 88);
INSERT INTO `attendance_attendance` VALUES (1142, '2024-12-17', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 89);
INSERT INTO `attendance_attendance` VALUES (1143, '2024-12-17', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 90);
INSERT INTO `attendance_attendance` VALUES (1144, '2024-12-17', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 91);
INSERT INTO `attendance_attendance` VALUES (1145, '2024-12-17', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 92);
INSERT INTO `attendance_attendance` VALUES (1146, '2024-12-17', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 93);
INSERT INTO `attendance_attendance` VALUES (1147, '2024-12-17', '09:05:07.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 94);
INSERT INTO `attendance_attendance` VALUES (1148, '2024-12-17', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 95);
INSERT INTO `attendance_attendance` VALUES (1149, '2024-12-17', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 96);
INSERT INTO `attendance_attendance` VALUES (1150, '2024-12-17', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 97);
INSERT INTO `attendance_attendance` VALUES (1151, '2024-12-17', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 98);
INSERT INTO `attendance_attendance` VALUES (1152, '2024-12-17', '08:55:06.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 99);
INSERT INTO `attendance_attendance` VALUES (1153, '2024-12-17', NULL, NULL, 'absent', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 100);
INSERT INTO `attendance_attendance` VALUES (1154, '2024-12-18', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 5);
INSERT INTO `attendance_attendance` VALUES (1155, '2024-12-18', '08:55:04.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 6);
INSERT INTO `attendance_attendance` VALUES (1156, '2024-12-18', '08:55:00.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 7);
INSERT INTO `attendance_attendance` VALUES (1157, '2024-12-18', '08:55:09.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 8);
INSERT INTO `attendance_attendance` VALUES (1158, '2024-12-18', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 9);
INSERT INTO `attendance_attendance` VALUES (1159, '2024-12-18', '08:55:02.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 10);
INSERT INTO `attendance_attendance` VALUES (1160, '2024-12-18', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 11);
INSERT INTO `attendance_attendance` VALUES (1161, '2024-12-18', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 12);
INSERT INTO `attendance_attendance` VALUES (1162, '2024-12-18', '08:55:09.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 13);
INSERT INTO `attendance_attendance` VALUES (1163, '2024-12-18', '08:55:09.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 14);
INSERT INTO `attendance_attendance` VALUES (1164, '2024-12-18', '08:55:06.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 15);
INSERT INTO `attendance_attendance` VALUES (1165, '2024-12-18', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 16);
INSERT INTO `attendance_attendance` VALUES (1166, '2024-12-18', '08:55:10.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 17);
INSERT INTO `attendance_attendance` VALUES (1167, '2024-12-18', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 18);
INSERT INTO `attendance_attendance` VALUES (1168, '2024-12-18', '08:55:07.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 19);
INSERT INTO `attendance_attendance` VALUES (1169, '2024-12-18', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 20);
INSERT INTO `attendance_attendance` VALUES (1170, '2024-12-18', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 21);
INSERT INTO `attendance_attendance` VALUES (1171, '2024-12-18', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 22);
INSERT INTO `attendance_attendance` VALUES (1172, '2024-12-18', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 23);
INSERT INTO `attendance_attendance` VALUES (1173, '2024-12-18', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 24);
INSERT INTO `attendance_attendance` VALUES (1174, '2024-12-18', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 25);
INSERT INTO `attendance_attendance` VALUES (1175, '2024-12-18', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 26);
INSERT INTO `attendance_attendance` VALUES (1176, '2024-12-18', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 27);
INSERT INTO `attendance_attendance` VALUES (1177, '2024-12-18', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 28);
INSERT INTO `attendance_attendance` VALUES (1178, '2024-12-18', '08:55:09.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 29);
INSERT INTO `attendance_attendance` VALUES (1179, '2024-12-18', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 30);
INSERT INTO `attendance_attendance` VALUES (1180, '2024-12-18', '08:55:10.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 31);
INSERT INTO `attendance_attendance` VALUES (1181, '2024-12-18', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 32);
INSERT INTO `attendance_attendance` VALUES (1182, '2024-12-18', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 33);
INSERT INTO `attendance_attendance` VALUES (1183, '2024-12-18', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 34);
INSERT INTO `attendance_attendance` VALUES (1184, '2024-12-18', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 35);
INSERT INTO `attendance_attendance` VALUES (1185, '2024-12-18', '08:55:10.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 36);
INSERT INTO `attendance_attendance` VALUES (1186, '2024-12-18', '08:55:08.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 37);
INSERT INTO `attendance_attendance` VALUES (1187, '2024-12-18', '08:55:02.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 38);
INSERT INTO `attendance_attendance` VALUES (1188, '2024-12-18', '08:55:05.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 39);
INSERT INTO `attendance_attendance` VALUES (1189, '2024-12-18', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 40);
INSERT INTO `attendance_attendance` VALUES (1190, '2024-12-18', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 41);
INSERT INTO `attendance_attendance` VALUES (1191, '2024-12-18', '08:55:10.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 42);
INSERT INTO `attendance_attendance` VALUES (1192, '2024-12-18', '09:05:19.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 43);
INSERT INTO `attendance_attendance` VALUES (1193, '2024-12-18', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 44);
INSERT INTO `attendance_attendance` VALUES (1194, '2024-12-18', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 45);
INSERT INTO `attendance_attendance` VALUES (1195, '2024-12-18', '08:55:04.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 46);
INSERT INTO `attendance_attendance` VALUES (1196, '2024-12-18', '08:55:00.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 47);
INSERT INTO `attendance_attendance` VALUES (1197, '2024-12-18', '08:55:01.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 48);
INSERT INTO `attendance_attendance` VALUES (1198, '2024-12-18', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 49);
INSERT INTO `attendance_attendance` VALUES (1199, '2024-12-18', '08:55:02.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 50);
INSERT INTO `attendance_attendance` VALUES (1200, '2024-12-18', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 51);
INSERT INTO `attendance_attendance` VALUES (1201, '2024-12-18', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 52);
INSERT INTO `attendance_attendance` VALUES (1202, '2024-12-18', '09:05:18.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 53);
INSERT INTO `attendance_attendance` VALUES (1203, '2024-12-18', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 54);
INSERT INTO `attendance_attendance` VALUES (1204, '2024-12-18', '08:55:00.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 55);
INSERT INTO `attendance_attendance` VALUES (1205, '2024-12-18', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 56);
INSERT INTO `attendance_attendance` VALUES (1206, '2024-12-18', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 57);
INSERT INTO `attendance_attendance` VALUES (1207, '2024-12-18', '08:55:10.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 58);
INSERT INTO `attendance_attendance` VALUES (1208, '2024-12-18', '08:55:00.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 59);
INSERT INTO `attendance_attendance` VALUES (1209, '2024-12-18', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 60);
INSERT INTO `attendance_attendance` VALUES (1210, '2024-12-18', NULL, '17:45:09.000000', 'early', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 61);
INSERT INTO `attendance_attendance` VALUES (1211, '2024-12-18', '09:05:14.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 62);
INSERT INTO `attendance_attendance` VALUES (1212, '2024-12-18', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 63);
INSERT INTO `attendance_attendance` VALUES (1213, '2024-12-18', '08:55:07.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 64);
INSERT INTO `attendance_attendance` VALUES (1214, '2024-12-18', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 65);
INSERT INTO `attendance_attendance` VALUES (1215, '2024-12-18', '08:55:02.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 66);
INSERT INTO `attendance_attendance` VALUES (1216, '2024-12-18', NULL, '17:45:03.000000', 'early', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 67);
INSERT INTO `attendance_attendance` VALUES (1217, '2024-12-18', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 68);
INSERT INTO `attendance_attendance` VALUES (1218, '2024-12-18', '08:55:08.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 69);
INSERT INTO `attendance_attendance` VALUES (1219, '2024-12-18', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 70);
INSERT INTO `attendance_attendance` VALUES (1220, '2024-12-18', NULL, '17:45:09.000000', 'early', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 71);
INSERT INTO `attendance_attendance` VALUES (1221, '2024-12-18', '09:05:17.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 72);
INSERT INTO `attendance_attendance` VALUES (1222, '2024-12-18', '08:55:02.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 73);
INSERT INTO `attendance_attendance` VALUES (1223, '2024-12-18', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 74);
INSERT INTO `attendance_attendance` VALUES (1224, '2024-12-18', '08:55:09.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 75);
INSERT INTO `attendance_attendance` VALUES (1225, '2024-12-18', '09:05:05.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 76);
INSERT INTO `attendance_attendance` VALUES (1226, '2024-12-18', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 77);
INSERT INTO `attendance_attendance` VALUES (1227, '2024-12-18', '08:55:04.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 78);
INSERT INTO `attendance_attendance` VALUES (1228, '2024-12-18', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 79);
INSERT INTO `attendance_attendance` VALUES (1229, '2024-12-18', '08:55:06.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 80);
INSERT INTO `attendance_attendance` VALUES (1230, '2024-12-18', '08:55:01.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 81);
INSERT INTO `attendance_attendance` VALUES (1231, '2024-12-18', '08:55:08.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 82);
INSERT INTO `attendance_attendance` VALUES (1232, '2024-12-18', '08:55:06.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 83);
INSERT INTO `attendance_attendance` VALUES (1233, '2024-12-18', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 84);
INSERT INTO `attendance_attendance` VALUES (1234, '2024-12-18', '08:55:09.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 85);
INSERT INTO `attendance_attendance` VALUES (1235, '2024-12-18', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 86);
INSERT INTO `attendance_attendance` VALUES (1236, '2024-12-18', '08:55:01.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 87);
INSERT INTO `attendance_attendance` VALUES (1237, '2024-12-18', NULL, '17:45:01.000000', 'early', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 88);
INSERT INTO `attendance_attendance` VALUES (1238, '2024-12-18', '08:55:10.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 89);
INSERT INTO `attendance_attendance` VALUES (1239, '2024-12-18', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 90);
INSERT INTO `attendance_attendance` VALUES (1240, '2024-12-18', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 91);
INSERT INTO `attendance_attendance` VALUES (1241, '2024-12-18', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 92);
INSERT INTO `attendance_attendance` VALUES (1242, '2024-12-18', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 93);
INSERT INTO `attendance_attendance` VALUES (1243, '2024-12-18', '09:05:19.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 94);
INSERT INTO `attendance_attendance` VALUES (1244, '2024-12-18', '08:55:10.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 95);
INSERT INTO `attendance_attendance` VALUES (1245, '2024-12-18', '08:55:00.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 96);
INSERT INTO `attendance_attendance` VALUES (1246, '2024-12-18', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 97);
INSERT INTO `attendance_attendance` VALUES (1247, '2024-12-18', '08:55:02.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 98);
INSERT INTO `attendance_attendance` VALUES (1248, '2024-12-18', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 99);
INSERT INTO `attendance_attendance` VALUES (1249, '2024-12-18', '09:05:14.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 100);
INSERT INTO `attendance_attendance` VALUES (1250, '2024-12-19', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 5);
INSERT INTO `attendance_attendance` VALUES (1251, '2024-12-19', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 6);
INSERT INTO `attendance_attendance` VALUES (1252, '2024-12-19', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 7);
INSERT INTO `attendance_attendance` VALUES (1253, '2024-12-19', '08:55:07.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 8);
INSERT INTO `attendance_attendance` VALUES (1254, '2024-12-19', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 9);
INSERT INTO `attendance_attendance` VALUES (1255, '2024-12-19', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 10);
INSERT INTO `attendance_attendance` VALUES (1256, '2024-12-19', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 11);
INSERT INTO `attendance_attendance` VALUES (1257, '2024-12-19', '09:05:05.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 12);
INSERT INTO `attendance_attendance` VALUES (1258, '2024-12-19', '08:55:00.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 13);
INSERT INTO `attendance_attendance` VALUES (1259, '2024-12-19', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 14);
INSERT INTO `attendance_attendance` VALUES (1260, '2024-12-19', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 15);
INSERT INTO `attendance_attendance` VALUES (1261, '2024-12-19', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 16);
INSERT INTO `attendance_attendance` VALUES (1262, '2024-12-19', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 17);
INSERT INTO `attendance_attendance` VALUES (1263, '2024-12-19', '09:05:09.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 18);
INSERT INTO `attendance_attendance` VALUES (1264, '2024-12-19', '08:55:10.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 19);
INSERT INTO `attendance_attendance` VALUES (1265, '2024-12-19', '08:55:10.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 20);
INSERT INTO `attendance_attendance` VALUES (1266, '2024-12-19', '09:05:05.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 21);
INSERT INTO `attendance_attendance` VALUES (1267, '2024-12-19', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 22);
INSERT INTO `attendance_attendance` VALUES (1268, '2024-12-19', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 23);
INSERT INTO `attendance_attendance` VALUES (1269, '2024-12-19', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 24);
INSERT INTO `attendance_attendance` VALUES (1270, '2024-12-19', '08:55:08.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 25);
INSERT INTO `attendance_attendance` VALUES (1271, '2024-12-19', '08:55:06.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 26);
INSERT INTO `attendance_attendance` VALUES (1272, '2024-12-19', '09:05:10.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 27);
INSERT INTO `attendance_attendance` VALUES (1273, '2024-12-19', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 28);
INSERT INTO `attendance_attendance` VALUES (1274, '2024-12-19', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 29);
INSERT INTO `attendance_attendance` VALUES (1275, '2024-12-19', NULL, '17:45:01.000000', 'early', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 30);
INSERT INTO `attendance_attendance` VALUES (1276, '2024-12-19', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 31);
INSERT INTO `attendance_attendance` VALUES (1277, '2024-12-19', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 32);
INSERT INTO `attendance_attendance` VALUES (1278, '2024-12-19', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 33);
INSERT INTO `attendance_attendance` VALUES (1279, '2024-12-19', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 34);
INSERT INTO `attendance_attendance` VALUES (1280, '2024-12-19', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 35);
INSERT INTO `attendance_attendance` VALUES (1281, '2024-12-19', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 36);
INSERT INTO `attendance_attendance` VALUES (1282, '2024-12-19', '08:55:02.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 37);
INSERT INTO `attendance_attendance` VALUES (1283, '2024-12-19', '09:05:29.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 38);
INSERT INTO `attendance_attendance` VALUES (1284, '2024-12-19', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 39);
INSERT INTO `attendance_attendance` VALUES (1285, '2024-12-19', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 40);
INSERT INTO `attendance_attendance` VALUES (1286, '2024-12-19', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 41);
INSERT INTO `attendance_attendance` VALUES (1287, '2024-12-19', '08:55:03.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 42);
INSERT INTO `attendance_attendance` VALUES (1288, '2024-12-19', NULL, NULL, 'absent', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 43);
INSERT INTO `attendance_attendance` VALUES (1289, '2024-12-19', '09:05:14.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 44);
INSERT INTO `attendance_attendance` VALUES (1290, '2024-12-19', '08:55:00.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 45);
INSERT INTO `attendance_attendance` VALUES (1291, '2024-12-19', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 46);
INSERT INTO `attendance_attendance` VALUES (1292, '2024-12-19', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 47);
INSERT INTO `attendance_attendance` VALUES (1293, '2024-12-19', '08:55:04.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 48);
INSERT INTO `attendance_attendance` VALUES (1294, '2024-12-19', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 49);
INSERT INTO `attendance_attendance` VALUES (1295, '2024-12-19', '08:55:04.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 50);
INSERT INTO `attendance_attendance` VALUES (1296, '2024-12-19', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 51);
INSERT INTO `attendance_attendance` VALUES (1297, '2024-12-19', '08:55:08.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 52);
INSERT INTO `attendance_attendance` VALUES (1298, '2024-12-19', '08:55:07.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 53);
INSERT INTO `attendance_attendance` VALUES (1299, '2024-12-19', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 54);
INSERT INTO `attendance_attendance` VALUES (1300, '2024-12-19', '08:55:01.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 55);
INSERT INTO `attendance_attendance` VALUES (1301, '2024-12-19', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 56);
INSERT INTO `attendance_attendance` VALUES (1302, '2024-12-19', '08:55:07.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 57);
INSERT INTO `attendance_attendance` VALUES (1303, '2024-12-19', '08:55:03.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 58);
INSERT INTO `attendance_attendance` VALUES (1304, '2024-12-19', '08:55:08.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 59);
INSERT INTO `attendance_attendance` VALUES (1305, '2024-12-19', '08:55:06.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 60);
INSERT INTO `attendance_attendance` VALUES (1306, '2024-12-19', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 61);
INSERT INTO `attendance_attendance` VALUES (1307, '2024-12-19', '08:55:01.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 62);
INSERT INTO `attendance_attendance` VALUES (1308, '2024-12-19', '08:55:06.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 63);
INSERT INTO `attendance_attendance` VALUES (1309, '2024-12-19', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 64);
INSERT INTO `attendance_attendance` VALUES (1310, '2024-12-19', '08:55:03.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 65);
INSERT INTO `attendance_attendance` VALUES (1311, '2024-12-19', '08:55:00.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 66);
INSERT INTO `attendance_attendance` VALUES (1312, '2024-12-19', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 67);
INSERT INTO `attendance_attendance` VALUES (1313, '2024-12-19', '08:55:02.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 68);
INSERT INTO `attendance_attendance` VALUES (1314, '2024-12-19', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 69);
INSERT INTO `attendance_attendance` VALUES (1315, '2024-12-19', '09:05:16.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 70);
INSERT INTO `attendance_attendance` VALUES (1316, '2024-12-19', NULL, NULL, 'absent', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 71);
INSERT INTO `attendance_attendance` VALUES (1317, '2024-12-19', '08:55:08.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 72);
INSERT INTO `attendance_attendance` VALUES (1318, '2024-12-19', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 73);
INSERT INTO `attendance_attendance` VALUES (1319, '2024-12-19', '08:55:03.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 74);
INSERT INTO `attendance_attendance` VALUES (1320, '2024-12-19', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 75);
INSERT INTO `attendance_attendance` VALUES (1321, '2024-12-19', '08:55:10.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 76);
INSERT INTO `attendance_attendance` VALUES (1322, '2024-12-19', '08:55:02.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 77);
INSERT INTO `attendance_attendance` VALUES (1323, '2024-12-19', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 78);
INSERT INTO `attendance_attendance` VALUES (1324, '2024-12-19', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 79);
INSERT INTO `attendance_attendance` VALUES (1325, '2024-12-19', '08:55:02.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 80);
INSERT INTO `attendance_attendance` VALUES (1326, '2024-12-19', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 81);
INSERT INTO `attendance_attendance` VALUES (1327, '2024-12-19', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 82);
INSERT INTO `attendance_attendance` VALUES (1328, '2024-12-19', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 83);
INSERT INTO `attendance_attendance` VALUES (1329, '2024-12-19', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 84);
INSERT INTO `attendance_attendance` VALUES (1330, '2024-12-19', '08:55:07.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 85);
INSERT INTO `attendance_attendance` VALUES (1331, '2024-12-19', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 86);
INSERT INTO `attendance_attendance` VALUES (1332, '2024-12-19', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 87);
INSERT INTO `attendance_attendance` VALUES (1333, '2024-12-19', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 88);
INSERT INTO `attendance_attendance` VALUES (1334, '2024-12-19', '09:05:18.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 89);
INSERT INTO `attendance_attendance` VALUES (1335, '2024-12-19', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 90);
INSERT INTO `attendance_attendance` VALUES (1336, '2024-12-19', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 91);
INSERT INTO `attendance_attendance` VALUES (1337, '2024-12-19', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 92);
INSERT INTO `attendance_attendance` VALUES (1338, '2024-12-19', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 93);
INSERT INTO `attendance_attendance` VALUES (1339, '2024-12-19', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 94);
INSERT INTO `attendance_attendance` VALUES (1340, '2024-12-19', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 95);
INSERT INTO `attendance_attendance` VALUES (1341, '2024-12-19', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 96);
INSERT INTO `attendance_attendance` VALUES (1342, '2024-12-19', '09:05:29.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 97);
INSERT INTO `attendance_attendance` VALUES (1343, '2024-12-19', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 98);
INSERT INTO `attendance_attendance` VALUES (1344, '2024-12-19', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 99);
INSERT INTO `attendance_attendance` VALUES (1345, '2024-12-19', '09:05:28.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 100);
INSERT INTO `attendance_attendance` VALUES (1346, '2024-12-20', '09:05:22.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 5);
INSERT INTO `attendance_attendance` VALUES (1347, '2024-12-20', '09:05:05.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 6);
INSERT INTO `attendance_attendance` VALUES (1348, '2024-12-20', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 7);
INSERT INTO `attendance_attendance` VALUES (1349, '2024-12-20', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 8);
INSERT INTO `attendance_attendance` VALUES (1350, '2024-12-20', '09:05:11.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 9);
INSERT INTO `attendance_attendance` VALUES (1351, '2024-12-20', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 10);
INSERT INTO `attendance_attendance` VALUES (1352, '2024-12-20', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 11);
INSERT INTO `attendance_attendance` VALUES (1353, '2024-12-20', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 12);
INSERT INTO `attendance_attendance` VALUES (1354, '2024-12-20', '08:55:06.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 13);
INSERT INTO `attendance_attendance` VALUES (1355, '2024-12-20', '09:05:13.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 14);
INSERT INTO `attendance_attendance` VALUES (1356, '2024-12-20', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 15);
INSERT INTO `attendance_attendance` VALUES (1357, '2024-12-20', '08:55:00.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 16);
INSERT INTO `attendance_attendance` VALUES (1358, '2024-12-20', NULL, '17:45:04.000000', 'early', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 17);
INSERT INTO `attendance_attendance` VALUES (1359, '2024-12-20', '08:55:10.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 18);
INSERT INTO `attendance_attendance` VALUES (1360, '2024-12-20', '08:55:01.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 19);
INSERT INTO `attendance_attendance` VALUES (1361, '2024-12-20', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 20);
INSERT INTO `attendance_attendance` VALUES (1362, '2024-12-20', '08:55:10.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 21);
INSERT INTO `attendance_attendance` VALUES (1363, '2024-12-20', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 22);
INSERT INTO `attendance_attendance` VALUES (1364, '2024-12-20', '08:55:00.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 23);
INSERT INTO `attendance_attendance` VALUES (1365, '2024-12-20', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 24);
INSERT INTO `attendance_attendance` VALUES (1366, '2024-12-20', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 25);
INSERT INTO `attendance_attendance` VALUES (1367, '2024-12-20', '08:55:00.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 26);
INSERT INTO `attendance_attendance` VALUES (1368, '2024-12-20', '08:55:09.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 27);
INSERT INTO `attendance_attendance` VALUES (1369, '2024-12-20', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 28);
INSERT INTO `attendance_attendance` VALUES (1370, '2024-12-20', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 29);
INSERT INTO `attendance_attendance` VALUES (1371, '2024-12-20', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 30);
INSERT INTO `attendance_attendance` VALUES (1372, '2024-12-20', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 31);
INSERT INTO `attendance_attendance` VALUES (1373, '2024-12-20', '08:55:05.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 32);
INSERT INTO `attendance_attendance` VALUES (1374, '2024-12-20', '08:55:07.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 33);
INSERT INTO `attendance_attendance` VALUES (1375, '2024-12-20', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 34);
INSERT INTO `attendance_attendance` VALUES (1376, '2024-12-20', NULL, '17:45:01.000000', 'early', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 35);
INSERT INTO `attendance_attendance` VALUES (1377, '2024-12-20', '08:55:00.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 36);
INSERT INTO `attendance_attendance` VALUES (1378, '2024-12-20', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 37);
INSERT INTO `attendance_attendance` VALUES (1379, '2024-12-20', '08:55:01.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 38);
INSERT INTO `attendance_attendance` VALUES (1380, '2024-12-20', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 39);
INSERT INTO `attendance_attendance` VALUES (1381, '2024-12-20', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 40);
INSERT INTO `attendance_attendance` VALUES (1382, '2024-12-20', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 41);
INSERT INTO `attendance_attendance` VALUES (1383, '2024-12-20', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 42);
INSERT INTO `attendance_attendance` VALUES (1384, '2024-12-20', '08:55:10.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 43);
INSERT INTO `attendance_attendance` VALUES (1385, '2024-12-20', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 44);
INSERT INTO `attendance_attendance` VALUES (1386, '2024-12-20', '08:55:03.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 45);
INSERT INTO `attendance_attendance` VALUES (1387, '2024-12-20', '09:05:25.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 46);
INSERT INTO `attendance_attendance` VALUES (1388, '2024-12-20', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 47);
INSERT INTO `attendance_attendance` VALUES (1389, '2024-12-20', '08:55:10.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 48);
INSERT INTO `attendance_attendance` VALUES (1390, '2024-12-20', '09:05:22.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 49);
INSERT INTO `attendance_attendance` VALUES (1391, '2024-12-20', NULL, '17:45:06.000000', 'early', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 50);
INSERT INTO `attendance_attendance` VALUES (1392, '2024-12-20', '08:55:06.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 51);
INSERT INTO `attendance_attendance` VALUES (1393, '2024-12-20', '08:55:05.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 52);
INSERT INTO `attendance_attendance` VALUES (1394, '2024-12-20', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 53);
INSERT INTO `attendance_attendance` VALUES (1395, '2024-12-20', NULL, '17:45:05.000000', 'early', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 54);
INSERT INTO `attendance_attendance` VALUES (1396, '2024-12-20', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 55);
INSERT INTO `attendance_attendance` VALUES (1397, '2024-12-20', '08:55:10.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 56);
INSERT INTO `attendance_attendance` VALUES (1398, '2024-12-20', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 57);
INSERT INTO `attendance_attendance` VALUES (1399, '2024-12-20', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 58);
INSERT INTO `attendance_attendance` VALUES (1400, '2024-12-20', NULL, '17:45:05.000000', 'early', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 59);
INSERT INTO `attendance_attendance` VALUES (1401, '2024-12-20', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 60);
INSERT INTO `attendance_attendance` VALUES (1402, '2024-12-20', '08:55:08.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 61);
INSERT INTO `attendance_attendance` VALUES (1403, '2024-12-20', '09:05:23.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 62);
INSERT INTO `attendance_attendance` VALUES (1404, '2024-12-20', '08:55:10.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 63);
INSERT INTO `attendance_attendance` VALUES (1405, '2024-12-20', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 64);
INSERT INTO `attendance_attendance` VALUES (1406, '2024-12-20', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 65);
INSERT INTO `attendance_attendance` VALUES (1407, '2024-12-20', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 66);
INSERT INTO `attendance_attendance` VALUES (1408, '2024-12-20', '08:55:02.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 67);
INSERT INTO `attendance_attendance` VALUES (1409, '2024-12-20', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 68);
INSERT INTO `attendance_attendance` VALUES (1410, '2024-12-20', '08:55:03.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 69);
INSERT INTO `attendance_attendance` VALUES (1411, '2024-12-20', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 70);
INSERT INTO `attendance_attendance` VALUES (1412, '2024-12-20', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 71);
INSERT INTO `attendance_attendance` VALUES (1413, '2024-12-20', '08:55:10.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 72);
INSERT INTO `attendance_attendance` VALUES (1414, '2024-12-20', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 73);
INSERT INTO `attendance_attendance` VALUES (1415, '2024-12-20', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 74);
INSERT INTO `attendance_attendance` VALUES (1416, '2024-12-20', NULL, '17:45:09.000000', 'early', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 75);
INSERT INTO `attendance_attendance` VALUES (1417, '2024-12-20', '08:55:10.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 76);
INSERT INTO `attendance_attendance` VALUES (1418, '2024-12-20', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 77);
INSERT INTO `attendance_attendance` VALUES (1419, '2024-12-20', '08:55:07.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 78);
INSERT INTO `attendance_attendance` VALUES (1420, '2024-12-20', '08:55:05.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 79);
INSERT INTO `attendance_attendance` VALUES (1421, '2024-12-20', '08:55:06.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 80);
INSERT INTO `attendance_attendance` VALUES (1422, '2024-12-20', '08:55:09.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 81);
INSERT INTO `attendance_attendance` VALUES (1423, '2024-12-20', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 82);
INSERT INTO `attendance_attendance` VALUES (1424, '2024-12-20', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 83);
INSERT INTO `attendance_attendance` VALUES (1425, '2024-12-20', '08:55:04.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 84);
INSERT INTO `attendance_attendance` VALUES (1426, '2024-12-20', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 85);
INSERT INTO `attendance_attendance` VALUES (1427, '2024-12-20', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 86);
INSERT INTO `attendance_attendance` VALUES (1428, '2024-12-20', '08:55:00.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 87);
INSERT INTO `attendance_attendance` VALUES (1429, '2024-12-20', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 88);
INSERT INTO `attendance_attendance` VALUES (1430, '2024-12-20', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 89);
INSERT INTO `attendance_attendance` VALUES (1431, '2024-12-20', NULL, '17:45:03.000000', 'early', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 90);
INSERT INTO `attendance_attendance` VALUES (1432, '2024-12-20', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 91);
INSERT INTO `attendance_attendance` VALUES (1433, '2024-12-20', '08:55:03.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 92);
INSERT INTO `attendance_attendance` VALUES (1434, '2024-12-20', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 93);
INSERT INTO `attendance_attendance` VALUES (1435, '2024-12-20', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 94);
INSERT INTO `attendance_attendance` VALUES (1436, '2024-12-20', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 95);
INSERT INTO `attendance_attendance` VALUES (1437, '2024-12-20', '08:55:10.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 96);
INSERT INTO `attendance_attendance` VALUES (1438, '2024-12-20', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 97);
INSERT INTO `attendance_attendance` VALUES (1439, '2024-12-20', '08:55:07.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 98);
INSERT INTO `attendance_attendance` VALUES (1440, '2024-12-20', '09:05:10.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 99);
INSERT INTO `attendance_attendance` VALUES (1441, '2024-12-20', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 100);
INSERT INTO `attendance_attendance` VALUES (1442, '2024-12-23', '08:55:05.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 5);
INSERT INTO `attendance_attendance` VALUES (1443, '2024-12-23', '08:55:10.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 6);
INSERT INTO `attendance_attendance` VALUES (1444, '2024-12-23', '08:55:07.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 7);
INSERT INTO `attendance_attendance` VALUES (1445, '2024-12-23', '09:05:16.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 8);
INSERT INTO `attendance_attendance` VALUES (1446, '2024-12-23', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 9);
INSERT INTO `attendance_attendance` VALUES (1447, '2024-12-23', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 10);
INSERT INTO `attendance_attendance` VALUES (1448, '2024-12-23', '08:55:00.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 11);
INSERT INTO `attendance_attendance` VALUES (1449, '2024-12-23', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 12);
INSERT INTO `attendance_attendance` VALUES (1450, '2024-12-23', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 13);
INSERT INTO `attendance_attendance` VALUES (1451, '2024-12-23', '08:55:07.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 14);
INSERT INTO `attendance_attendance` VALUES (1452, '2024-12-23', '09:05:26.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 15);
INSERT INTO `attendance_attendance` VALUES (1453, '2024-12-23', '08:55:01.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 16);
INSERT INTO `attendance_attendance` VALUES (1454, '2024-12-23', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 17);
INSERT INTO `attendance_attendance` VALUES (1455, '2024-12-23', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 18);
INSERT INTO `attendance_attendance` VALUES (1456, '2024-12-23', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 19);
INSERT INTO `attendance_attendance` VALUES (1457, '2024-12-23', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 20);
INSERT INTO `attendance_attendance` VALUES (1458, '2024-12-23', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 21);
INSERT INTO `attendance_attendance` VALUES (1459, '2024-12-23', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 22);
INSERT INTO `attendance_attendance` VALUES (1460, '2024-12-23', '08:55:10.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 23);
INSERT INTO `attendance_attendance` VALUES (1461, '2024-12-23', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 24);
INSERT INTO `attendance_attendance` VALUES (1462, '2024-12-23', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 25);
INSERT INTO `attendance_attendance` VALUES (1463, '2024-12-23', '08:55:01.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 26);
INSERT INTO `attendance_attendance` VALUES (1464, '2024-12-23', '08:55:06.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 27);
INSERT INTO `attendance_attendance` VALUES (1465, '2024-12-23', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 28);
INSERT INTO `attendance_attendance` VALUES (1466, '2024-12-23', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 29);
INSERT INTO `attendance_attendance` VALUES (1467, '2024-12-23', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 30);
INSERT INTO `attendance_attendance` VALUES (1468, '2024-12-23', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 31);
INSERT INTO `attendance_attendance` VALUES (1469, '2024-12-23', '08:55:10.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 32);
INSERT INTO `attendance_attendance` VALUES (1470, '2024-12-23', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 33);
INSERT INTO `attendance_attendance` VALUES (1471, '2024-12-23', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 34);
INSERT INTO `attendance_attendance` VALUES (1472, '2024-12-23', '08:55:05.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 35);
INSERT INTO `attendance_attendance` VALUES (1473, '2024-12-23', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 36);
INSERT INTO `attendance_attendance` VALUES (1474, '2024-12-23', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 37);
INSERT INTO `attendance_attendance` VALUES (1475, '2024-12-23', '08:55:02.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 38);
INSERT INTO `attendance_attendance` VALUES (1476, '2024-12-23', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 39);
INSERT INTO `attendance_attendance` VALUES (1477, '2024-12-23', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 40);
INSERT INTO `attendance_attendance` VALUES (1478, '2024-12-23', '09:05:30.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 41);
INSERT INTO `attendance_attendance` VALUES (1479, '2024-12-23', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 42);
INSERT INTO `attendance_attendance` VALUES (1480, '2024-12-23', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 43);
INSERT INTO `attendance_attendance` VALUES (1481, '2024-12-23', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 44);
INSERT INTO `attendance_attendance` VALUES (1482, '2024-12-23', '08:55:05.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 45);
INSERT INTO `attendance_attendance` VALUES (1483, '2024-12-23', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 46);
INSERT INTO `attendance_attendance` VALUES (1484, '2024-12-23', '08:55:06.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 47);
INSERT INTO `attendance_attendance` VALUES (1485, '2024-12-23', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 48);
INSERT INTO `attendance_attendance` VALUES (1486, '2024-12-23', '09:05:16.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 49);
INSERT INTO `attendance_attendance` VALUES (1487, '2024-12-23', NULL, NULL, 'absent', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 50);
INSERT INTO `attendance_attendance` VALUES (1488, '2024-12-23', '08:55:08.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 51);
INSERT INTO `attendance_attendance` VALUES (1489, '2024-12-23', '08:55:03.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 52);
INSERT INTO `attendance_attendance` VALUES (1490, '2024-12-23', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 53);
INSERT INTO `attendance_attendance` VALUES (1491, '2024-12-23', '08:55:01.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 54);
INSERT INTO `attendance_attendance` VALUES (1492, '2024-12-23', '08:55:08.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 55);
INSERT INTO `attendance_attendance` VALUES (1493, '2024-12-23', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 56);
INSERT INTO `attendance_attendance` VALUES (1494, '2024-12-23', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 57);
INSERT INTO `attendance_attendance` VALUES (1495, '2024-12-23', '08:55:00.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 58);
INSERT INTO `attendance_attendance` VALUES (1496, '2024-12-23', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 59);
INSERT INTO `attendance_attendance` VALUES (1497, '2024-12-23', '08:55:05.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 60);
INSERT INTO `attendance_attendance` VALUES (1498, '2024-12-23', '08:55:09.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 61);
INSERT INTO `attendance_attendance` VALUES (1499, '2024-12-23', '08:55:08.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 62);
INSERT INTO `attendance_attendance` VALUES (1500, '2024-12-23', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 63);
INSERT INTO `attendance_attendance` VALUES (1501, '2024-12-23', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 64);
INSERT INTO `attendance_attendance` VALUES (1502, '2024-12-23', '08:55:05.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 65);
INSERT INTO `attendance_attendance` VALUES (1503, '2024-12-23', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 66);
INSERT INTO `attendance_attendance` VALUES (1504, '2024-12-23', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 67);
INSERT INTO `attendance_attendance` VALUES (1505, '2024-12-23', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 68);
INSERT INTO `attendance_attendance` VALUES (1506, '2024-12-23', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 69);
INSERT INTO `attendance_attendance` VALUES (1507, '2024-12-23', NULL, NULL, 'absent', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 70);
INSERT INTO `attendance_attendance` VALUES (1508, '2024-12-23', '08:55:04.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 71);
INSERT INTO `attendance_attendance` VALUES (1509, '2024-12-23', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 72);
INSERT INTO `attendance_attendance` VALUES (1510, '2024-12-23', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 73);
INSERT INTO `attendance_attendance` VALUES (1511, '2024-12-23', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 74);
INSERT INTO `attendance_attendance` VALUES (1512, '2024-12-23', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 75);
INSERT INTO `attendance_attendance` VALUES (1513, '2024-12-23', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 76);
INSERT INTO `attendance_attendance` VALUES (1514, '2024-12-23', '09:05:04.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 77);
INSERT INTO `attendance_attendance` VALUES (1515, '2024-12-23', '08:55:10.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 78);
INSERT INTO `attendance_attendance` VALUES (1516, '2024-12-23', '09:05:27.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 79);
INSERT INTO `attendance_attendance` VALUES (1517, '2024-12-23', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 80);
INSERT INTO `attendance_attendance` VALUES (1518, '2024-12-23', '09:05:30.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 81);
INSERT INTO `attendance_attendance` VALUES (1519, '2024-12-23', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 82);
INSERT INTO `attendance_attendance` VALUES (1520, '2024-12-23', '08:55:00.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 83);
INSERT INTO `attendance_attendance` VALUES (1521, '2024-12-23', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 84);
INSERT INTO `attendance_attendance` VALUES (1522, '2024-12-23', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 85);
INSERT INTO `attendance_attendance` VALUES (1523, '2024-12-23', '09:05:11.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 86);
INSERT INTO `attendance_attendance` VALUES (1524, '2024-12-23', '08:55:06.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 87);
INSERT INTO `attendance_attendance` VALUES (1525, '2024-12-23', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 88);
INSERT INTO `attendance_attendance` VALUES (1526, '2024-12-23', '08:55:08.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 89);
INSERT INTO `attendance_attendance` VALUES (1527, '2024-12-23', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 90);
INSERT INTO `attendance_attendance` VALUES (1528, '2024-12-23', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 91);
INSERT INTO `attendance_attendance` VALUES (1529, '2024-12-23', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 92);
INSERT INTO `attendance_attendance` VALUES (1530, '2024-12-23', '08:55:03.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 93);
INSERT INTO `attendance_attendance` VALUES (1531, '2024-12-23', NULL, NULL, 'absent', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 94);
INSERT INTO `attendance_attendance` VALUES (1532, '2024-12-23', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 95);
INSERT INTO `attendance_attendance` VALUES (1533, '2024-12-23', NULL, NULL, 'absent', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 96);
INSERT INTO `attendance_attendance` VALUES (1534, '2024-12-23', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 97);
INSERT INTO `attendance_attendance` VALUES (1535, '2024-12-23', '09:05:10.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 98);
INSERT INTO `attendance_attendance` VALUES (1536, '2024-12-23', '09:05:20.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 99);
INSERT INTO `attendance_attendance` VALUES (1537, '2024-12-23', '08:55:05.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 100);
INSERT INTO `attendance_attendance` VALUES (1538, '2024-12-24', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 5);
INSERT INTO `attendance_attendance` VALUES (1539, '2024-12-24', '08:55:09.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 6);
INSERT INTO `attendance_attendance` VALUES (1540, '2024-12-24', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 7);
INSERT INTO `attendance_attendance` VALUES (1541, '2024-12-24', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 8);
INSERT INTO `attendance_attendance` VALUES (1542, '2024-12-24', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 9);
INSERT INTO `attendance_attendance` VALUES (1543, '2024-12-24', '09:05:22.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 10);
INSERT INTO `attendance_attendance` VALUES (1544, '2024-12-24', NULL, NULL, 'absent', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 11);
INSERT INTO `attendance_attendance` VALUES (1545, '2024-12-24', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 12);
INSERT INTO `attendance_attendance` VALUES (1546, '2024-12-24', NULL, NULL, 'absent', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 13);
INSERT INTO `attendance_attendance` VALUES (1547, '2024-12-24', '08:55:05.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 14);
INSERT INTO `attendance_attendance` VALUES (1548, '2024-12-24', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 15);
INSERT INTO `attendance_attendance` VALUES (1549, '2024-12-24', '08:55:02.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 16);
INSERT INTO `attendance_attendance` VALUES (1550, '2024-12-24', '08:55:01.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 17);
INSERT INTO `attendance_attendance` VALUES (1551, '2024-12-24', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 18);
INSERT INTO `attendance_attendance` VALUES (1552, '2024-12-24', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 19);
INSERT INTO `attendance_attendance` VALUES (1553, '2024-12-24', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 20);
INSERT INTO `attendance_attendance` VALUES (1554, '2024-12-24', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 21);
INSERT INTO `attendance_attendance` VALUES (1555, '2024-12-24', '09:05:18.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 22);
INSERT INTO `attendance_attendance` VALUES (1556, '2024-12-24', '08:55:01.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 23);
INSERT INTO `attendance_attendance` VALUES (1557, '2024-12-24', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 24);
INSERT INTO `attendance_attendance` VALUES (1558, '2024-12-24', '08:55:00.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 25);
INSERT INTO `attendance_attendance` VALUES (1559, '2024-12-24', '08:55:02.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 26);
INSERT INTO `attendance_attendance` VALUES (1560, '2024-12-24', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 27);
INSERT INTO `attendance_attendance` VALUES (1561, '2024-12-24', '09:05:20.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 28);
INSERT INTO `attendance_attendance` VALUES (1562, '2024-12-24', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 29);
INSERT INTO `attendance_attendance` VALUES (1563, '2024-12-24', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 30);
INSERT INTO `attendance_attendance` VALUES (1564, '2024-12-24', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 31);
INSERT INTO `attendance_attendance` VALUES (1565, '2024-12-24', '08:55:07.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 32);
INSERT INTO `attendance_attendance` VALUES (1566, '2024-12-24', NULL, '17:45:07.000000', 'early', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 33);
INSERT INTO `attendance_attendance` VALUES (1567, '2024-12-24', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 34);
INSERT INTO `attendance_attendance` VALUES (1568, '2024-12-24', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 35);
INSERT INTO `attendance_attendance` VALUES (1569, '2024-12-24', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 36);
INSERT INTO `attendance_attendance` VALUES (1570, '2024-12-24', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 37);
INSERT INTO `attendance_attendance` VALUES (1571, '2024-12-24', '09:05:13.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 38);
INSERT INTO `attendance_attendance` VALUES (1572, '2024-12-24', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 39);
INSERT INTO `attendance_attendance` VALUES (1573, '2024-12-24', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 40);
INSERT INTO `attendance_attendance` VALUES (1574, '2024-12-24', '08:55:00.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 41);
INSERT INTO `attendance_attendance` VALUES (1575, '2024-12-24', '08:55:06.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 42);
INSERT INTO `attendance_attendance` VALUES (1576, '2024-12-24', '09:05:05.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 43);
INSERT INTO `attendance_attendance` VALUES (1577, '2024-12-24', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 44);
INSERT INTO `attendance_attendance` VALUES (1578, '2024-12-24', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 45);
INSERT INTO `attendance_attendance` VALUES (1579, '2024-12-24', '08:55:02.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 46);
INSERT INTO `attendance_attendance` VALUES (1580, '2024-12-24', '08:55:03.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 47);
INSERT INTO `attendance_attendance` VALUES (1581, '2024-12-24', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 48);
INSERT INTO `attendance_attendance` VALUES (1582, '2024-12-24', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 49);
INSERT INTO `attendance_attendance` VALUES (1583, '2024-12-24', '08:55:00.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 50);
INSERT INTO `attendance_attendance` VALUES (1584, '2024-12-24', '08:55:00.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 51);
INSERT INTO `attendance_attendance` VALUES (1585, '2024-12-24', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 52);
INSERT INTO `attendance_attendance` VALUES (1586, '2024-12-24', '08:55:00.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 53);
INSERT INTO `attendance_attendance` VALUES (1587, '2024-12-24', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 54);
INSERT INTO `attendance_attendance` VALUES (1588, '2024-12-24', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 55);
INSERT INTO `attendance_attendance` VALUES (1589, '2024-12-24', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 56);
INSERT INTO `attendance_attendance` VALUES (1590, '2024-12-24', '09:05:09.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 57);
INSERT INTO `attendance_attendance` VALUES (1591, '2024-12-24', NULL, NULL, 'absent', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 58);
INSERT INTO `attendance_attendance` VALUES (1592, '2024-12-24', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 59);
INSERT INTO `attendance_attendance` VALUES (1593, '2024-12-24', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 60);
INSERT INTO `attendance_attendance` VALUES (1594, '2024-12-24', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 61);
INSERT INTO `attendance_attendance` VALUES (1595, '2024-12-24', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 62);
INSERT INTO `attendance_attendance` VALUES (1596, '2024-12-24', '08:55:06.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 63);
INSERT INTO `attendance_attendance` VALUES (1597, '2024-12-24', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 64);
INSERT INTO `attendance_attendance` VALUES (1598, '2024-12-24', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 65);
INSERT INTO `attendance_attendance` VALUES (1599, '2024-12-24', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 66);
INSERT INTO `attendance_attendance` VALUES (1600, '2024-12-24', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 67);
INSERT INTO `attendance_attendance` VALUES (1601, '2024-12-24', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 68);
INSERT INTO `attendance_attendance` VALUES (1602, '2024-12-24', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 69);
INSERT INTO `attendance_attendance` VALUES (1603, '2024-12-24', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 70);
INSERT INTO `attendance_attendance` VALUES (1604, '2024-12-24', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 71);
INSERT INTO `attendance_attendance` VALUES (1605, '2024-12-24', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 72);
INSERT INTO `attendance_attendance` VALUES (1606, '2024-12-24', NULL, NULL, 'absent', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 73);
INSERT INTO `attendance_attendance` VALUES (1607, '2024-12-24', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 74);
INSERT INTO `attendance_attendance` VALUES (1608, '2024-12-24', '09:05:09.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 75);
INSERT INTO `attendance_attendance` VALUES (1609, '2024-12-24', '08:55:00.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 76);
INSERT INTO `attendance_attendance` VALUES (1610, '2024-12-24', '08:55:10.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 77);
INSERT INTO `attendance_attendance` VALUES (1611, '2024-12-24', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 78);
INSERT INTO `attendance_attendance` VALUES (1612, '2024-12-24', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 79);
INSERT INTO `attendance_attendance` VALUES (1613, '2024-12-24', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 80);
INSERT INTO `attendance_attendance` VALUES (1614, '2024-12-24', '09:05:25.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 81);
INSERT INTO `attendance_attendance` VALUES (1615, '2024-12-24', '08:55:10.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 82);
INSERT INTO `attendance_attendance` VALUES (1616, '2024-12-24', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 83);
INSERT INTO `attendance_attendance` VALUES (1617, '2024-12-24', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 84);
INSERT INTO `attendance_attendance` VALUES (1618, '2024-12-24', '08:55:09.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 85);
INSERT INTO `attendance_attendance` VALUES (1619, '2024-12-24', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 86);
INSERT INTO `attendance_attendance` VALUES (1620, '2024-12-24', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 87);
INSERT INTO `attendance_attendance` VALUES (1621, '2024-12-24', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 88);
INSERT INTO `attendance_attendance` VALUES (1622, '2024-12-24', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 89);
INSERT INTO `attendance_attendance` VALUES (1623, '2024-12-24', '08:55:10.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 90);
INSERT INTO `attendance_attendance` VALUES (1624, '2024-12-24', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 91);
INSERT INTO `attendance_attendance` VALUES (1625, '2024-12-24', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 92);
INSERT INTO `attendance_attendance` VALUES (1626, '2024-12-24', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 93);
INSERT INTO `attendance_attendance` VALUES (1627, '2024-12-24', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 94);
INSERT INTO `attendance_attendance` VALUES (1628, '2024-12-24', '09:05:22.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 95);
INSERT INTO `attendance_attendance` VALUES (1629, '2024-12-24', '08:55:10.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 96);
INSERT INTO `attendance_attendance` VALUES (1630, '2024-12-24', '09:05:18.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 97);
INSERT INTO `attendance_attendance` VALUES (1631, '2024-12-24', '08:55:02.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 98);
INSERT INTO `attendance_attendance` VALUES (1632, '2024-12-24', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 99);
INSERT INTO `attendance_attendance` VALUES (1633, '2024-12-24', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 100);
INSERT INTO `attendance_attendance` VALUES (1634, '2024-12-25', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 5);
INSERT INTO `attendance_attendance` VALUES (1635, '2024-12-25', '08:55:03.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 6);
INSERT INTO `attendance_attendance` VALUES (1636, '2024-12-25', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 7);
INSERT INTO `attendance_attendance` VALUES (1637, '2024-12-25', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 8);
INSERT INTO `attendance_attendance` VALUES (1638, '2024-12-25', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 9);
INSERT INTO `attendance_attendance` VALUES (1639, '2024-12-25', '08:55:02.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 10);
INSERT INTO `attendance_attendance` VALUES (1640, '2024-12-25', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 11);
INSERT INTO `attendance_attendance` VALUES (1641, '2024-12-25', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 12);
INSERT INTO `attendance_attendance` VALUES (1642, '2024-12-25', '08:55:07.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 13);
INSERT INTO `attendance_attendance` VALUES (1643, '2024-12-25', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 14);
INSERT INTO `attendance_attendance` VALUES (1644, '2024-12-25', '08:55:08.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 15);
INSERT INTO `attendance_attendance` VALUES (1645, '2024-12-25', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 16);
INSERT INTO `attendance_attendance` VALUES (1646, '2024-12-25', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 17);
INSERT INTO `attendance_attendance` VALUES (1647, '2024-12-25', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 18);
INSERT INTO `attendance_attendance` VALUES (1648, '2024-12-25', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 19);
INSERT INTO `attendance_attendance` VALUES (1649, '2024-12-25', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 20);
INSERT INTO `attendance_attendance` VALUES (1650, '2024-12-25', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 21);
INSERT INTO `attendance_attendance` VALUES (1651, '2024-12-25', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 22);
INSERT INTO `attendance_attendance` VALUES (1652, '2024-12-25', NULL, NULL, 'absent', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 23);
INSERT INTO `attendance_attendance` VALUES (1653, '2024-12-25', '08:55:00.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 24);
INSERT INTO `attendance_attendance` VALUES (1654, '2024-12-25', '09:05:06.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 25);
INSERT INTO `attendance_attendance` VALUES (1655, '2024-12-25', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 26);
INSERT INTO `attendance_attendance` VALUES (1656, '2024-12-25', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 27);
INSERT INTO `attendance_attendance` VALUES (1657, '2024-12-25', NULL, '17:45:00.000000', 'early', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 28);
INSERT INTO `attendance_attendance` VALUES (1658, '2024-12-25', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 29);
INSERT INTO `attendance_attendance` VALUES (1659, '2024-12-25', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 30);
INSERT INTO `attendance_attendance` VALUES (1660, '2024-12-25', '09:05:14.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 31);
INSERT INTO `attendance_attendance` VALUES (1661, '2024-12-25', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 32);
INSERT INTO `attendance_attendance` VALUES (1662, '2024-12-25', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 33);
INSERT INTO `attendance_attendance` VALUES (1663, '2024-12-25', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 34);
INSERT INTO `attendance_attendance` VALUES (1664, '2024-12-25', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 35);
INSERT INTO `attendance_attendance` VALUES (1665, '2024-12-25', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 36);
INSERT INTO `attendance_attendance` VALUES (1666, '2024-12-25', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 37);
INSERT INTO `attendance_attendance` VALUES (1667, '2024-12-25', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 38);
INSERT INTO `attendance_attendance` VALUES (1668, '2024-12-25', '08:55:00.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 39);
INSERT INTO `attendance_attendance` VALUES (1669, '2024-12-25', '08:55:07.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 40);
INSERT INTO `attendance_attendance` VALUES (1670, '2024-12-25', '08:55:08.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 41);
INSERT INTO `attendance_attendance` VALUES (1671, '2024-12-25', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 42);
INSERT INTO `attendance_attendance` VALUES (1672, '2024-12-25', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 43);
INSERT INTO `attendance_attendance` VALUES (1673, '2024-12-25', '08:55:08.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 44);
INSERT INTO `attendance_attendance` VALUES (1674, '2024-12-25', '08:55:01.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 45);
INSERT INTO `attendance_attendance` VALUES (1675, '2024-12-25', NULL, NULL, 'absent', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 46);
INSERT INTO `attendance_attendance` VALUES (1676, '2024-12-25', '08:55:06.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 47);
INSERT INTO `attendance_attendance` VALUES (1677, '2024-12-25', '08:55:00.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 48);
INSERT INTO `attendance_attendance` VALUES (1678, '2024-12-25', '08:55:07.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 49);
INSERT INTO `attendance_attendance` VALUES (1679, '2024-12-25', '09:05:21.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 50);
INSERT INTO `attendance_attendance` VALUES (1680, '2024-12-25', '09:05:05.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 51);
INSERT INTO `attendance_attendance` VALUES (1681, '2024-12-25', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 52);
INSERT INTO `attendance_attendance` VALUES (1682, '2024-12-25', '08:55:08.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 53);
INSERT INTO `attendance_attendance` VALUES (1683, '2024-12-25', '08:55:05.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 54);
INSERT INTO `attendance_attendance` VALUES (1684, '2024-12-25', '08:55:04.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 55);
INSERT INTO `attendance_attendance` VALUES (1685, '2024-12-25', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 56);
INSERT INTO `attendance_attendance` VALUES (1686, '2024-12-25', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 57);
INSERT INTO `attendance_attendance` VALUES (1687, '2024-12-25', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 58);
INSERT INTO `attendance_attendance` VALUES (1688, '2024-12-25', '08:55:01.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 59);
INSERT INTO `attendance_attendance` VALUES (1689, '2024-12-25', '08:55:10.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 60);
INSERT INTO `attendance_attendance` VALUES (1690, '2024-12-25', '08:55:09.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 61);
INSERT INTO `attendance_attendance` VALUES (1691, '2024-12-25', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 62);
INSERT INTO `attendance_attendance` VALUES (1692, '2024-12-25', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 63);
INSERT INTO `attendance_attendance` VALUES (1693, '2024-12-25', '08:55:07.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 64);
INSERT INTO `attendance_attendance` VALUES (1694, '2024-12-25', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 65);
INSERT INTO `attendance_attendance` VALUES (1695, '2024-12-25', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 66);
INSERT INTO `attendance_attendance` VALUES (1696, '2024-12-25', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 67);
INSERT INTO `attendance_attendance` VALUES (1697, '2024-12-25', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 68);
INSERT INTO `attendance_attendance` VALUES (1698, '2024-12-25', '08:55:08.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 69);
INSERT INTO `attendance_attendance` VALUES (1699, '2024-12-25', '09:05:23.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 70);
INSERT INTO `attendance_attendance` VALUES (1700, '2024-12-25', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 71);
INSERT INTO `attendance_attendance` VALUES (1701, '2024-12-25', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 72);
INSERT INTO `attendance_attendance` VALUES (1702, '2024-12-25', '08:55:00.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 73);
INSERT INTO `attendance_attendance` VALUES (1703, '2024-12-25', NULL, NULL, 'absent', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 74);
INSERT INTO `attendance_attendance` VALUES (1704, '2024-12-25', '08:55:06.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 75);
INSERT INTO `attendance_attendance` VALUES (1705, '2024-12-25', NULL, NULL, 'absent', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 76);
INSERT INTO `attendance_attendance` VALUES (1706, '2024-12-25', '08:55:02.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 77);
INSERT INTO `attendance_attendance` VALUES (1707, '2024-12-25', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 78);
INSERT INTO `attendance_attendance` VALUES (1708, '2024-12-25', '08:55:02.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 79);
INSERT INTO `attendance_attendance` VALUES (1709, '2024-12-25', '08:55:10.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 80);
INSERT INTO `attendance_attendance` VALUES (1710, '2024-12-25', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 81);
INSERT INTO `attendance_attendance` VALUES (1711, '2024-12-25', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 82);
INSERT INTO `attendance_attendance` VALUES (1712, '2024-12-25', '08:55:09.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 83);
INSERT INTO `attendance_attendance` VALUES (1713, '2024-12-25', '08:55:04.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 84);
INSERT INTO `attendance_attendance` VALUES (1714, '2024-12-25', '08:55:00.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 85);
INSERT INTO `attendance_attendance` VALUES (1715, '2024-12-25', '09:05:16.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 86);
INSERT INTO `attendance_attendance` VALUES (1716, '2024-12-25', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 87);
INSERT INTO `attendance_attendance` VALUES (1717, '2024-12-25', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 88);
INSERT INTO `attendance_attendance` VALUES (1718, '2024-12-25', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 89);
INSERT INTO `attendance_attendance` VALUES (1719, '2024-12-25', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 90);
INSERT INTO `attendance_attendance` VALUES (1720, '2024-12-25', '08:55:08.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 91);
INSERT INTO `attendance_attendance` VALUES (1721, '2024-12-25', '08:55:05.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 92);
INSERT INTO `attendance_attendance` VALUES (1722, '2024-12-25', '09:05:25.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 93);
INSERT INTO `attendance_attendance` VALUES (1723, '2024-12-25', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 94);
INSERT INTO `attendance_attendance` VALUES (1724, '2024-12-25', '08:55:06.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 95);
INSERT INTO `attendance_attendance` VALUES (1725, '2024-12-25', '08:55:00.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 96);
INSERT INTO `attendance_attendance` VALUES (1726, '2024-12-25', '08:55:01.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 97);
INSERT INTO `attendance_attendance` VALUES (1727, '2024-12-25', '08:55:00.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 98);
INSERT INTO `attendance_attendance` VALUES (1728, '2024-12-25', '08:55:02.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 99);
INSERT INTO `attendance_attendance` VALUES (1729, '2024-12-25', '08:55:05.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 100);
INSERT INTO `attendance_attendance` VALUES (1730, '2024-12-26', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 5);
INSERT INTO `attendance_attendance` VALUES (1731, '2024-12-26', '08:55:09.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 6);
INSERT INTO `attendance_attendance` VALUES (1732, '2024-12-26', '08:55:05.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 7);
INSERT INTO `attendance_attendance` VALUES (1733, '2024-12-26', '08:55:01.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 8);
INSERT INTO `attendance_attendance` VALUES (1734, '2024-12-26', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 9);
INSERT INTO `attendance_attendance` VALUES (1735, '2024-12-26', '08:55:01.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 10);
INSERT INTO `attendance_attendance` VALUES (1736, '2024-12-26', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 11);
INSERT INTO `attendance_attendance` VALUES (1737, '2024-12-26', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 12);
INSERT INTO `attendance_attendance` VALUES (1738, '2024-12-26', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 13);
INSERT INTO `attendance_attendance` VALUES (1739, '2024-12-26', '08:55:02.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 14);
INSERT INTO `attendance_attendance` VALUES (1740, '2024-12-26', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 15);
INSERT INTO `attendance_attendance` VALUES (1741, '2024-12-26', '08:55:06.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 16);
INSERT INTO `attendance_attendance` VALUES (1742, '2024-12-26', '08:55:00.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 17);
INSERT INTO `attendance_attendance` VALUES (1743, '2024-12-26', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 18);
INSERT INTO `attendance_attendance` VALUES (1744, '2024-12-26', NULL, NULL, 'absent', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 19);
INSERT INTO `attendance_attendance` VALUES (1745, '2024-12-26', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 20);
INSERT INTO `attendance_attendance` VALUES (1746, '2024-12-26', '08:55:00.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 21);
INSERT INTO `attendance_attendance` VALUES (1747, '2024-12-26', '08:55:04.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 22);
INSERT INTO `attendance_attendance` VALUES (1748, '2024-12-26', '08:55:03.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 23);
INSERT INTO `attendance_attendance` VALUES (1749, '2024-12-26', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 24);
INSERT INTO `attendance_attendance` VALUES (1750, '2024-12-26', '08:55:10.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 25);
INSERT INTO `attendance_attendance` VALUES (1751, '2024-12-26', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 26);
INSERT INTO `attendance_attendance` VALUES (1752, '2024-12-26', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 27);
INSERT INTO `attendance_attendance` VALUES (1753, '2024-12-26', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 28);
INSERT INTO `attendance_attendance` VALUES (1754, '2024-12-26', '08:55:01.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 29);
INSERT INTO `attendance_attendance` VALUES (1755, '2024-12-26', '08:55:10.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 30);
INSERT INTO `attendance_attendance` VALUES (1756, '2024-12-26', '09:05:27.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 31);
INSERT INTO `attendance_attendance` VALUES (1757, '2024-12-26', '08:55:09.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 32);
INSERT INTO `attendance_attendance` VALUES (1758, '2024-12-26', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 33);
INSERT INTO `attendance_attendance` VALUES (1759, '2024-12-26', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 34);
INSERT INTO `attendance_attendance` VALUES (1760, '2024-12-26', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 35);
INSERT INTO `attendance_attendance` VALUES (1761, '2024-12-26', '08:55:10.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 36);
INSERT INTO `attendance_attendance` VALUES (1762, '2024-12-26', '09:05:09.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 37);
INSERT INTO `attendance_attendance` VALUES (1763, '2024-12-26', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 38);
INSERT INTO `attendance_attendance` VALUES (1764, '2024-12-26', '08:55:02.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 39);
INSERT INTO `attendance_attendance` VALUES (1765, '2024-12-26', NULL, NULL, 'absent', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 40);
INSERT INTO `attendance_attendance` VALUES (1766, '2024-12-26', '08:55:07.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 41);
INSERT INTO `attendance_attendance` VALUES (1767, '2024-12-26', '08:55:06.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 42);
INSERT INTO `attendance_attendance` VALUES (1768, '2024-12-26', NULL, '17:45:03.000000', 'early', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 43);
INSERT INTO `attendance_attendance` VALUES (1769, '2024-12-26', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 44);
INSERT INTO `attendance_attendance` VALUES (1770, '2024-12-26', '08:55:10.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 45);
INSERT INTO `attendance_attendance` VALUES (1771, '2024-12-26', '08:55:10.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 46);
INSERT INTO `attendance_attendance` VALUES (1772, '2024-12-26', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 47);
INSERT INTO `attendance_attendance` VALUES (1773, '2024-12-26', '08:55:01.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 48);
INSERT INTO `attendance_attendance` VALUES (1774, '2024-12-26', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 49);
INSERT INTO `attendance_attendance` VALUES (1775, '2024-12-26', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 50);
INSERT INTO `attendance_attendance` VALUES (1776, '2024-12-26', '08:55:00.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 51);
INSERT INTO `attendance_attendance` VALUES (1777, '2024-12-26', '08:55:06.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 52);
INSERT INTO `attendance_attendance` VALUES (1778, '2024-12-26', '08:55:10.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 53);
INSERT INTO `attendance_attendance` VALUES (1779, '2024-12-26', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 54);
INSERT INTO `attendance_attendance` VALUES (1780, '2024-12-26', '09:05:03.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 55);
INSERT INTO `attendance_attendance` VALUES (1781, '2024-12-26', '09:05:02.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 56);
INSERT INTO `attendance_attendance` VALUES (1782, '2024-12-26', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 57);
INSERT INTO `attendance_attendance` VALUES (1783, '2024-12-26', NULL, NULL, 'absent', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 58);
INSERT INTO `attendance_attendance` VALUES (1784, '2024-12-26', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 59);
INSERT INTO `attendance_attendance` VALUES (1785, '2024-12-26', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 60);
INSERT INTO `attendance_attendance` VALUES (1786, '2024-12-26', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 61);
INSERT INTO `attendance_attendance` VALUES (1787, '2024-12-26', '08:55:01.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 62);
INSERT INTO `attendance_attendance` VALUES (1788, '2024-12-26', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 63);
INSERT INTO `attendance_attendance` VALUES (1789, '2024-12-26', '08:55:06.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 64);
INSERT INTO `attendance_attendance` VALUES (1790, '2024-12-26', NULL, '17:45:04.000000', 'early', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 65);
INSERT INTO `attendance_attendance` VALUES (1791, '2024-12-26', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 66);
INSERT INTO `attendance_attendance` VALUES (1792, '2024-12-26', '08:55:06.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 67);
INSERT INTO `attendance_attendance` VALUES (1793, '2024-12-26', '08:55:10.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 68);
INSERT INTO `attendance_attendance` VALUES (1794, '2024-12-26', '08:55:00.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 69);
INSERT INTO `attendance_attendance` VALUES (1795, '2024-12-26', '08:55:06.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 70);
INSERT INTO `attendance_attendance` VALUES (1796, '2024-12-26', '08:55:08.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 71);
INSERT INTO `attendance_attendance` VALUES (1797, '2024-12-26', '08:55:03.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 72);
INSERT INTO `attendance_attendance` VALUES (1798, '2024-12-26', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 73);
INSERT INTO `attendance_attendance` VALUES (1799, '2024-12-26', '09:05:22.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 74);
INSERT INTO `attendance_attendance` VALUES (1800, '2024-12-26', '08:55:10.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 75);
INSERT INTO `attendance_attendance` VALUES (1801, '2024-12-26', '09:05:09.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 76);
INSERT INTO `attendance_attendance` VALUES (1802, '2024-12-26', '09:05:18.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 77);
INSERT INTO `attendance_attendance` VALUES (1803, '2024-12-26', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 78);
INSERT INTO `attendance_attendance` VALUES (1804, '2024-12-26', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 79);
INSERT INTO `attendance_attendance` VALUES (1805, '2024-12-26', '08:55:06.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 80);
INSERT INTO `attendance_attendance` VALUES (1806, '2024-12-26', '09:05:03.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 81);
INSERT INTO `attendance_attendance` VALUES (1807, '2024-12-26', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 82);
INSERT INTO `attendance_attendance` VALUES (1808, '2024-12-26', '09:05:14.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 83);
INSERT INTO `attendance_attendance` VALUES (1809, '2024-12-26', '08:55:06.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 84);
INSERT INTO `attendance_attendance` VALUES (1810, '2024-12-26', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 85);
INSERT INTO `attendance_attendance` VALUES (1811, '2024-12-26', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 86);
INSERT INTO `attendance_attendance` VALUES (1812, '2024-12-26', '08:55:07.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 87);
INSERT INTO `attendance_attendance` VALUES (1813, '2024-12-26', '08:55:09.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 88);
INSERT INTO `attendance_attendance` VALUES (1814, '2024-12-26', '08:55:08.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 89);
INSERT INTO `attendance_attendance` VALUES (1815, '2024-12-26', '08:55:10.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 90);
INSERT INTO `attendance_attendance` VALUES (1816, '2024-12-26', '08:55:01.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 91);
INSERT INTO `attendance_attendance` VALUES (1817, '2024-12-26', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 92);
INSERT INTO `attendance_attendance` VALUES (1818, '2024-12-26', '08:55:00.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 93);
INSERT INTO `attendance_attendance` VALUES (1819, '2024-12-26', '09:05:27.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 94);
INSERT INTO `attendance_attendance` VALUES (1820, '2024-12-26', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 95);
INSERT INTO `attendance_attendance` VALUES (1821, '2024-12-26', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 96);
INSERT INTO `attendance_attendance` VALUES (1822, '2024-12-26', '08:55:08.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 97);
INSERT INTO `attendance_attendance` VALUES (1823, '2024-12-26', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 98);
INSERT INTO `attendance_attendance` VALUES (1824, '2024-12-26', '08:55:07.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 99);
INSERT INTO `attendance_attendance` VALUES (1825, '2024-12-26', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 100);
INSERT INTO `attendance_attendance` VALUES (1826, '2024-12-27', '08:55:01.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 5);
INSERT INTO `attendance_attendance` VALUES (1827, '2024-12-27', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 6);
INSERT INTO `attendance_attendance` VALUES (1828, '2024-12-27', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 7);
INSERT INTO `attendance_attendance` VALUES (1829, '2024-12-27', '08:55:03.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 8);
INSERT INTO `attendance_attendance` VALUES (1830, '2024-12-27', NULL, '17:45:09.000000', 'early', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 9);
INSERT INTO `attendance_attendance` VALUES (1831, '2024-12-27', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 10);
INSERT INTO `attendance_attendance` VALUES (1832, '2024-12-27', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 11);
INSERT INTO `attendance_attendance` VALUES (1833, '2024-12-27', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 12);
INSERT INTO `attendance_attendance` VALUES (1834, '2024-12-27', '08:55:05.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 13);
INSERT INTO `attendance_attendance` VALUES (1835, '2024-12-27', '08:55:00.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 14);
INSERT INTO `attendance_attendance` VALUES (1836, '2024-12-27', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 15);
INSERT INTO `attendance_attendance` VALUES (1837, '2024-12-27', '09:05:02.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 16);
INSERT INTO `attendance_attendance` VALUES (1838, '2024-12-27', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 17);
INSERT INTO `attendance_attendance` VALUES (1839, '2024-12-27', '08:55:03.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 18);
INSERT INTO `attendance_attendance` VALUES (1840, '2024-12-27', '08:55:00.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 19);
INSERT INTO `attendance_attendance` VALUES (1841, '2024-12-27', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 20);
INSERT INTO `attendance_attendance` VALUES (1842, '2024-12-27', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 21);
INSERT INTO `attendance_attendance` VALUES (1843, '2024-12-27', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 22);
INSERT INTO `attendance_attendance` VALUES (1844, '2024-12-27', '08:55:09.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 23);
INSERT INTO `attendance_attendance` VALUES (1845, '2024-12-27', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 24);
INSERT INTO `attendance_attendance` VALUES (1846, '2024-12-27', '09:05:04.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 25);
INSERT INTO `attendance_attendance` VALUES (1847, '2024-12-27', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 26);
INSERT INTO `attendance_attendance` VALUES (1848, '2024-12-27', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 27);
INSERT INTO `attendance_attendance` VALUES (1849, '2024-12-27', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 28);
INSERT INTO `attendance_attendance` VALUES (1850, '2024-12-27', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 29);
INSERT INTO `attendance_attendance` VALUES (1851, '2024-12-27', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 30);
INSERT INTO `attendance_attendance` VALUES (1852, '2024-12-27', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 31);
INSERT INTO `attendance_attendance` VALUES (1853, '2024-12-27', '08:55:05.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 32);
INSERT INTO `attendance_attendance` VALUES (1854, '2024-12-27', '08:55:04.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 33);
INSERT INTO `attendance_attendance` VALUES (1855, '2024-12-27', '08:55:10.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 34);
INSERT INTO `attendance_attendance` VALUES (1856, '2024-12-27', '09:05:17.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 35);
INSERT INTO `attendance_attendance` VALUES (1857, '2024-12-27', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 36);
INSERT INTO `attendance_attendance` VALUES (1858, '2024-12-27', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 37);
INSERT INTO `attendance_attendance` VALUES (1859, '2024-12-27', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 38);
INSERT INTO `attendance_attendance` VALUES (1860, '2024-12-27', '08:55:01.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 39);
INSERT INTO `attendance_attendance` VALUES (1861, '2024-12-27', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 40);
INSERT INTO `attendance_attendance` VALUES (1862, '2024-12-27', '08:55:10.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 41);
INSERT INTO `attendance_attendance` VALUES (1863, '2024-12-27', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 42);
INSERT INTO `attendance_attendance` VALUES (1864, '2024-12-27', NULL, '17:45:07.000000', 'early', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 43);
INSERT INTO `attendance_attendance` VALUES (1865, '2024-12-27', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 44);
INSERT INTO `attendance_attendance` VALUES (1866, '2024-12-27', '09:05:01.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 45);
INSERT INTO `attendance_attendance` VALUES (1867, '2024-12-27', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 46);
INSERT INTO `attendance_attendance` VALUES (1868, '2024-12-27', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 47);
INSERT INTO `attendance_attendance` VALUES (1869, '2024-12-27', '08:55:03.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 48);
INSERT INTO `attendance_attendance` VALUES (1870, '2024-12-27', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 49);
INSERT INTO `attendance_attendance` VALUES (1871, '2024-12-27', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 50);
INSERT INTO `attendance_attendance` VALUES (1872, '2024-12-27', '08:55:03.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 51);
INSERT INTO `attendance_attendance` VALUES (1873, '2024-12-27', NULL, '17:45:05.000000', 'early', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 52);
INSERT INTO `attendance_attendance` VALUES (1874, '2024-12-27', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 53);
INSERT INTO `attendance_attendance` VALUES (1875, '2024-12-27', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 54);
INSERT INTO `attendance_attendance` VALUES (1876, '2024-12-27', '09:05:08.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 55);
INSERT INTO `attendance_attendance` VALUES (1877, '2024-12-27', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 56);
INSERT INTO `attendance_attendance` VALUES (1878, '2024-12-27', '08:55:01.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 57);
INSERT INTO `attendance_attendance` VALUES (1879, '2024-12-27', NULL, '17:45:03.000000', 'early', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 58);
INSERT INTO `attendance_attendance` VALUES (1880, '2024-12-27', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 59);
INSERT INTO `attendance_attendance` VALUES (1881, '2024-12-27', NULL, NULL, 'absent', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 60);
INSERT INTO `attendance_attendance` VALUES (1882, '2024-12-27', '08:55:00.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 61);
INSERT INTO `attendance_attendance` VALUES (1883, '2024-12-27', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 62);
INSERT INTO `attendance_attendance` VALUES (1884, '2024-12-27', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 63);
INSERT INTO `attendance_attendance` VALUES (1885, '2024-12-27', '09:05:08.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 64);
INSERT INTO `attendance_attendance` VALUES (1886, '2024-12-27', '08:55:01.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 65);
INSERT INTO `attendance_attendance` VALUES (1887, '2024-12-27', '08:55:08.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 66);
INSERT INTO `attendance_attendance` VALUES (1888, '2024-12-27', NULL, '17:45:02.000000', 'early', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 67);
INSERT INTO `attendance_attendance` VALUES (1889, '2024-12-27', '08:55:08.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 68);
INSERT INTO `attendance_attendance` VALUES (1890, '2024-12-27', '08:55:00.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 69);
INSERT INTO `attendance_attendance` VALUES (1891, '2024-12-27', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 70);
INSERT INTO `attendance_attendance` VALUES (1892, '2024-12-27', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 71);
INSERT INTO `attendance_attendance` VALUES (1893, '2024-12-27', NULL, '17:45:08.000000', 'early', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 72);
INSERT INTO `attendance_attendance` VALUES (1894, '2024-12-27', '08:55:02.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 73);
INSERT INTO `attendance_attendance` VALUES (1895, '2024-12-27', '09:05:28.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 74);
INSERT INTO `attendance_attendance` VALUES (1896, '2024-12-27', NULL, NULL, 'absent', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 75);
INSERT INTO `attendance_attendance` VALUES (1897, '2024-12-27', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 76);
INSERT INTO `attendance_attendance` VALUES (1898, '2024-12-27', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 77);
INSERT INTO `attendance_attendance` VALUES (1899, '2024-12-27', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 78);
INSERT INTO `attendance_attendance` VALUES (1900, '2024-12-27', '09:05:13.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 79);
INSERT INTO `attendance_attendance` VALUES (1901, '2024-12-27', '08:55:03.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 80);
INSERT INTO `attendance_attendance` VALUES (1902, '2024-12-27', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 81);
INSERT INTO `attendance_attendance` VALUES (1903, '2024-12-27', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 82);
INSERT INTO `attendance_attendance` VALUES (1904, '2024-12-27', '09:05:07.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 83);
INSERT INTO `attendance_attendance` VALUES (1905, '2024-12-27', '08:55:06.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 84);
INSERT INTO `attendance_attendance` VALUES (1906, '2024-12-27', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 85);
INSERT INTO `attendance_attendance` VALUES (1907, '2024-12-27', '08:55:07.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 86);
INSERT INTO `attendance_attendance` VALUES (1908, '2024-12-27', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 87);
INSERT INTO `attendance_attendance` VALUES (1909, '2024-12-27', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 88);
INSERT INTO `attendance_attendance` VALUES (1910, '2024-12-27', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 89);
INSERT INTO `attendance_attendance` VALUES (1911, '2024-12-27', '08:55:06.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 90);
INSERT INTO `attendance_attendance` VALUES (1912, '2024-12-27', '08:55:06.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 91);
INSERT INTO `attendance_attendance` VALUES (1913, '2024-12-27', '09:05:02.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 92);
INSERT INTO `attendance_attendance` VALUES (1914, '2024-12-27', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 93);
INSERT INTO `attendance_attendance` VALUES (1915, '2024-12-27', '08:55:08.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 94);
INSERT INTO `attendance_attendance` VALUES (1916, '2024-12-27', '09:05:19.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 95);
INSERT INTO `attendance_attendance` VALUES (1917, '2024-12-27', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 96);
INSERT INTO `attendance_attendance` VALUES (1918, '2024-12-27', '09:05:02.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 97);
INSERT INTO `attendance_attendance` VALUES (1919, '2024-12-27', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 98);
INSERT INTO `attendance_attendance` VALUES (1920, '2024-12-27', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 99);
INSERT INTO `attendance_attendance` VALUES (1921, '2024-12-27', '08:55:02.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 100);
INSERT INTO `attendance_attendance` VALUES (1922, '2024-12-30', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 5);
INSERT INTO `attendance_attendance` VALUES (1923, '2024-12-30', '09:05:27.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 6);
INSERT INTO `attendance_attendance` VALUES (1924, '2024-12-30', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 7);
INSERT INTO `attendance_attendance` VALUES (1925, '2024-12-30', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 8);
INSERT INTO `attendance_attendance` VALUES (1926, '2024-12-30', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 9);
INSERT INTO `attendance_attendance` VALUES (1927, '2024-12-30', '08:55:00.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 10);
INSERT INTO `attendance_attendance` VALUES (1928, '2024-12-30', '08:55:01.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 11);
INSERT INTO `attendance_attendance` VALUES (1929, '2024-12-30', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 12);
INSERT INTO `attendance_attendance` VALUES (1930, '2024-12-30', '08:55:07.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 13);
INSERT INTO `attendance_attendance` VALUES (1931, '2024-12-30', '08:55:00.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 14);
INSERT INTO `attendance_attendance` VALUES (1932, '2024-12-30', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 15);
INSERT INTO `attendance_attendance` VALUES (1933, '2024-12-30', '09:05:03.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 16);
INSERT INTO `attendance_attendance` VALUES (1934, '2024-12-30', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 17);
INSERT INTO `attendance_attendance` VALUES (1935, '2024-12-30', '08:55:02.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 18);
INSERT INTO `attendance_attendance` VALUES (1936, '2024-12-30', '09:05:13.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 19);
INSERT INTO `attendance_attendance` VALUES (1937, '2024-12-30', '08:55:02.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 20);
INSERT INTO `attendance_attendance` VALUES (1938, '2024-12-30', '08:55:06.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 21);
INSERT INTO `attendance_attendance` VALUES (1939, '2024-12-30', '08:55:10.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 22);
INSERT INTO `attendance_attendance` VALUES (1940, '2024-12-30', '08:55:10.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 23);
INSERT INTO `attendance_attendance` VALUES (1941, '2024-12-30', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 24);
INSERT INTO `attendance_attendance` VALUES (1942, '2024-12-30', '08:55:00.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 25);
INSERT INTO `attendance_attendance` VALUES (1943, '2024-12-30', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 26);
INSERT INTO `attendance_attendance` VALUES (1944, '2024-12-30', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 27);
INSERT INTO `attendance_attendance` VALUES (1945, '2024-12-30', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 28);
INSERT INTO `attendance_attendance` VALUES (1946, '2024-12-30', NULL, NULL, 'absent', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 29);
INSERT INTO `attendance_attendance` VALUES (1947, '2024-12-30', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 30);
INSERT INTO `attendance_attendance` VALUES (1948, '2024-12-30', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 31);
INSERT INTO `attendance_attendance` VALUES (1949, '2024-12-30', '08:55:06.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 32);
INSERT INTO `attendance_attendance` VALUES (1950, '2024-12-30', '08:55:00.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 33);
INSERT INTO `attendance_attendance` VALUES (1951, '2024-12-30', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 34);
INSERT INTO `attendance_attendance` VALUES (1952, '2024-12-30', '08:55:10.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 35);
INSERT INTO `attendance_attendance` VALUES (1953, '2024-12-30', '08:55:08.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 36);
INSERT INTO `attendance_attendance` VALUES (1954, '2024-12-30', '09:05:15.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 37);
INSERT INTO `attendance_attendance` VALUES (1955, '2024-12-30', '08:55:09.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 38);
INSERT INTO `attendance_attendance` VALUES (1956, '2024-12-30', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 39);
INSERT INTO `attendance_attendance` VALUES (1957, '2024-12-30', '08:55:06.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 40);
INSERT INTO `attendance_attendance` VALUES (1958, '2024-12-30', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 41);
INSERT INTO `attendance_attendance` VALUES (1959, '2024-12-30', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 42);
INSERT INTO `attendance_attendance` VALUES (1960, '2024-12-30', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 43);
INSERT INTO `attendance_attendance` VALUES (1961, '2024-12-30', '08:55:02.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 44);
INSERT INTO `attendance_attendance` VALUES (1962, '2024-12-30', '08:55:07.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 45);
INSERT INTO `attendance_attendance` VALUES (1963, '2024-12-30', '09:05:09.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 46);
INSERT INTO `attendance_attendance` VALUES (1964, '2024-12-30', '08:55:02.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 47);
INSERT INTO `attendance_attendance` VALUES (1965, '2024-12-30', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 48);
INSERT INTO `attendance_attendance` VALUES (1966, '2024-12-30', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 49);
INSERT INTO `attendance_attendance` VALUES (1967, '2024-12-30', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 50);
INSERT INTO `attendance_attendance` VALUES (1968, '2024-12-30', '08:55:08.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 51);
INSERT INTO `attendance_attendance` VALUES (1969, '2024-12-30', '09:05:05.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 52);
INSERT INTO `attendance_attendance` VALUES (1970, '2024-12-30', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 53);
INSERT INTO `attendance_attendance` VALUES (1971, '2024-12-30', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 54);
INSERT INTO `attendance_attendance` VALUES (1972, '2024-12-30', '08:55:07.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 55);
INSERT INTO `attendance_attendance` VALUES (1973, '2024-12-30', '08:55:05.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 56);
INSERT INTO `attendance_attendance` VALUES (1974, '2024-12-30', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 57);
INSERT INTO `attendance_attendance` VALUES (1975, '2024-12-30', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 58);
INSERT INTO `attendance_attendance` VALUES (1976, '2024-12-30', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 59);
INSERT INTO `attendance_attendance` VALUES (1977, '2024-12-30', '08:55:04.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 60);
INSERT INTO `attendance_attendance` VALUES (1978, '2024-12-30', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 61);
INSERT INTO `attendance_attendance` VALUES (1979, '2024-12-30', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 62);
INSERT INTO `attendance_attendance` VALUES (1980, '2024-12-30', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 63);
INSERT INTO `attendance_attendance` VALUES (1981, '2024-12-30', '08:55:07.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 64);
INSERT INTO `attendance_attendance` VALUES (1982, '2024-12-30', NULL, '17:45:08.000000', 'early', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 65);
INSERT INTO `attendance_attendance` VALUES (1983, '2024-12-30', NULL, NULL, 'absent', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 66);
INSERT INTO `attendance_attendance` VALUES (1984, '2024-12-30', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 67);
INSERT INTO `attendance_attendance` VALUES (1985, '2024-12-30', '08:55:07.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 68);
INSERT INTO `attendance_attendance` VALUES (1986, '2024-12-30', '08:55:03.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 69);
INSERT INTO `attendance_attendance` VALUES (1987, '2024-12-30', '08:55:00.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 70);
INSERT INTO `attendance_attendance` VALUES (1988, '2024-12-30', '08:55:05.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 71);
INSERT INTO `attendance_attendance` VALUES (1989, '2024-12-30', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 72);
INSERT INTO `attendance_attendance` VALUES (1990, '2024-12-30', '08:55:00.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 73);
INSERT INTO `attendance_attendance` VALUES (1991, '2024-12-30', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 74);
INSERT INTO `attendance_attendance` VALUES (1992, '2024-12-30', '08:55:06.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 75);
INSERT INTO `attendance_attendance` VALUES (1993, '2024-12-30', '08:55:07.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 76);
INSERT INTO `attendance_attendance` VALUES (1994, '2024-12-30', '08:55:05.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 77);
INSERT INTO `attendance_attendance` VALUES (1995, '2024-12-30', '08:55:03.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 78);
INSERT INTO `attendance_attendance` VALUES (1996, '2024-12-30', '08:55:10.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 79);
INSERT INTO `attendance_attendance` VALUES (1997, '2024-12-30', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 80);
INSERT INTO `attendance_attendance` VALUES (1998, '2024-12-30', '08:55:08.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 81);
INSERT INTO `attendance_attendance` VALUES (1999, '2024-12-30', '08:55:10.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 82);
INSERT INTO `attendance_attendance` VALUES (2000, '2024-12-30', '09:05:13.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 83);
INSERT INTO `attendance_attendance` VALUES (2001, '2024-12-30', '08:55:05.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 84);
INSERT INTO `attendance_attendance` VALUES (2002, '2024-12-30', '08:55:01.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 85);
INSERT INTO `attendance_attendance` VALUES (2003, '2024-12-30', '08:55:10.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 86);
INSERT INTO `attendance_attendance` VALUES (2004, '2024-12-30', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 87);
INSERT INTO `attendance_attendance` VALUES (2005, '2024-12-30', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 88);
INSERT INTO `attendance_attendance` VALUES (2006, '2024-12-30', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 89);
INSERT INTO `attendance_attendance` VALUES (2007, '2024-12-30', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 90);
INSERT INTO `attendance_attendance` VALUES (2008, '2024-12-30', NULL, NULL, 'absent', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 91);
INSERT INTO `attendance_attendance` VALUES (2009, '2024-12-30', '08:55:10.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 92);
INSERT INTO `attendance_attendance` VALUES (2010, '2024-12-30', '08:55:08.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 93);
INSERT INTO `attendance_attendance` VALUES (2011, '2024-12-30', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 94);
INSERT INTO `attendance_attendance` VALUES (2012, '2024-12-30', '09:05:20.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 95);
INSERT INTO `attendance_attendance` VALUES (2013, '2024-12-30', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 96);
INSERT INTO `attendance_attendance` VALUES (2014, '2024-12-30', NULL, '17:45:04.000000', 'early', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 97);
INSERT INTO `attendance_attendance` VALUES (2015, '2024-12-30', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 98);
INSERT INTO `attendance_attendance` VALUES (2016, '2024-12-30', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 99);
INSERT INTO `attendance_attendance` VALUES (2017, '2024-12-30', '08:55:10.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 100);
INSERT INTO `attendance_attendance` VALUES (2018, '2026-01-24', '21:14:04.000000', NULL, 'late', '2026-01-24 13:14:04.775791', '2026-01-24 13:14:04.782794', 100);
INSERT INTO `attendance_attendance` VALUES (2019, '2026-01-25', '00:07:06.000000', '19:34:32.000000', 'normal', '2026-01-24 16:07:06.253436', '2026-01-25 11:35:56.470055', 6);

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id` ASC, `codename` ASC) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 77 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` VALUES (13, 'Can add content type', 4, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (14, 'Can change content type', 4, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (15, 'Can delete content type', 4, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (16, 'Can view content type', 4, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (17, 'Can add session', 5, 'add_session');
INSERT INTO `auth_permission` VALUES (18, 'Can change session', 5, 'change_session');
INSERT INTO `auth_permission` VALUES (19, 'Can delete session', 5, 'delete_session');
INSERT INTO `auth_permission` VALUES (20, 'Can view session', 5, 'view_session');
INSERT INTO `auth_permission` VALUES (21, 'Can add 用户', 6, 'add_user');
INSERT INTO `auth_permission` VALUES (22, 'Can change 用户', 6, 'change_user');
INSERT INTO `auth_permission` VALUES (23, 'Can delete 用户', 6, 'delete_user');
INSERT INTO `auth_permission` VALUES (24, 'Can view 用户', 6, 'view_user');
INSERT INTO `auth_permission` VALUES (25, 'Can add 部门', 7, 'add_department');
INSERT INTO `auth_permission` VALUES (26, 'Can change 部门', 7, 'change_department');
INSERT INTO `auth_permission` VALUES (27, 'Can delete 部门', 7, 'delete_department');
INSERT INTO `auth_permission` VALUES (28, 'Can view 部门', 7, 'view_department');
INSERT INTO `auth_permission` VALUES (29, 'Can add 岗位', 8, 'add_post');
INSERT INTO `auth_permission` VALUES (30, 'Can change 岗位', 8, 'change_post');
INSERT INTO `auth_permission` VALUES (31, 'Can delete 岗位', 8, 'delete_post');
INSERT INTO `auth_permission` VALUES (32, 'Can view 岗位', 8, 'view_post');
INSERT INTO `auth_permission` VALUES (33, 'Can add 员工档案', 9, 'add_employeeprofile');
INSERT INTO `auth_permission` VALUES (34, 'Can change 员工档案', 9, 'change_employeeprofile');
INSERT INTO `auth_permission` VALUES (35, 'Can delete 员工档案', 9, 'delete_employeeprofile');
INSERT INTO `auth_permission` VALUES (36, 'Can view 员工档案', 9, 'view_employeeprofile');
INSERT INTO `auth_permission` VALUES (37, 'Can add 考勤记录', 10, 'add_attendance');
INSERT INTO `auth_permission` VALUES (38, 'Can change 考勤记录', 10, 'change_attendance');
INSERT INTO `auth_permission` VALUES (39, 'Can delete 考勤记录', 10, 'delete_attendance');
INSERT INTO `auth_permission` VALUES (40, 'Can view 考勤记录', 10, 'view_attendance');
INSERT INTO `auth_permission` VALUES (41, 'Can add 薪资记录', 11, 'add_salaryrecord');
INSERT INTO `auth_permission` VALUES (42, 'Can change 薪资记录', 11, 'change_salaryrecord');
INSERT INTO `auth_permission` VALUES (43, 'Can delete 薪资记录', 11, 'delete_salaryrecord');
INSERT INTO `auth_permission` VALUES (44, 'Can view 薪资记录', 11, 'view_salaryrecord');
INSERT INTO `auth_permission` VALUES (45, 'Can add 审批请求', 12, 'add_approvalrequest');
INSERT INTO `auth_permission` VALUES (46, 'Can change 审批请求', 12, 'change_approvalrequest');
INSERT INTO `auth_permission` VALUES (47, 'Can delete 审批请求', 12, 'delete_approvalrequest');
INSERT INTO `auth_permission` VALUES (48, 'Can view 审批请求', 12, 'view_approvalrequest');
INSERT INTO `auth_permission` VALUES (49, 'Can add 公告', 13, 'add_notice');
INSERT INTO `auth_permission` VALUES (50, 'Can change 公告', 13, 'change_notice');
INSERT INTO `auth_permission` VALUES (51, 'Can delete 公告', 13, 'delete_notice');
INSERT INTO `auth_permission` VALUES (52, 'Can view 公告', 13, 'view_notice');
INSERT INTO `auth_permission` VALUES (53, 'Can add 绩效评估', 14, 'add_performancereview');
INSERT INTO `auth_permission` VALUES (54, 'Can change 绩效评估', 14, 'change_performancereview');
INSERT INTO `auth_permission` VALUES (55, 'Can delete 绩效评估', 14, 'delete_performancereview');
INSERT INTO `auth_permission` VALUES (56, 'Can view 绩效评估', 14, 'view_performancereview');
INSERT INTO `auth_permission` VALUES (57, 'Can add 信息修改申请', 15, 'add_usereditrequest');
INSERT INTO `auth_permission` VALUES (58, 'Can change 信息修改申请', 15, 'change_usereditrequest');
INSERT INTO `auth_permission` VALUES (59, 'Can delete 信息修改申请', 15, 'delete_usereditrequest');
INSERT INTO `auth_permission` VALUES (60, 'Can view 信息修改申请', 15, 'view_usereditrequest');
INSERT INTO `auth_permission` VALUES (61, 'Can add 角色权限配置', 16, 'add_rolepermission');
INSERT INTO `auth_permission` VALUES (62, 'Can change 角色权限配置', 16, 'change_rolepermission');
INSERT INTO `auth_permission` VALUES (63, 'Can delete 角色权限配置', 16, 'delete_rolepermission');
INSERT INTO `auth_permission` VALUES (64, 'Can view 角色权限配置', 16, 'view_rolepermission');
INSERT INTO `auth_permission` VALUES (65, 'Can add 绩效模板', 17, 'add_performancetemplate');
INSERT INTO `auth_permission` VALUES (66, 'Can change 绩效模板', 17, 'change_performancetemplate');
INSERT INTO `auth_permission` VALUES (67, 'Can delete 绩效模板', 17, 'delete_performancetemplate');
INSERT INTO `auth_permission` VALUES (68, 'Can view 绩效模板', 17, 'view_performancetemplate');
INSERT INTO `auth_permission` VALUES (69, 'Can add 薪资异常', 18, 'add_salaryexception');
INSERT INTO `auth_permission` VALUES (70, 'Can change 薪资异常', 18, 'change_salaryexception');
INSERT INTO `auth_permission` VALUES (71, 'Can delete 薪资异常', 18, 'delete_salaryexception');
INSERT INTO `auth_permission` VALUES (72, 'Can view 薪资异常', 18, 'view_salaryexception');
INSERT INTO `auth_permission` VALUES (73, 'Can add 系统配置', 19, 'add_systemconfig');
INSERT INTO `auth_permission` VALUES (74, 'Can change 系统配置', 19, 'change_systemconfig');
INSERT INTO `auth_permission` VALUES (75, 'Can delete 系统配置', 19, 'delete_systemconfig');
INSERT INTO `auth_permission` VALUES (76, 'Can view 系统配置', 19, 'view_systemconfig');

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NULL DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id` ASC) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk_accounts_user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_chk_1` CHECK (`action_flag` >= 0)
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label` ASC, `model` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 20 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (16, 'accounts', 'rolepermission');
INSERT INTO `django_content_type` VALUES (19, 'accounts', 'systemconfig');
INSERT INTO `django_content_type` VALUES (6, 'accounts', 'user');
INSERT INTO `django_content_type` VALUES (15, 'accounts', 'usereditrequest');
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (12, 'approval', 'approvalrequest');
INSERT INTO `django_content_type` VALUES (10, 'attendance', 'attendance');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (9, 'employee', 'employeeprofile');
INSERT INTO `django_content_type` VALUES (13, 'notice', 'notice');
INSERT INTO `django_content_type` VALUES (7, 'organization', 'department');
INSERT INTO `django_content_type` VALUES (8, 'organization', 'post');
INSERT INTO `django_content_type` VALUES (14, 'performance', 'performancereview');
INSERT INTO `django_content_type` VALUES (17, 'performance', 'performancetemplate');
INSERT INTO `django_content_type` VALUES (18, 'salary', 'salaryexception');
INSERT INTO `django_content_type` VALUES (11, 'salary', 'salaryrecord');
INSERT INTO `django_content_type` VALUES (5, 'sessions', 'session');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 33 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2026-01-23 12:44:35.268155');
INSERT INTO `django_migrations` VALUES (2, 'contenttypes', '0002_remove_content_type_name', '2026-01-23 12:44:35.435734');
INSERT INTO `django_migrations` VALUES (3, 'auth', '0001_initial', '2026-01-23 12:44:35.806600');
INSERT INTO `django_migrations` VALUES (4, 'auth', '0002_alter_permission_name_max_length', '2026-01-23 12:44:35.884109');
INSERT INTO `django_migrations` VALUES (5, 'auth', '0003_alter_user_email_max_length', '2026-01-23 12:44:35.891127');
INSERT INTO `django_migrations` VALUES (6, 'auth', '0004_alter_user_username_opts', '2026-01-23 12:44:35.897996');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0005_alter_user_last_login_null', '2026-01-23 12:44:35.904137');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0006_require_contenttypes_0002', '2026-01-23 12:44:35.909158');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0007_alter_validators_add_error_messages', '2026-01-23 12:44:35.915658');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0008_alter_user_username_max_length', '2026-01-23 12:44:35.921584');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0009_alter_user_last_name_max_length', '2026-01-23 12:44:35.929138');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0010_alter_group_name_max_length', '2026-01-23 12:44:35.945152');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0011_update_proxy_permissions', '2026-01-23 12:44:35.952164');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0012_alter_user_first_name_max_length', '2026-01-23 12:44:35.958683');
INSERT INTO `django_migrations` VALUES (15, 'accounts', '0001_initial', '2026-01-23 12:44:36.388949');
INSERT INTO `django_migrations` VALUES (16, 'admin', '0001_initial', '2026-01-23 12:44:36.566519');
INSERT INTO `django_migrations` VALUES (17, 'admin', '0002_logentry_remove_auto_add', '2026-01-23 12:44:36.573536');
INSERT INTO `django_migrations` VALUES (18, 'admin', '0003_logentry_add_action_flag_choices', '2026-01-23 12:44:36.582753');
INSERT INTO `django_migrations` VALUES (19, 'sessions', '0001_initial', '2026-01-23 12:44:36.639479');
INSERT INTO `django_migrations` VALUES (20, 'organization', '0001_initial', '2026-01-23 13:23:52.105643');
INSERT INTO `django_migrations` VALUES (21, 'organization', '0002_post', '2026-01-23 13:45:28.718479');
INSERT INTO `django_migrations` VALUES (22, 'employee', '0001_initial', '2026-01-23 13:55:47.835588');
INSERT INTO `django_migrations` VALUES (23, 'attendance', '0001_initial', '2026-01-24 05:34:22.158104');
INSERT INTO `django_migrations` VALUES (24, 'salary', '0001_initial', '2026-01-24 06:04:33.062346');
INSERT INTO `django_migrations` VALUES (25, 'approval', '0001_initial', '2026-01-24 11:59:09.928669');
INSERT INTO `django_migrations` VALUES (26, 'notice', '0001_initial', '2026-01-24 13:45:04.857848');
INSERT INTO `django_migrations` VALUES (27, 'performance', '0001_initial', '2026-01-24 14:20:34.300802');
INSERT INTO `django_migrations` VALUES (28, 'accounts', '0002_usereditrequest', '2026-01-25 02:42:21.950777');
INSERT INTO `django_migrations` VALUES (29, 'accounts', '0003_rolepermission', '2026-01-25 06:11:02.870624');
INSERT INTO `django_migrations` VALUES (30, 'performance', '0002_performancetemplate', '2026-01-25 07:27:05.054098');
INSERT INTO `django_migrations` VALUES (31, 'salary', '0002_salaryexception', '2026-01-25 09:22:48.369943');
INSERT INTO `django_migrations` VALUES (32, 'accounts', '0004_systemconfig', '2026-01-25 09:38:06.682831');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_session
-- ----------------------------

-- ----------------------------
-- Table structure for employee_employeeprofile
-- ----------------------------
DROP TABLE IF EXISTS `employee_employeeprofile`;
CREATE TABLE `employee_employeeprofile`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `employee_no` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `hire_date` date NOT NULL,
  `salary_base` decimal(10, 2) NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `resigned_date` date NULL DEFAULT NULL,
  `resigned_reason` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `department_id` bigint NOT NULL,
  `post_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `employee_no`(`employee_no` ASC) USING BTREE,
  UNIQUE INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `employee_employeepro_department_id_b7c56aba_fk_organizat`(`department_id` ASC) USING BTREE,
  INDEX `employee_employeepro_post_id_5925dec5_fk_organizat`(`post_id` ASC) USING BTREE,
  CONSTRAINT `employee_employeepro_department_id_b7c56aba_fk_organizat` FOREIGN KEY (`department_id`) REFERENCES `organization_department` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `employee_employeepro_post_id_5925dec5_fk_organizat` FOREIGN KEY (`post_id`) REFERENCES `organization_post` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `employee_employeeprofile_user_id_d5e61f5c_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 98 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of employee_employeeprofile
-- ----------------------------
INSERT INTO `employee_employeeprofile` VALUES (1, 'EMP202401TECH001', '2024-01-10', 8000.00, 'resigned', '2026-01-24', '离职测试', '2026-01-24 16:10:19.000000', '2026-01-24 12:35:54.030147', 1, 1, 5);
INSERT INTO `employee_employeeprofile` VALUES (2, 'EMP202401TECH002', '2024-01-15', 8500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 1, 1, 6);
INSERT INTO `employee_employeeprofile` VALUES (3, 'EMP202402TECH003', '2024-02-01', 9000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 1, 2, 7);
INSERT INTO `employee_employeeprofile` VALUES (4, 'EMP202402TECH004', '2024-02-10', 9000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 1, 2, 8);
INSERT INTO `employee_employeeprofile` VALUES (5, 'EMP202402TECH005', '2024-02-20', 9500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 1, 2, 9);
INSERT INTO `employee_employeeprofile` VALUES (6, 'EMP202403TECH006', '2024-03-01', 9500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 1, 3, 10);
INSERT INTO `employee_employeeprofile` VALUES (7, 'EMP202403TECH007', '2024-03-05', 10000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 1, 3, 11);
INSERT INTO `employee_employeeprofile` VALUES (8, 'EMP202403TECH008', '2024-03-10', 10000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 1, 3, 12);
INSERT INTO `employee_employeeprofile` VALUES (9, 'EMP202403TECH009', '2024-03-15', 10500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 1, 3, 13);
INSERT INTO `employee_employeeprofile` VALUES (10, 'EMP202403TECH010', '2024-03-20', 11000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 1, 4, 14);
INSERT INTO `employee_employeeprofile` VALUES (11, 'EMP202404TECH011', '2024-04-01', 8000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 1, 1, 15);
INSERT INTO `employee_employeeprofile` VALUES (12, 'EMP202404TECH012', '2024-04-05', 8500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 1, 1, 16);
INSERT INTO `employee_employeeprofile` VALUES (13, 'EMP202404TECH013', '2024-04-10', 9000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 1, 2, 17);
INSERT INTO `employee_employeeprofile` VALUES (14, 'EMP202404TECH014', '2024-04-15', 9500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 1, 2, 18);
INSERT INTO `employee_employeeprofile` VALUES (15, 'EMP202404TECH015', '2024-04-20', 10000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 1, 2, 19);
INSERT INTO `employee_employeeprofile` VALUES (16, 'EMP202405TECH016', '2024-05-01', 10000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 1, 3, 20);
INSERT INTO `employee_employeeprofile` VALUES (17, 'EMP202405TECH017', '2024-05-05', 10500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 1, 3, 21);
INSERT INTO `employee_employeeprofile` VALUES (18, 'EMP202405TECH018', '2024-05-10', 11000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 1, 3, 22);
INSERT INTO `employee_employeeprofile` VALUES (19, 'EMP202405TECH019', '2024-05-15', 11500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 1, 3, 23);
INSERT INTO `employee_employeeprofile` VALUES (20, 'EMP202405TECH020', '2024-05-20', 12000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 1, 4, 24);
INSERT INTO `employee_employeeprofile` VALUES (21, 'EMP202401PRD021', '2024-01-20', 9000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 2, 5, 25);
INSERT INTO `employee_employeeprofile` VALUES (22, 'EMP202402PRD022', '2024-02-15', 9500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 2, 5, 26);
INSERT INTO `employee_employeeprofile` VALUES (23, 'EMP202403PRD023', '2024-03-01', 10000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 2, 5, 27);
INSERT INTO `employee_employeeprofile` VALUES (24, 'EMP202403PRD024', '2024-03-20', 10500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 2, 5, 28);
INSERT INTO `employee_employeeprofile` VALUES (25, 'EMP202404PRD025', '2024-04-01', 11000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 2, 5, 29);
INSERT INTO `employee_employeeprofile` VALUES (26, 'EMP202404PRD026', '2024-04-15', 11000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 2, 5, 30);
INSERT INTO `employee_employeeprofile` VALUES (27, 'EMP202405PRD027', '2024-05-01', 11500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 2, 5, 31);
INSERT INTO `employee_employeeprofile` VALUES (28, 'EMP202405PRD028', '2024-05-10', 11500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 2, 5, 32);
INSERT INTO `employee_employeeprofile` VALUES (29, 'EMP202405PRD029', '2024-05-20', 12000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 2, 5, 33);
INSERT INTO `employee_employeeprofile` VALUES (30, 'EMP202406PRD030', '2024-06-01', 12000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 2, 5, 34);
INSERT INTO `employee_employeeprofile` VALUES (31, 'EMP202401MKT031', '2024-01-25', 7500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 3, 1, 35);
INSERT INTO `employee_employeeprofile` VALUES (32, 'EMP202402MKT032', '2024-02-20', 8000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 3, 1, 36);
INSERT INTO `employee_employeeprofile` VALUES (33, 'EMP202403MKT033', '2024-03-10', 8500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 3, 2, 37);
INSERT INTO `employee_employeeprofile` VALUES (34, 'EMP202403MKT034', '2024-03-25', 9000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 3, 2, 38);
INSERT INTO `employee_employeeprofile` VALUES (35, 'EMP202404MKT035', '2024-04-05', 9500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 3, 2, 39);
INSERT INTO `employee_employeeprofile` VALUES (36, 'EMP202404MKT036', '2024-04-20', 10000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 3, 2, 40);
INSERT INTO `employee_employeeprofile` VALUES (37, 'EMP202405MKT037', '2024-05-05', 10000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 3, 3, 41);
INSERT INTO `employee_employeeprofile` VALUES (38, 'EMP202405MKT038', '2024-05-15', 10500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 3, 3, 42);
INSERT INTO `employee_employeeprofile` VALUES (39, 'EMP202406MKT039', '2024-06-01', 11000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 3, 3, 43);
INSERT INTO `employee_employeeprofile` VALUES (40, 'EMP202406MKT040', '2024-06-10', 11000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 3, 3, 44);
INSERT INTO `employee_employeeprofile` VALUES (41, 'EMP202402HR041', '2024-02-01', 7000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 4, 7, 45);
INSERT INTO `employee_employeeprofile` VALUES (42, 'EMP202403HR042', '2024-03-01', 7500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 4, 7, 46);
INSERT INTO `employee_employeeprofile` VALUES (43, 'EMP202404HR043', '2024-04-01', 8000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 4, 7, 47);
INSERT INTO `employee_employeeprofile` VALUES (44, 'EMP202405HR044', '2024-05-01', 8500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 4, 7, 48);
INSERT INTO `employee_employeeprofile` VALUES (45, 'EMP202406HR045', '2024-06-01', 9000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 4, 7, 49);
INSERT INTO `employee_employeeprofile` VALUES (46, 'EMP202401FIN046', '2024-01-10', 7500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 5, 8, 50);
INSERT INTO `employee_employeeprofile` VALUES (47, 'EMP202402FIN047', '2024-02-15', 8000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 5, 8, 51);
INSERT INTO `employee_employeeprofile` VALUES (48, 'EMP202403FIN048', '2024-03-01', 8500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 5, 8, 52);
INSERT INTO `employee_employeeprofile` VALUES (49, 'EMP202403FIN049', '2024-03-20', 8500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 5, 8, 53);
INSERT INTO `employee_employeeprofile` VALUES (50, 'EMP202404FIN050', '2024-04-05', 9000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 5, 8, 54);
INSERT INTO `employee_employeeprofile` VALUES (51, 'EMP202404FIN051', '2024-04-20', 9000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 5, 8, 55);
INSERT INTO `employee_employeeprofile` VALUES (52, 'EMP202405FIN052', '2024-05-05', 9500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 5, 8, 56);
INSERT INTO `employee_employeeprofile` VALUES (53, 'EMP202405FIN053', '2024-05-20', 10000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 5, 8, 57);
INSERT INTO `employee_employeeprofile` VALUES (54, 'EMP202401OPS054', '2024-01-20', 6500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 6, 9, 58);
INSERT INTO `employee_employeeprofile` VALUES (55, 'EMP202402OPS055', '2024-02-10', 7000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 6, 9, 59);
INSERT INTO `employee_employeeprofile` VALUES (56, 'EMP202402OPS056', '2024-02-28', 7500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 6, 9, 60);
INSERT INTO `employee_employeeprofile` VALUES (57, 'EMP202403OPS057', '2024-03-15', 7500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 6, 9, 61);
INSERT INTO `employee_employeeprofile` VALUES (58, 'EMP202404OPS058', '2024-04-01', 8000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 6, 9, 62);
INSERT INTO `employee_employeeprofile` VALUES (59, 'EMP202404OPS059', '2024-04-15', 8000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 6, 9, 63);
INSERT INTO `employee_employeeprofile` VALUES (60, 'EMP202404OPS060', '2024-04-30', 8500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 6, 9, 64);
INSERT INTO `employee_employeeprofile` VALUES (61, 'EMP202405OPS061', '2024-05-10', 8500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 6, 9, 65);
INSERT INTO `employee_employeeprofile` VALUES (62, 'EMP202405OPS062', '2024-05-25', 9000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 6, 9, 66);
INSERT INTO `employee_employeeprofile` VALUES (63, 'EMP202406OPS063', '2024-06-05', 9000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 6, 9, 67);
INSERT INTO `employee_employeeprofile` VALUES (64, 'EMP202402DES064', '2024-02-01', 8500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 7, 6, 68);
INSERT INTO `employee_employeeprofile` VALUES (65, 'EMP202402DES065', '2024-02-20', 9000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 7, 6, 69);
INSERT INTO `employee_employeeprofile` VALUES (66, 'EMP202403DES066', '2024-03-10', 9500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 7, 6, 70);
INSERT INTO `employee_employeeprofile` VALUES (67, 'EMP202403DES067', '2024-03-25', 10000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 7, 6, 71);
INSERT INTO `employee_employeeprofile` VALUES (68, 'EMP202404DES068', '2024-04-10', 10000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 7, 6, 72);
INSERT INTO `employee_employeeprofile` VALUES (69, 'EMP202404DES069', '2024-04-25', 10500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 7, 6, 73);
INSERT INTO `employee_employeeprofile` VALUES (70, 'EMP202405DES070', '2024-05-05', 10500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 7, 6, 74);
INSERT INTO `employee_employeeprofile` VALUES (71, 'EMP202405DES071', '2024-05-20', 11000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 7, 6, 75);
INSERT INTO `employee_employeeprofile` VALUES (72, 'EMP202401CS072', '2024-01-15', 5500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 8, 10, 76);
INSERT INTO `employee_employeeprofile` VALUES (73, 'EMP202402CS073', '2024-02-01', 6000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 8, 10, 77);
INSERT INTO `employee_employeeprofile` VALUES (74, 'EMP202402CS074', '2024-02-20', 6500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 8, 10, 78);
INSERT INTO `employee_employeeprofile` VALUES (75, 'EMP202403CS075', '2024-03-10', 6500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 8, 10, 79);
INSERT INTO `employee_employeeprofile` VALUES (76, 'EMP202403CS076', '2024-03-25', 7000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 8, 10, 80);
INSERT INTO `employee_employeeprofile` VALUES (77, 'EMP202404CS077', '2024-04-05', 7000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 8, 10, 81);
INSERT INTO `employee_employeeprofile` VALUES (78, 'EMP202404CS078', '2024-04-20', 7500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 8, 10, 82);
INSERT INTO `employee_employeeprofile` VALUES (79, 'EMP202405CS079', '2024-05-05', 7500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 8, 10, 83);
INSERT INTO `employee_employeeprofile` VALUES (80, 'EMP202401ADM080', '2024-01-20', 6000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 9, 1, 84);
INSERT INTO `employee_employeeprofile` VALUES (81, 'EMP202402ADM081', '2024-02-15', 6500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 9, 1, 85);
INSERT INTO `employee_employeeprofile` VALUES (82, 'EMP202403ADM082', '2024-03-01', 7000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 9, 1, 86);
INSERT INTO `employee_employeeprofile` VALUES (83, 'EMP202403ADM083', '2024-03-20', 7000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 9, 1, 87);
INSERT INTO `employee_employeeprofile` VALUES (84, 'EMP202404ADM084', '2024-04-10', 7500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 9, 1, 88);
INSERT INTO `employee_employeeprofile` VALUES (85, 'EMP202402LEG085', '2024-02-01', 10000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 10, 1, 89);
INSERT INTO `employee_employeeprofile` VALUES (86, 'EMP202403LEG086', '2024-03-01', 11000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 10, 1, 90);
INSERT INTO `employee_employeeprofile` VALUES (87, 'EMP202406TECH087', '2024-06-01', 9000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 1, 2, 91);
INSERT INTO `employee_employeeprofile` VALUES (88, 'EMP202406PRD088', '2024-06-05', 10000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 2, 5, 92);
INSERT INTO `employee_employeeprofile` VALUES (89, 'EMP202406MKT089', '2024-06-10', 8500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 3, 1, 93);
INSERT INTO `employee_employeeprofile` VALUES (90, 'EMP202406OPS090', '2024-06-15', 7500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 6, 9, 94);
INSERT INTO `employee_employeeprofile` VALUES (91, 'EMP202406FIN091', '2024-06-20', 8500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 5, 8, 95);
INSERT INTO `employee_employeeprofile` VALUES (92, 'EMP202406CS092', '2024-06-25', 6500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 8, 10, 96);
INSERT INTO `employee_employeeprofile` VALUES (93, 'EMP202406DES093', '2024-06-28', 9500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 7, 6, 97);
INSERT INTO `employee_employeeprofile` VALUES (94, 'EMP202406HR094', '2024-06-30', 7500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 4, 7, 98);
INSERT INTO `employee_employeeprofile` VALUES (95, 'EMP202407ADM095', '2024-07-01', 6500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 9, 1, 99);
INSERT INTO `employee_employeeprofile` VALUES (96, 'EMP202407LEG096', '2024-07-05', 10000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 10, 1, 100);

-- ----------------------------
-- Table structure for notice_notice
-- ----------------------------
DROP TABLE IF EXISTS `notice_notice`;
CREATE TABLE `notice_notice`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_pinned` tinyint(1) NOT NULL,
  `is_published` tinyint(1) NOT NULL,
  `published_at` datetime(6) NULL DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `published_by_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `notice_notice_published_by_id_f5dd3c7f_fk_accounts_user_id`(`published_by_id` ASC) USING BTREE,
  CONSTRAINT `notice_notice_published_by_id_f5dd3c7f_fk_accounts_user_id` FOREIGN KEY (`published_by_id`) REFERENCES `accounts_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of notice_notice
-- ----------------------------
INSERT INTO `notice_notice` VALUES (1, '测试公告', '123213', 1, 1, '2026-01-24 13:59:07.065629', '2026-01-24 13:58:57.875888', '2026-01-24 14:07:28.461323', 1);

-- ----------------------------
-- Table structure for organization_department
-- ----------------------------
DROP TABLE IF EXISTS `organization_department`;
CREATE TABLE `organization_department`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `code` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `sort_order` int NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `parent_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `code`(`code` ASC) USING BTREE,
  INDEX `organization_departm_parent_id_26506ab2_fk_organizat`(`parent_id` ASC) USING BTREE,
  CONSTRAINT `organization_departm_parent_id_26506ab2_fk_organizat` FOREIGN KEY (`parent_id`) REFERENCES `organization_department` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of organization_department
-- ----------------------------
INSERT INTO `organization_department` VALUES (1, '技术研发部', 'TECH', 1, 1, '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', NULL);
INSERT INTO `organization_department` VALUES (2, '产品部', 'PRD', 2, 1, '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', NULL);
INSERT INTO `organization_department` VALUES (3, '市场部', 'MKT', 3, 1, '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', NULL);
INSERT INTO `organization_department` VALUES (4, '人力资源部', 'HR', 4, 1, '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', NULL);
INSERT INTO `organization_department` VALUES (5, '财务部', 'FIN', 5, 1, '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', NULL);
INSERT INTO `organization_department` VALUES (6, '运营部', 'OPS', 6, 1, '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', NULL);
INSERT INTO `organization_department` VALUES (7, '设计部', 'DES', 7, 1, '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', NULL);
INSERT INTO `organization_department` VALUES (8, '客服部', 'CS', 8, 1, '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', NULL);
INSERT INTO `organization_department` VALUES (9, '行政部', 'ADM', 9, 1, '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', NULL);
INSERT INTO `organization_department` VALUES (10, '法务部', 'LEG', 10, 1, '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', NULL);

-- ----------------------------
-- Table structure for organization_post
-- ----------------------------
DROP TABLE IF EXISTS `organization_post`;
CREATE TABLE `organization_post`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `code` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `sort_order` int NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `code`(`code` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of organization_post
-- ----------------------------
INSERT INTO `organization_post` VALUES (1, '初级开发工程师', 'JDEV', '负责基础开发工作，使用公司技术栈完成功能开发', 1, 1, '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000');
INSERT INTO `organization_post` VALUES (2, '中级开发工程师', 'MDEV', '承担核心模块开发，指导初级工程师', 2, 1, '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000');
INSERT INTO `organization_post` VALUES (3, '高级开发工程师', 'SDEV', '负责技术架构设计，攻克技术难题', 3, 1, '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000');
INSERT INTO `organization_post` VALUES (4, '技术总监', 'TD', '技术团队管理，技术战略规划', 4, 1, '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000');
INSERT INTO `organization_post` VALUES (5, '产品经理', 'PM', '产品规划，需求分析，项目管理', 5, 1, '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000');
INSERT INTO `organization_post` VALUES (6, 'UI/UX设计师', 'UI', '界面设计，用户体验优化', 6, 1, '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000');
INSERT INTO `organization_post` VALUES (7, '人事专员', 'HRSP', '招聘，员工关系，薪酬福利', 7, 1, '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000');
INSERT INTO `organization_post` VALUES (8, '财务专员', 'FASP', '账务处理，财务报表，税务申报', 8, 1, '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000');
INSERT INTO `organization_post` VALUES (9, '运营专员', 'OPSP', '日常运营，数据分析，活动策划', 9, 1, '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000');
INSERT INTO `organization_post` VALUES (10, '客户成功经理', 'CSM', '客户服务，客户满意度维护', 10, 1, '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000');

-- ----------------------------
-- Table structure for performance_performancereview
-- ----------------------------
DROP TABLE IF EXISTS `performance_performancereview`;
CREATE TABLE `performance_performancereview`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `review_period` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `score` decimal(2, 1) NULL DEFAULT NULL,
  `strengths` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `improvements` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `goals` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `employee_id` bigint NOT NULL,
  `reviewer_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `performance_performancer_employee_id_review_perio_3c6a206c_uniq`(`employee_id` ASC, `review_period` ASC) USING BTREE,
  INDEX `performance_performa_reviewer_id_fa353eac_fk_accounts_`(`reviewer_id` ASC) USING BTREE,
  CONSTRAINT `performance_performa_employee_id_3c08abd5_fk_accounts_` FOREIGN KEY (`employee_id`) REFERENCES `accounts_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `performance_performa_reviewer_id_fa353eac_fk_accounts_` FOREIGN KEY (`reviewer_id`) REFERENCES `accounts_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of performance_performancereview
-- ----------------------------
INSERT INTO `performance_performancereview` VALUES (1, '2025-Q1', 5.0, '好', '好', '好', 'draft', '2026-01-24 15:32:48.447836', '2026-01-24 15:32:48.447836', 2, 1);
INSERT INTO `performance_performancereview` VALUES (2, '2025-Q1', 5.0, '优秀', '优秀', '优秀', 'draft', '2026-01-24 15:40:22.393695', '2026-01-24 15:40:22.393695', 3, 1);
INSERT INTO `performance_performancereview` VALUES (3, '2025-Q3', 5.0, '优秀', '优秀', '优秀', 'draft', '2026-01-24 15:41:22.623888', '2026-01-24 15:41:22.623888', 2, 1);
INSERT INTO `performance_performancereview` VALUES (4, '2025-01', 5.0, '优秀', '优秀', '优秀', 'draft', '2026-01-24 15:41:58.331549', '2026-01-24 15:41:58.331549', 2, 1);
INSERT INTO `performance_performancereview` VALUES (5, '2025-Q1', 5.0, '优秀', '优秀', '优秀', 'published', '2026-01-24 15:51:36.824303', '2026-01-24 16:00:14.381128', 6, 1);

-- ----------------------------
-- Table structure for performance_performancetemplate
-- ----------------------------
DROP TABLE IF EXISTS `performance_performancetemplate`;
CREATE TABLE `performance_performancetemplate`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `items` json NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of performance_performancetemplate
-- ----------------------------

-- ----------------------------
-- Table structure for salary_exception
-- ----------------------------
DROP TABLE IF EXISTS `salary_exception`;
CREATE TABLE `salary_exception`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `exception_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `resolution` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `adjustment_amount` decimal(10, 2) NOT NULL,
  `resolved_at` datetime(6) NULL DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `assigned_to_id` bigint NULL DEFAULT NULL,
  `reported_by_id` bigint NULL DEFAULT NULL,
  `salary_record_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `salary_exception_assigned_to_id_b493e5eb_fk_accounts_user_id`(`assigned_to_id` ASC) USING BTREE,
  INDEX `salary_exception_reported_by_id_3e6df770_fk_accounts_user_id`(`reported_by_id` ASC) USING BTREE,
  INDEX `salary_exception_salary_record_id_5c158ee5_fk_salary_sa`(`salary_record_id` ASC) USING BTREE,
  CONSTRAINT `salary_exception_assigned_to_id_b493e5eb_fk_accounts_user_id` FOREIGN KEY (`assigned_to_id`) REFERENCES `accounts_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `salary_exception_reported_by_id_3e6df770_fk_accounts_user_id` FOREIGN KEY (`reported_by_id`) REFERENCES `accounts_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `salary_exception_salary_record_id_5c158ee5_fk_salary_sa` FOREIGN KEY (`salary_record_id`) REFERENCES `salary_salaryrecord` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of salary_exception
-- ----------------------------
INSERT INTO `salary_exception` VALUES (1, 'salary_error', 'ces', 'resolved', '测试', 400.00, '2026-01-25 09:25:37.331122', '2026-01-25 09:25:13.323380', '2026-01-25 09:25:37.331122', 1, 1, 286);

-- ----------------------------
-- Table structure for salary_salaryrecord
-- ----------------------------
DROP TABLE IF EXISTS `salary_salaryrecord`;
CREATE TABLE `salary_salaryrecord`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `month` varchar(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `base_salary` decimal(10, 2) NOT NULL,
  `overtime_hours` decimal(6, 1) NOT NULL,
  `overtime_pay` decimal(10, 2) NOT NULL,
  `late_count` int NOT NULL,
  `early_count` int NOT NULL,
  `attendance_deduction` decimal(10, 2) NOT NULL,
  `final_salary` decimal(10, 2) NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `salary_salaryrecord_user_id_month_dc1c8ea1_uniq`(`user_id` ASC, `month` ASC) USING BTREE,
  CONSTRAINT `salary_salaryrecord_user_id_0c9b30a7_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 289 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of salary_salaryrecord
-- ----------------------------
INSERT INTO `salary_salaryrecord` VALUES (1, '2024-11', 8000.00, 8.6, 390.91, 4, 1, 250.00, 8140.91, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 5);
INSERT INTO `salary_salaryrecord` VALUES (2, '2024-11', 8500.00, 9.8, 473.30, 4, 1, 250.00, 8723.30, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 6);
INSERT INTO `salary_salaryrecord` VALUES (3, '2024-11', 9000.00, 19.2, 981.82, 0, 0, 0.00, 9981.82, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 7);
INSERT INTO `salary_salaryrecord` VALUES (4, '2024-11', 9000.00, 7.8, 398.86, 1, 0, 50.00, 9348.86, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 8);
INSERT INTO `salary_salaryrecord` VALUES (5, '2024-11', 9500.00, 18.8, 1014.77, 2, 1, 150.00, 10364.77, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 9);
INSERT INTO `salary_salaryrecord` VALUES (6, '2024-11', 9500.00, 11.4, 615.34, 3, 0, 150.00, 9965.34, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 10);
INSERT INTO `salary_salaryrecord` VALUES (7, '2024-11', 10000.00, 13.3, 755.68, 0, 0, 0.00, 10755.68, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 11);
INSERT INTO `salary_salaryrecord` VALUES (8, '2024-11', 10000.00, 1.4, 79.55, 4, 2, 300.00, 9779.55, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 12);
INSERT INTO `salary_salaryrecord` VALUES (9, '2024-11', 10500.00, 0.2, 11.93, 2, 2, 200.00, 10311.93, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 13);
INSERT INTO `salary_salaryrecord` VALUES (10, '2024-11', 11000.00, 15.9, 993.75, 2, 1, 150.00, 11843.75, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 14);
INSERT INTO `salary_salaryrecord` VALUES (11, '2024-11', 8000.00, 15.5, 704.55, 2, 1, 150.00, 8554.55, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 15);
INSERT INTO `salary_salaryrecord` VALUES (12, '2024-11', 8500.00, 14.2, 685.80, 0, 2, 100.00, 9085.80, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 16);
INSERT INTO `salary_salaryrecord` VALUES (13, '2024-11', 9000.00, 6.9, 352.84, 2, 1, 150.00, 9202.84, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 17);
INSERT INTO `salary_salaryrecord` VALUES (14, '2024-11', 9500.00, 10.1, 545.17, 0, 0, 0.00, 10045.17, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 18);
INSERT INTO `salary_salaryrecord` VALUES (15, '2024-11', 10000.00, 1.4, 79.55, 2, 0, 100.00, 9979.55, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 19);
INSERT INTO `salary_salaryrecord` VALUES (16, '2024-11', 10000.00, 14.4, 818.18, 3, 0, 150.00, 10668.18, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 20);
INSERT INTO `salary_salaryrecord` VALUES (17, '2024-11', 10500.00, 5.9, 351.99, 3, 0, 150.00, 10701.99, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 21);
INSERT INTO `salary_salaryrecord` VALUES (18, '2024-11', 11000.00, 18.3, 1143.75, 2, 0, 100.00, 12043.75, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 22);
INSERT INTO `salary_salaryrecord` VALUES (19, '2024-11', 11500.00, 6.6, 431.25, 0, 1, 50.00, 11881.25, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 23);
INSERT INTO `salary_salaryrecord` VALUES (20, '2024-11', 12000.00, 0.8, 54.55, 4, 0, 200.00, 11854.55, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 24);
INSERT INTO `salary_salaryrecord` VALUES (21, '2024-11', 9000.00, 9.4, 480.68, 2, 0, 100.00, 9380.68, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 25);
INSERT INTO `salary_salaryrecord` VALUES (22, '2024-11', 9500.00, 12.5, 674.72, 4, 1, 250.00, 9924.72, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 26);
INSERT INTO `salary_salaryrecord` VALUES (23, '2024-11', 10000.00, 10.3, 585.23, 4, 2, 300.00, 10285.23, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 27);
INSERT INTO `salary_salaryrecord` VALUES (24, '2024-11', 10500.00, 9.4, 560.80, 4, 2, 300.00, 10760.80, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 28);
INSERT INTO `salary_salaryrecord` VALUES (25, '2024-11', 11000.00, 5.7, 356.25, 0, 1, 50.00, 11306.25, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 29);
INSERT INTO `salary_salaryrecord` VALUES (26, '2024-11', 11000.00, 17.9, 1118.75, 1, 1, 100.00, 12018.75, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 30);
INSERT INTO `salary_salaryrecord` VALUES (27, '2024-11', 11500.00, 2.6, 169.89, 4, 1, 250.00, 11419.89, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 31);
INSERT INTO `salary_salaryrecord` VALUES (28, '2024-11', 11500.00, 1.7, 111.08, 0, 2, 100.00, 11511.08, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 32);
INSERT INTO `salary_salaryrecord` VALUES (29, '2024-11', 12000.00, 6.0, 409.09, 3, 1, 200.00, 12209.09, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 33);
INSERT INTO `salary_salaryrecord` VALUES (30, '2024-11', 12000.00, 10.0, 681.82, 3, 1, 200.00, 12481.82, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 34);
INSERT INTO `salary_salaryrecord` VALUES (31, '2024-11', 7500.00, 10.1, 430.40, 3, 2, 250.00, 7680.40, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 35);
INSERT INTO `salary_salaryrecord` VALUES (32, '2024-11', 8000.00, 16.4, 745.45, 2, 1, 150.00, 8595.45, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 36);
INSERT INTO `salary_salaryrecord` VALUES (33, '2024-11', 8500.00, 18.3, 883.81, 4, 2, 300.00, 9083.81, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 37);
INSERT INTO `salary_salaryrecord` VALUES (34, '2024-11', 9000.00, 6.1, 311.93, 0, 1, 50.00, 9261.93, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 38);
INSERT INTO `salary_salaryrecord` VALUES (35, '2024-11', 9500.00, 16.8, 906.82, 1, 1, 100.00, 10306.82, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 39);
INSERT INTO `salary_salaryrecord` VALUES (36, '2024-11', 10000.00, 4.2, 238.64, 1, 0, 50.00, 10188.64, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 40);
INSERT INTO `salary_salaryrecord` VALUES (37, '2024-11', 10000.00, 6.8, 386.36, 1, 1, 100.00, 10286.36, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 41);
INSERT INTO `salary_salaryrecord` VALUES (38, '2024-11', 10500.00, 8.0, 477.27, 1, 0, 50.00, 10927.27, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 42);
INSERT INTO `salary_salaryrecord` VALUES (39, '2024-11', 11000.00, 10.3, 643.75, 2, 0, 100.00, 11543.75, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 43);
INSERT INTO `salary_salaryrecord` VALUES (40, '2024-11', 11000.00, 5.8, 362.50, 4, 2, 300.00, 11062.50, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 44);
INSERT INTO `salary_salaryrecord` VALUES (41, '2024-11', 7000.00, 18.8, 747.73, 1, 1, 100.00, 7647.73, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 45);
INSERT INTO `salary_salaryrecord` VALUES (42, '2024-11', 7500.00, 5.3, 225.85, 3, 2, 250.00, 7475.85, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 46);
INSERT INTO `salary_salaryrecord` VALUES (43, '2024-11', 8000.00, 13.1, 595.45, 2, 1, 150.00, 8445.45, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 47);
INSERT INTO `salary_salaryrecord` VALUES (44, '2024-11', 8500.00, 3.0, 144.89, 1, 1, 100.00, 8544.89, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 48);
INSERT INTO `salary_salaryrecord` VALUES (45, '2024-11', 9000.00, 19.6, 1002.27, 0, 0, 0.00, 10002.27, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 49);
INSERT INTO `salary_salaryrecord` VALUES (46, '2024-11', 7500.00, 11.1, 473.01, 1, 2, 150.00, 7823.01, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 50);
INSERT INTO `salary_salaryrecord` VALUES (47, '2024-11', 8000.00, 18.1, 822.73, 1, 2, 150.00, 8672.73, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 51);
INSERT INTO `salary_salaryrecord` VALUES (48, '2024-11', 8500.00, 1.2, 57.95, 3, 1, 200.00, 8357.95, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 52);
INSERT INTO `salary_salaryrecord` VALUES (49, '2024-11', 8500.00, 9.8, 473.30, 1, 0, 50.00, 8923.30, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 53);
INSERT INTO `salary_salaryrecord` VALUES (50, '2024-11', 9000.00, 17.0, 869.32, 3, 2, 250.00, 9619.32, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 54);
INSERT INTO `salary_salaryrecord` VALUES (51, '2024-11', 9000.00, 0.6, 30.68, 3, 2, 250.00, 8780.68, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 55);
INSERT INTO `salary_salaryrecord` VALUES (52, '2024-11', 9500.00, 0.1, 5.40, 3, 1, 200.00, 9305.40, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 56);
INSERT INTO `salary_salaryrecord` VALUES (53, '2024-11', 10000.00, 12.3, 698.86, 4, 1, 250.00, 10448.86, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 57);
INSERT INTO `salary_salaryrecord` VALUES (54, '2024-11', 6500.00, 5.4, 199.43, 3, 0, 150.00, 6549.43, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 58);
INSERT INTO `salary_salaryrecord` VALUES (55, '2024-11', 7000.00, 18.9, 751.70, 1, 2, 150.00, 7601.70, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 59);
INSERT INTO `salary_salaryrecord` VALUES (56, '2024-11', 7500.00, 3.0, 127.84, 0, 2, 100.00, 7527.84, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 60);
INSERT INTO `salary_salaryrecord` VALUES (57, '2024-11', 7500.00, 12.0, 511.36, 1, 1, 100.00, 7911.36, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 61);
INSERT INTO `salary_salaryrecord` VALUES (58, '2024-11', 8000.00, 7.9, 359.09, 0, 2, 100.00, 8259.09, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 62);
INSERT INTO `salary_salaryrecord` VALUES (59, '2024-11', 8000.00, 11.4, 518.18, 0, 0, 0.00, 8518.18, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 63);
INSERT INTO `salary_salaryrecord` VALUES (60, '2024-11', 8500.00, 13.0, 627.84, 2, 0, 100.00, 9027.84, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 64);
INSERT INTO `salary_salaryrecord` VALUES (61, '2024-11', 8500.00, 5.8, 280.11, 3, 1, 200.00, 8580.11, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 65);
INSERT INTO `salary_salaryrecord` VALUES (62, '2024-11', 9000.00, 12.6, 644.32, 4, 1, 250.00, 9394.32, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 66);
INSERT INTO `salary_salaryrecord` VALUES (63, '2024-11', 9000.00, 7.8, 398.86, 1, 0, 50.00, 9348.86, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 67);
INSERT INTO `salary_salaryrecord` VALUES (64, '2024-11', 8500.00, 12.9, 623.01, 0, 2, 100.00, 9023.01, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 68);
INSERT INTO `salary_salaryrecord` VALUES (65, '2024-11', 9000.00, 7.0, 357.95, 4, 2, 300.00, 9057.95, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 69);
INSERT INTO `salary_salaryrecord` VALUES (66, '2024-11', 9500.00, 8.4, 453.41, 3, 0, 150.00, 9803.41, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 70);
INSERT INTO `salary_salaryrecord` VALUES (67, '2024-11', 10000.00, 4.0, 227.27, 0, 2, 100.00, 10127.27, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 71);
INSERT INTO `salary_salaryrecord` VALUES (68, '2024-11', 10000.00, 17.4, 988.64, 1, 0, 50.00, 10938.64, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 72);
INSERT INTO `salary_salaryrecord` VALUES (69, '2024-11', 10500.00, 3.3, 196.87, 3, 2, 250.00, 10446.87, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 73);
INSERT INTO `salary_salaryrecord` VALUES (70, '2024-11', 10500.00, 18.5, 1103.69, 4, 0, 200.00, 11403.69, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 74);
INSERT INTO `salary_salaryrecord` VALUES (71, '2024-11', 11000.00, 9.3, 581.25, 3, 1, 200.00, 11381.25, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 75);
INSERT INTO `salary_salaryrecord` VALUES (72, '2024-11', 5500.00, 3.5, 109.38, 3, 1, 200.00, 5409.38, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 76);
INSERT INTO `salary_salaryrecord` VALUES (73, '2024-11', 6000.00, 2.7, 92.05, 4, 1, 250.00, 5842.05, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 77);
INSERT INTO `salary_salaryrecord` VALUES (74, '2024-11', 6500.00, 5.9, 217.90, 2, 1, 150.00, 6567.90, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 78);
INSERT INTO `salary_salaryrecord` VALUES (75, '2024-11', 6500.00, 10.0, 369.32, 4, 2, 300.00, 6569.32, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 79);
INSERT INTO `salary_salaryrecord` VALUES (76, '2024-11', 7000.00, 8.5, 338.07, 2, 2, 200.00, 7138.07, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 80);
INSERT INTO `salary_salaryrecord` VALUES (77, '2024-11', 7000.00, 0.7, 27.84, 1, 2, 150.00, 6877.84, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 81);
INSERT INTO `salary_salaryrecord` VALUES (78, '2024-11', 7500.00, 19.2, 818.18, 2, 2, 200.00, 8118.18, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 82);
INSERT INTO `salary_salaryrecord` VALUES (79, '2024-11', 7500.00, 16.4, 698.86, 3, 2, 250.00, 7948.86, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 83);
INSERT INTO `salary_salaryrecord` VALUES (80, '2024-11', 6000.00, 11.3, 385.23, 0, 0, 0.00, 6385.23, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 84);
INSERT INTO `salary_salaryrecord` VALUES (81, '2024-11', 6500.00, 0.0, 0.00, 2, 0, 100.00, 6400.00, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 85);
INSERT INTO `salary_salaryrecord` VALUES (82, '2024-11', 7000.00, 14.1, 560.80, 4, 1, 250.00, 7310.80, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 86);
INSERT INTO `salary_salaryrecord` VALUES (83, '2024-11', 7000.00, 10.4, 413.64, 2, 2, 200.00, 7213.64, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 87);
INSERT INTO `salary_salaryrecord` VALUES (84, '2024-11', 7500.00, 10.4, 443.18, 1, 1, 100.00, 7843.18, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 88);
INSERT INTO `salary_salaryrecord` VALUES (85, '2024-11', 10000.00, 2.3, 130.68, 1, 1, 100.00, 10030.68, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 89);
INSERT INTO `salary_salaryrecord` VALUES (86, '2024-11', 11000.00, 12.1, 756.25, 0, 1, 50.00, 11706.25, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 90);
INSERT INTO `salary_salaryrecord` VALUES (87, '2024-11', 9000.00, 0.0, 0.00, 4, 0, 200.00, 8800.00, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 91);
INSERT INTO `salary_salaryrecord` VALUES (88, '2024-11', 10000.00, 9.5, 539.77, 1, 2, 150.00, 10389.77, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 92);
INSERT INTO `salary_salaryrecord` VALUES (89, '2024-11', 8500.00, 0.6, 28.98, 4, 2, 300.00, 8228.98, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 93);
INSERT INTO `salary_salaryrecord` VALUES (90, '2024-11', 7500.00, 14.8, 630.68, 3, 2, 250.00, 7880.68, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 94);
INSERT INTO `salary_salaryrecord` VALUES (91, '2024-11', 8500.00, 14.4, 695.45, 2, 1, 150.00, 9045.45, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 95);
INSERT INTO `salary_salaryrecord` VALUES (92, '2024-11', 6500.00, 4.7, 173.58, 0, 1, 50.00, 6623.58, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 96);
INSERT INTO `salary_salaryrecord` VALUES (93, '2024-11', 9500.00, 17.4, 939.20, 4, 0, 200.00, 10239.20, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 97);
INSERT INTO `salary_salaryrecord` VALUES (94, '2024-11', 7500.00, 9.0, 383.52, 1, 2, 150.00, 7733.52, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 98);
INSERT INTO `salary_salaryrecord` VALUES (95, '2024-11', 6500.00, 12.5, 461.65, 3, 2, 250.00, 6711.65, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 99);
INSERT INTO `salary_salaryrecord` VALUES (96, '2024-11', 10000.00, 6.9, 392.05, 3, 1, 200.00, 10192.05, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 100);
INSERT INTO `salary_salaryrecord` VALUES (97, '2024-12', 8000.00, 7.0, 318.18, 4, 2, 300.00, 8018.18, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 5);
INSERT INTO `salary_salaryrecord` VALUES (98, '2024-12', 8500.00, 11.0, 531.25, 2, 2, 200.00, 8831.25, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 6);
INSERT INTO `salary_salaryrecord` VALUES (99, '2024-12', 9000.00, 16.4, 838.64, 3, 0, 150.00, 9688.64, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 7);
INSERT INTO `salary_salaryrecord` VALUES (100, '2024-12', 9000.00, 2.4, 122.73, 1, 1, 100.00, 9022.73, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 8);
INSERT INTO `salary_salaryrecord` VALUES (101, '2024-12', 9500.00, 19.5, 1052.56, 3, 0, 150.00, 10402.56, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 9);
INSERT INTO `salary_salaryrecord` VALUES (102, '2024-12', 9500.00, 0.8, 43.18, 2, 0, 100.00, 9443.18, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 10);
INSERT INTO `salary_salaryrecord` VALUES (103, '2024-12', 10000.00, 17.7, 1005.68, 0, 2, 100.00, 10905.68, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 11);
INSERT INTO `salary_salaryrecord` VALUES (104, '2024-12', 10000.00, 14.9, 846.59, 2, 1, 150.00, 10696.59, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 12);
INSERT INTO `salary_salaryrecord` VALUES (105, '2024-12', 10500.00, 15.2, 906.82, 0, 1, 50.00, 11356.82, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 13);
INSERT INTO `salary_salaryrecord` VALUES (106, '2024-12', 11000.00, 8.2, 512.50, 2, 2, 200.00, 11312.50, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 14);
INSERT INTO `salary_salaryrecord` VALUES (107, '2024-12', 8000.00, 11.3, 513.64, 1, 0, 50.00, 8463.64, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 15);
INSERT INTO `salary_salaryrecord` VALUES (108, '2024-12', 8500.00, 13.1, 632.67, 0, 1, 50.00, 9082.67, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 16);
INSERT INTO `salary_salaryrecord` VALUES (109, '2024-12', 9000.00, 14.3, 731.25, 2, 0, 100.00, 9631.25, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 17);
INSERT INTO `salary_salaryrecord` VALUES (110, '2024-12', 9500.00, 4.3, 232.10, 3, 0, 150.00, 9582.10, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 18);
INSERT INTO `salary_salaryrecord` VALUES (111, '2024-12', 10000.00, 6.0, 340.91, 2, 0, 100.00, 10240.91, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 19);
INSERT INTO `salary_salaryrecord` VALUES (112, '2024-12', 10000.00, 15.4, 875.00, 0, 1, 50.00, 10825.00, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 20);
INSERT INTO `salary_salaryrecord` VALUES (113, '2024-12', 10500.00, 0.9, 53.69, 2, 1, 150.00, 10403.69, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 21);
INSERT INTO `salary_salaryrecord` VALUES (114, '2024-12', 11000.00, 3.4, 212.50, 3, 2, 250.00, 10962.50, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 22);
INSERT INTO `salary_salaryrecord` VALUES (115, '2024-12', 11500.00, 17.4, 1136.93, 4, 2, 300.00, 12336.93, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 23);
INSERT INTO `salary_salaryrecord` VALUES (116, '2024-12', 12000.00, 12.2, 831.82, 1, 0, 50.00, 12781.82, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 24);
INSERT INTO `salary_salaryrecord` VALUES (117, '2024-12', 9000.00, 1.5, 76.70, 3, 0, 150.00, 8926.70, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 25);
INSERT INTO `salary_salaryrecord` VALUES (118, '2024-12', 9500.00, 11.2, 604.55, 3, 1, 200.00, 9904.55, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 26);
INSERT INTO `salary_salaryrecord` VALUES (119, '2024-12', 10000.00, 1.8, 102.27, 4, 2, 300.00, 9802.27, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 27);
INSERT INTO `salary_salaryrecord` VALUES (120, '2024-12', 10500.00, 11.4, 680.11, 4, 0, 200.00, 10980.11, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 28);
INSERT INTO `salary_salaryrecord` VALUES (121, '2024-12', 11000.00, 4.8, 300.00, 0, 1, 50.00, 11250.00, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 29);
INSERT INTO `salary_salaryrecord` VALUES (122, '2024-12', 11000.00, 12.4, 775.00, 0, 0, 0.00, 11775.00, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 30);
INSERT INTO `salary_salaryrecord` VALUES (123, '2024-12', 11500.00, 6.3, 411.65, 4, 0, 200.00, 11711.65, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 31);
INSERT INTO `salary_salaryrecord` VALUES (124, '2024-12', 11500.00, 18.8, 1228.41, 2, 0, 100.00, 12628.41, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 32);
INSERT INTO `salary_salaryrecord` VALUES (125, '2024-12', 12000.00, 15.2, 1036.36, 3, 0, 150.00, 12886.36, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 33);
INSERT INTO `salary_salaryrecord` VALUES (126, '2024-12', 12000.00, 19.1, 1302.27, 3, 1, 200.00, 13102.27, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 34);
INSERT INTO `salary_salaryrecord` VALUES (127, '2024-12', 7500.00, 0.4, 17.05, 4, 2, 300.00, 7217.05, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 35);
INSERT INTO `salary_salaryrecord` VALUES (128, '2024-12', 8000.00, 17.3, 786.36, 4, 2, 300.00, 8486.36, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 36);
INSERT INTO `salary_salaryrecord` VALUES (129, '2024-12', 8500.00, 15.6, 753.41, 1, 2, 150.00, 9103.41, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 37);
INSERT INTO `salary_salaryrecord` VALUES (130, '2024-12', 9000.00, 19.2, 981.82, 3, 0, 150.00, 9831.82, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 38);
INSERT INTO `salary_salaryrecord` VALUES (131, '2024-12', 9500.00, 12.9, 696.31, 2, 0, 100.00, 10096.31, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 39);
INSERT INTO `salary_salaryrecord` VALUES (132, '2024-12', 10000.00, 2.5, 142.05, 3, 0, 150.00, 9992.05, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 40);
INSERT INTO `salary_salaryrecord` VALUES (133, '2024-12', 10000.00, 4.8, 272.73, 1, 2, 150.00, 10122.73, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 41);
INSERT INTO `salary_salaryrecord` VALUES (134, '2024-12', 10500.00, 12.6, 751.70, 3, 0, 150.00, 11101.70, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 42);
INSERT INTO `salary_salaryrecord` VALUES (135, '2024-12', 11000.00, 17.9, 1118.75, 0, 2, 100.00, 12018.75, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 43);
INSERT INTO `salary_salaryrecord` VALUES (136, '2024-12', 11000.00, 10.5, 656.25, 3, 1, 200.00, 11456.25, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 44);
INSERT INTO `salary_salaryrecord` VALUES (137, '2024-12', 7000.00, 6.5, 258.52, 2, 2, 200.00, 7058.52, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 45);
INSERT INTO `salary_salaryrecord` VALUES (138, '2024-12', 7500.00, 3.8, 161.93, 3, 1, 200.00, 7461.93, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 46);
INSERT INTO `salary_salaryrecord` VALUES (139, '2024-12', 8000.00, 5.8, 263.64, 0, 2, 100.00, 8163.64, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 47);
INSERT INTO `salary_salaryrecord` VALUES (140, '2024-12', 8500.00, 6.8, 328.41, 0, 1, 50.00, 8778.41, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 48);
INSERT INTO `salary_salaryrecord` VALUES (141, '2024-12', 9000.00, 13.8, 705.68, 4, 2, 300.00, 9405.68, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 49);
INSERT INTO `salary_salaryrecord` VALUES (142, '2024-12', 7500.00, 18.9, 805.40, 3, 1, 200.00, 8105.40, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 50);
INSERT INTO `salary_salaryrecord` VALUES (143, '2024-12', 8000.00, 17.0, 772.73, 1, 1, 100.00, 8672.73, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 51);
INSERT INTO `salary_salaryrecord` VALUES (144, '2024-12', 8500.00, 10.5, 507.10, 0, 0, 0.00, 9007.10, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 52);
INSERT INTO `salary_salaryrecord` VALUES (145, '2024-12', 8500.00, 8.9, 429.83, 0, 2, 100.00, 8829.83, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 53);
INSERT INTO `salary_salaryrecord` VALUES (146, '2024-12', 9000.00, 19.3, 986.93, 0, 2, 100.00, 9886.93, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 54);
INSERT INTO `salary_salaryrecord` VALUES (147, '2024-12', 9000.00, 17.7, 905.11, 3, 2, 250.00, 9655.11, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 55);
INSERT INTO `salary_salaryrecord` VALUES (148, '2024-12', 9500.00, 10.7, 577.56, 1, 2, 150.00, 9927.56, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 56);
INSERT INTO `salary_salaryrecord` VALUES (149, '2024-12', 10000.00, 11.8, 670.45, 4, 2, 300.00, 10370.45, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 57);
INSERT INTO `salary_salaryrecord` VALUES (150, '2024-12', 6500.00, 8.9, 328.69, 4, 1, 250.00, 6578.69, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 58);
INSERT INTO `salary_salaryrecord` VALUES (151, '2024-12', 7000.00, 11.3, 449.43, 2, 0, 100.00, 7349.43, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 59);
INSERT INTO `salary_salaryrecord` VALUES (152, '2024-12', 7500.00, 6.9, 294.03, 2, 1, 150.00, 7644.03, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 60);
INSERT INTO `salary_salaryrecord` VALUES (153, '2024-12', 7500.00, 2.1, 89.49, 2, 0, 100.00, 7489.49, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 61);
INSERT INTO `salary_salaryrecord` VALUES (154, '2024-12', 8000.00, 5.8, 263.64, 0, 1, 50.00, 8213.64, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 62);
INSERT INTO `salary_salaryrecord` VALUES (155, '2024-12', 8000.00, 2.8, 127.27, 0, 0, 0.00, 8127.27, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 63);
INSERT INTO `salary_salaryrecord` VALUES (156, '2024-12', 8500.00, 3.4, 164.20, 1, 2, 150.00, 8514.20, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 64);
INSERT INTO `salary_salaryrecord` VALUES (157, '2024-12', 8500.00, 4.5, 217.33, 0, 1, 50.00, 8667.33, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 65);
INSERT INTO `salary_salaryrecord` VALUES (158, '2024-12', 9000.00, 17.9, 915.34, 1, 0, 50.00, 9865.34, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 66);
INSERT INTO `salary_salaryrecord` VALUES (159, '2024-12', 9000.00, 6.8, 347.73, 3, 1, 200.00, 9147.73, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 67);
INSERT INTO `salary_salaryrecord` VALUES (160, '2024-12', 8500.00, 9.8, 473.30, 1, 0, 50.00, 8923.30, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 68);
INSERT INTO `salary_salaryrecord` VALUES (161, '2024-12', 9000.00, 19.5, 997.16, 0, 2, 100.00, 9897.16, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 69);
INSERT INTO `salary_salaryrecord` VALUES (162, '2024-12', 9500.00, 2.7, 145.74, 0, 0, 0.00, 9645.74, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 70);
INSERT INTO `salary_salaryrecord` VALUES (163, '2024-12', 10000.00, 16.5, 937.50, 2, 2, 200.00, 10737.50, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 71);
INSERT INTO `salary_salaryrecord` VALUES (164, '2024-12', 10000.00, 8.3, 471.59, 4, 2, 300.00, 10171.59, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 72);
INSERT INTO `salary_salaryrecord` VALUES (165, '2024-12', 10500.00, 5.6, 334.09, 4, 0, 200.00, 10634.09, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 73);
INSERT INTO `salary_salaryrecord` VALUES (166, '2024-12', 10500.00, 3.7, 220.74, 1, 2, 150.00, 10570.74, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 74);
INSERT INTO `salary_salaryrecord` VALUES (167, '2024-12', 11000.00, 11.8, 737.50, 0, 1, 50.00, 11687.50, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 75);
INSERT INTO `salary_salaryrecord` VALUES (168, '2024-12', 5500.00, 7.3, 228.13, 1, 2, 150.00, 5578.13, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 76);
INSERT INTO `salary_salaryrecord` VALUES (169, '2024-12', 6000.00, 11.8, 402.27, 4, 2, 300.00, 6102.27, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 77);
INSERT INTO `salary_salaryrecord` VALUES (170, '2024-12', 6500.00, 11.2, 413.64, 4, 0, 200.00, 6713.64, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 78);
INSERT INTO `salary_salaryrecord` VALUES (171, '2024-12', 6500.00, 16.4, 605.68, 4, 0, 200.00, 6905.68, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 79);
INSERT INTO `salary_salaryrecord` VALUES (172, '2024-12', 7000.00, 9.0, 357.95, 1, 0, 50.00, 7307.95, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 80);
INSERT INTO `salary_salaryrecord` VALUES (173, '2024-12', 7000.00, 5.2, 206.82, 2, 1, 150.00, 7056.82, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 81);
INSERT INTO `salary_salaryrecord` VALUES (174, '2024-12', 7500.00, 15.9, 677.56, 1, 2, 150.00, 8027.56, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 82);
INSERT INTO `salary_salaryrecord` VALUES (175, '2024-12', 7500.00, 16.6, 707.39, 4, 1, 250.00, 7957.39, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 83);
INSERT INTO `salary_salaryrecord` VALUES (176, '2024-12', 6000.00, 0.3, 10.23, 1, 2, 150.00, 5860.23, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 84);
INSERT INTO `salary_salaryrecord` VALUES (177, '2024-12', 6500.00, 8.0, 295.45, 1, 2, 150.00, 6645.45, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 85);
INSERT INTO `salary_salaryrecord` VALUES (178, '2024-12', 7000.00, 1.1, 43.75, 4, 1, 250.00, 6793.75, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 86);
INSERT INTO `salary_salaryrecord` VALUES (179, '2024-12', 7000.00, 0.0, 0.00, 2, 1, 150.00, 6850.00, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 87);
INSERT INTO `salary_salaryrecord` VALUES (180, '2024-12', 7500.00, 11.1, 473.01, 0, 1, 50.00, 7923.01, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 88);
INSERT INTO `salary_salaryrecord` VALUES (181, '2024-12', 10000.00, 4.8, 272.73, 2, 2, 200.00, 10072.73, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 89);
INSERT INTO `salary_salaryrecord` VALUES (182, '2024-12', 11000.00, 0.5, 31.25, 0, 0, 0.00, 11031.25, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 90);
INSERT INTO `salary_salaryrecord` VALUES (183, '2024-12', 9000.00, 11.6, 593.18, 3, 2, 250.00, 9343.18, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 91);
INSERT INTO `salary_salaryrecord` VALUES (184, '2024-12', 10000.00, 8.5, 482.95, 2, 1, 150.00, 10332.95, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 92);
INSERT INTO `salary_salaryrecord` VALUES (185, '2024-12', 8500.00, 3.0, 144.89, 2, 0, 100.00, 8544.89, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 93);
INSERT INTO `salary_salaryrecord` VALUES (186, '2024-12', 7500.00, 9.7, 413.35, 0, 1, 50.00, 7863.35, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 94);
INSERT INTO `salary_salaryrecord` VALUES (187, '2024-12', 8500.00, 1.2, 57.95, 4, 1, 250.00, 8307.95, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 95);
INSERT INTO `salary_salaryrecord` VALUES (188, '2024-12', 6500.00, 4.0, 147.73, 1, 0, 50.00, 6597.73, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 96);
INSERT INTO `salary_salaryrecord` VALUES (189, '2024-12', 9500.00, 16.0, 863.64, 3, 0, 150.00, 10213.64, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 97);
INSERT INTO `salary_salaryrecord` VALUES (190, '2024-12', 7500.00, 12.8, 545.45, 3, 2, 250.00, 7795.45, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 98);
INSERT INTO `salary_salaryrecord` VALUES (191, '2024-12', 6500.00, 1.2, 44.32, 1, 0, 50.00, 6494.32, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 99);
INSERT INTO `salary_salaryrecord` VALUES (192, '2024-12', 10000.00, 11.5, 653.41, 2, 2, 200.00, 10453.41, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 100);
INSERT INTO `salary_salaryrecord` VALUES (193, '2025-01', 8000.00, 16.0, 727.27, 3, 2, 250.00, 8477.27, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 5);
INSERT INTO `salary_salaryrecord` VALUES (194, '2025-01', 8500.00, 16.9, 816.19, 2, 2, 200.00, 9116.19, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 6);
INSERT INTO `salary_salaryrecord` VALUES (195, '2025-01', 9000.00, 8.1, 414.20, 4, 2, 300.00, 9114.20, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 7);
INSERT INTO `salary_salaryrecord` VALUES (196, '2025-01', 9000.00, 2.1, 107.39, 1, 2, 150.00, 8957.39, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 8);
INSERT INTO `salary_salaryrecord` VALUES (197, '2025-01', 9500.00, 11.9, 642.33, 3, 1, 200.00, 9942.33, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 9);
INSERT INTO `salary_salaryrecord` VALUES (198, '2025-01', 9500.00, 15.0, 809.66, 3, 1, 200.00, 10109.66, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 10);
INSERT INTO `salary_salaryrecord` VALUES (199, '2025-01', 10000.00, 10.8, 613.64, 0, 2, 100.00, 10513.64, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 11);
INSERT INTO `salary_salaryrecord` VALUES (200, '2025-01', 10000.00, 2.0, 113.64, 3, 1, 200.00, 9913.64, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 12);
INSERT INTO `salary_salaryrecord` VALUES (201, '2025-01', 10500.00, 13.1, 781.53, 3, 0, 150.00, 11131.53, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 13);
INSERT INTO `salary_salaryrecord` VALUES (202, '2025-01', 11000.00, 18.4, 1150.00, 4, 2, 300.00, 11850.00, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 14);
INSERT INTO `salary_salaryrecord` VALUES (203, '2025-01', 8000.00, 9.3, 422.73, 4, 2, 300.00, 8122.73, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 15);
INSERT INTO `salary_salaryrecord` VALUES (204, '2025-01', 8500.00, 0.5, 24.15, 4, 2, 300.00, 8224.15, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 16);
INSERT INTO `salary_salaryrecord` VALUES (205, '2025-01', 9000.00, 4.4, 225.00, 2, 1, 150.00, 9075.00, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 17);
INSERT INTO `salary_salaryrecord` VALUES (206, '2025-01', 9500.00, 8.1, 437.22, 4, 0, 200.00, 9737.22, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 18);
INSERT INTO `salary_salaryrecord` VALUES (207, '2025-01', 10000.00, 17.5, 994.32, 2, 2, 200.00, 10794.32, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 19);
INSERT INTO `salary_salaryrecord` VALUES (208, '2025-01', 10000.00, 6.1, 346.59, 4, 0, 200.00, 10146.59, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 20);
INSERT INTO `salary_salaryrecord` VALUES (209, '2025-01', 10500.00, 8.1, 483.24, 4, 0, 200.00, 10783.24, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 21);
INSERT INTO `salary_salaryrecord` VALUES (210, '2025-01', 11000.00, 18.8, 1175.00, 0, 1, 50.00, 12125.00, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 22);
INSERT INTO `salary_salaryrecord` VALUES (211, '2025-01', 11500.00, 2.5, 163.35, 2, 1, 150.00, 11513.35, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 23);
INSERT INTO `salary_salaryrecord` VALUES (212, '2025-01', 12000.00, 5.5, 375.00, 2, 2, 200.00, 12175.00, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 24);
INSERT INTO `salary_salaryrecord` VALUES (213, '2025-01', 9000.00, 16.6, 848.86, 1, 1, 100.00, 9748.86, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 25);
INSERT INTO `salary_salaryrecord` VALUES (214, '2025-01', 9500.00, 7.6, 410.23, 4, 1, 250.00, 9660.23, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 26);
INSERT INTO `salary_salaryrecord` VALUES (215, '2025-01', 10000.00, 5.9, 335.23, 2, 1, 150.00, 10185.23, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 27);
INSERT INTO `salary_salaryrecord` VALUES (216, '2025-01', 10500.00, 19.6, 1169.32, 2, 0, 100.00, 11569.32, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 28);
INSERT INTO `salary_salaryrecord` VALUES (217, '2025-01', 11000.00, 5.2, 325.00, 4, 1, 250.00, 11075.00, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 29);
INSERT INTO `salary_salaryrecord` VALUES (218, '2025-01', 11000.00, 13.4, 837.50, 2, 2, 200.00, 11637.50, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 30);
INSERT INTO `salary_salaryrecord` VALUES (219, '2025-01', 11500.00, 12.2, 797.16, 3, 2, 250.00, 12047.16, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 31);
INSERT INTO `salary_salaryrecord` VALUES (220, '2025-01', 11500.00, 6.2, 405.11, 1, 2, 150.00, 11755.11, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 32);
INSERT INTO `salary_salaryrecord` VALUES (221, '2025-01', 12000.00, 9.3, 634.09, 4, 1, 250.00, 12384.09, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 33);
INSERT INTO `salary_salaryrecord` VALUES (222, '2025-01', 12000.00, 8.1, 552.27, 4, 0, 200.00, 12352.27, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 34);
INSERT INTO `salary_salaryrecord` VALUES (223, '2025-01', 7500.00, 3.6, 153.41, 0, 0, 0.00, 7653.41, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 35);
INSERT INTO `salary_salaryrecord` VALUES (224, '2025-01', 8000.00, 3.7, 168.18, 3, 2, 250.00, 7918.18, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 36);
INSERT INTO `salary_salaryrecord` VALUES (225, '2025-01', 8500.00, 4.3, 207.67, 3, 0, 150.00, 8557.67, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 37);
INSERT INTO `salary_salaryrecord` VALUES (226, '2025-01', 9000.00, 7.5, 383.52, 1, 0, 50.00, 9333.52, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 38);
INSERT INTO `salary_salaryrecord` VALUES (227, '2025-01', 9500.00, 16.5, 890.62, 0, 1, 50.00, 10340.62, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 39);
INSERT INTO `salary_salaryrecord` VALUES (228, '2025-01', 10000.00, 18.4, 1045.45, 3, 0, 150.00, 10895.45, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 40);
INSERT INTO `salary_salaryrecord` VALUES (229, '2025-01', 10000.00, 18.1, 1028.41, 3, 0, 150.00, 10878.41, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 41);
INSERT INTO `salary_salaryrecord` VALUES (230, '2025-01', 10500.00, 13.4, 799.43, 1, 2, 150.00, 11149.43, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 42);
INSERT INTO `salary_salaryrecord` VALUES (231, '2025-01', 11000.00, 18.4, 1150.00, 3, 1, 200.00, 11950.00, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 43);
INSERT INTO `salary_salaryrecord` VALUES (232, '2025-01', 11000.00, 18.8, 1175.00, 1, 1, 100.00, 12075.00, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 44);
INSERT INTO `salary_salaryrecord` VALUES (233, '2025-01', 7000.00, 8.6, 342.05, 2, 2, 200.00, 7142.05, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 45);
INSERT INTO `salary_salaryrecord` VALUES (234, '2025-01', 7500.00, 17.9, 762.78, 2, 1, 150.00, 8112.78, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 46);
INSERT INTO `salary_salaryrecord` VALUES (235, '2025-01', 8000.00, 9.7, 440.91, 2, 2, 200.00, 8240.91, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 47);
INSERT INTO `salary_salaryrecord` VALUES (236, '2025-01', 8500.00, 8.8, 425.00, 1, 2, 150.00, 8775.00, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 48);
INSERT INTO `salary_salaryrecord` VALUES (237, '2025-01', 9000.00, 11.3, 577.84, 3, 1, 200.00, 9377.84, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 49);
INSERT INTO `salary_salaryrecord` VALUES (238, '2025-01', 7500.00, 0.8, 34.09, 2, 2, 200.00, 7334.09, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 50);
INSERT INTO `salary_salaryrecord` VALUES (239, '2025-01', 8000.00, 8.9, 404.55, 4, 0, 200.00, 8204.55, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 51);
INSERT INTO `salary_salaryrecord` VALUES (240, '2025-01', 8500.00, 3.0, 144.89, 2, 2, 200.00, 8444.89, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 52);
INSERT INTO `salary_salaryrecord` VALUES (241, '2025-01', 8500.00, 17.8, 859.66, 0, 0, 0.00, 9359.66, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 53);
INSERT INTO `salary_salaryrecord` VALUES (242, '2025-01', 9000.00, 11.8, 603.41, 3, 1, 200.00, 9403.41, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 54);
INSERT INTO `salary_salaryrecord` VALUES (243, '2025-01', 9000.00, 19.0, 971.59, 3, 0, 150.00, 9821.59, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 55);
INSERT INTO `salary_salaryrecord` VALUES (244, '2025-01', 9500.00, 9.4, 507.39, 3, 0, 150.00, 9857.39, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 56);
INSERT INTO `salary_salaryrecord` VALUES (245, '2025-01', 10000.00, 19.0, 1079.55, 0, 1, 50.00, 11029.55, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 57);
INSERT INTO `salary_salaryrecord` VALUES (246, '2025-01', 6500.00, 2.0, 73.86, 1, 2, 150.00, 6423.86, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 58);
INSERT INTO `salary_salaryrecord` VALUES (247, '2025-01', 7000.00, 7.2, 286.36, 3, 1, 200.00, 7086.36, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 59);
INSERT INTO `salary_salaryrecord` VALUES (248, '2025-01', 7500.00, 2.1, 89.49, 2, 0, 100.00, 7489.49, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 60);
INSERT INTO `salary_salaryrecord` VALUES (249, '2025-01', 7500.00, 1.0, 42.61, 1, 1, 100.00, 7442.61, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 61);
INSERT INTO `salary_salaryrecord` VALUES (250, '2025-01', 8000.00, 1.5, 68.18, 4, 2, 300.00, 7768.18, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 62);
INSERT INTO `salary_salaryrecord` VALUES (251, '2025-01', 8000.00, 11.6, 527.27, 0, 0, 0.00, 8527.27, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 63);
INSERT INTO `salary_salaryrecord` VALUES (252, '2025-01', 8500.00, 0.7, 33.81, 1, 2, 150.00, 8383.81, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 64);
INSERT INTO `salary_salaryrecord` VALUES (253, '2025-01', 8500.00, 6.5, 313.92, 0, 2, 100.00, 8713.92, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 65);
INSERT INTO `salary_salaryrecord` VALUES (254, '2025-01', 9000.00, 7.9, 403.98, 3, 0, 150.00, 9253.98, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 66);
INSERT INTO `salary_salaryrecord` VALUES (255, '2025-01', 9000.00, 8.9, 455.11, 4, 0, 200.00, 9255.11, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 67);
INSERT INTO `salary_salaryrecord` VALUES (256, '2025-01', 8500.00, 4.2, 202.84, 0, 1, 50.00, 8652.84, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 68);
INSERT INTO `salary_salaryrecord` VALUES (257, '2025-01', 9000.00, 19.3, 986.93, 3, 1, 200.00, 9786.93, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 69);
INSERT INTO `salary_salaryrecord` VALUES (258, '2025-01', 9500.00, 15.7, 847.44, 0, 1, 50.00, 10297.44, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 70);
INSERT INTO `salary_salaryrecord` VALUES (259, '2025-01', 10000.00, 13.9, 789.77, 0, 0, 0.00, 10789.77, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 71);
INSERT INTO `salary_salaryrecord` VALUES (260, '2025-01', 10000.00, 4.6, 261.36, 4, 0, 200.00, 10061.36, 'draft', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 72);
INSERT INTO `salary_salaryrecord` VALUES (261, '2025-01', 10500.00, 20.0, 1193.18, 1, 1, 100.00, 11593.18, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 73);
INSERT INTO `salary_salaryrecord` VALUES (262, '2025-01', 10500.00, 4.1, 244.60, 3, 0, 150.00, 10594.60, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 74);
INSERT INTO `salary_salaryrecord` VALUES (263, '2025-01', 11000.00, 17.1, 1068.75, 3, 1, 200.00, 11868.75, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 75);
INSERT INTO `salary_salaryrecord` VALUES (264, '2025-01', 5500.00, 13.1, 409.38, 0, 1, 50.00, 5859.38, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 76);
INSERT INTO `salary_salaryrecord` VALUES (265, '2025-01', 6000.00, 17.2, 586.36, 0, 0, 0.00, 6586.36, 'published', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 77);
INSERT INTO `salary_salaryrecord` VALUES (266, '2025-01', 6500.00, 15.0, 553.98, 3, 0, 150.00, 6903.98, 'published', '2026-01-24 16:13:28.000000', '2026-01-24 16:13:28.000000', 78);
INSERT INTO `salary_salaryrecord` VALUES (267, '2025-01', 6500.00, 13.0, 480.11, 2, 0, 100.00, 6880.11, 'draft', '2026-01-24 16:13:28.000000', '2026-01-24 16:13:28.000000', 79);
INSERT INTO `salary_salaryrecord` VALUES (268, '2025-01', 7000.00, 12.3, 489.20, 2, 1, 150.00, 7339.20, 'published', '2026-01-24 16:13:28.000000', '2026-01-24 16:13:28.000000', 80);
INSERT INTO `salary_salaryrecord` VALUES (269, '2025-01', 7000.00, 19.1, 759.66, 0, 2, 100.00, 7659.66, 'published', '2026-01-24 16:13:28.000000', '2026-01-24 16:13:28.000000', 81);
INSERT INTO `salary_salaryrecord` VALUES (270, '2025-01', 7500.00, 16.6, 707.39, 2, 1, 150.00, 8057.39, 'published', '2026-01-24 16:13:28.000000', '2026-01-24 16:13:28.000000', 82);
INSERT INTO `salary_salaryrecord` VALUES (271, '2025-01', 7500.00, 13.4, 571.02, 0, 2, 100.00, 7971.02, 'draft', '2026-01-24 16:13:28.000000', '2026-01-24 16:13:28.000000', 83);
INSERT INTO `salary_salaryrecord` VALUES (272, '2025-01', 6000.00, 3.0, 102.27, 4, 2, 300.00, 5802.27, 'published', '2026-01-24 16:13:28.000000', '2026-01-24 16:13:28.000000', 84);
INSERT INTO `salary_salaryrecord` VALUES (273, '2025-01', 6500.00, 2.1, 77.56, 1, 1, 100.00, 6477.56, 'draft', '2026-01-24 16:13:28.000000', '2026-01-24 16:13:28.000000', 85);
INSERT INTO `salary_salaryrecord` VALUES (274, '2025-01', 7000.00, 7.3, 290.34, 1, 1, 100.00, 7190.34, 'draft', '2026-01-24 16:13:28.000000', '2026-01-24 16:13:28.000000', 86);
INSERT INTO `salary_salaryrecord` VALUES (275, '2025-01', 7000.00, 10.7, 425.57, 0, 0, 0.00, 7425.57, 'draft', '2026-01-24 16:13:28.000000', '2026-01-24 16:13:28.000000', 87);
INSERT INTO `salary_salaryrecord` VALUES (276, '2025-01', 7500.00, 3.7, 157.67, 1, 0, 50.00, 7607.67, 'published', '2026-01-24 16:13:28.000000', '2026-01-24 16:13:28.000000', 88);
INSERT INTO `salary_salaryrecord` VALUES (277, '2025-01', 10000.00, 9.9, 562.50, 0, 1, 50.00, 10512.50, 'published', '2026-01-24 16:13:28.000000', '2026-01-24 16:13:28.000000', 89);
INSERT INTO `salary_salaryrecord` VALUES (278, '2025-01', 11000.00, 3.7, 231.25, 0, 0, 0.00, 11231.25, 'published', '2026-01-24 16:13:28.000000', '2026-01-24 16:13:28.000000', 90);
INSERT INTO `salary_salaryrecord` VALUES (279, '2025-01', 9000.00, 9.2, 470.45, 0, 2, 100.00, 9370.45, 'draft', '2026-01-24 16:13:28.000000', '2026-01-24 16:13:28.000000', 91);
INSERT INTO `salary_salaryrecord` VALUES (280, '2025-01', 10000.00, 9.3, 528.41, 1, 1, 100.00, 10428.41, 'published', '2026-01-24 16:13:28.000000', '2026-01-24 16:13:28.000000', 92);
INSERT INTO `salary_salaryrecord` VALUES (281, '2025-01', 8500.00, 12.2, 589.20, 2, 1, 150.00, 8939.20, 'draft', '2026-01-24 16:13:28.000000', '2026-01-24 16:13:28.000000', 93);
INSERT INTO `salary_salaryrecord` VALUES (282, '2025-01', 7500.00, 2.6, 110.80, 4, 1, 250.00, 7360.80, 'draft', '2026-01-24 16:13:28.000000', '2026-01-24 16:13:28.000000', 94);
INSERT INTO `salary_salaryrecord` VALUES (283, '2025-01', 8500.00, 15.9, 767.90, 0, 2, 100.00, 9167.90, 'draft', '2026-01-24 16:13:28.000000', '2026-01-24 16:13:28.000000', 95);
INSERT INTO `salary_salaryrecord` VALUES (284, '2025-01', 6500.00, 3.1, 114.49, 0, 2, 100.00, 6514.49, 'published', '2026-01-24 16:13:28.000000', '2026-01-24 16:13:28.000000', 96);
INSERT INTO `salary_salaryrecord` VALUES (285, '2025-01', 9500.00, 1.2, 64.77, 4, 2, 300.00, 9264.77, 'draft', '2026-01-24 16:13:28.000000', '2026-01-24 16:13:28.000000', 97);
INSERT INTO `salary_salaryrecord` VALUES (286, '2025-01', 7500.00, 9.4, 400.57, 2, 2, 200.00, 8100.57, 'published', '2026-01-24 16:13:28.000000', '2026-01-25 09:25:37.340366', 98);
INSERT INTO `salary_salaryrecord` VALUES (287, '2025-01', 6500.00, 17.8, 657.39, 2, 2, 200.00, 6957.39, 'published', '2026-01-24 16:13:28.000000', '2026-01-24 16:13:28.000000', 99);
INSERT INTO `salary_salaryrecord` VALUES (288, '2025-01', 10000.00, 4.3, 244.32, 1, 1, 100.00, 10144.32, 'published', '2026-01-24 16:13:28.000000', '2026-01-24 16:13:28.000000', 100);

-- ----------------------------
-- Procedure structure for generate_attendance
-- ----------------------------
DROP PROCEDURE IF EXISTS `generate_attendance`;
delimiter ;;
CREATE PROCEDURE `generate_attendance`(IN start_user INT, IN end_user INT, IN start_date DATE, IN num_days INT)
BEGIN
    DECLARE u INT;
    DECLARE d DATE;
    DECLARE i INT DEFAULT 0;
    DECLARE w INT;
    DECLARE r INT;
    DECLARE in_t TIME;
    DECLARE out_t TIME;
    DECLARE stat VARCHAR(20);

    SET i = 0;
    WHILE i < num_days DO
        SET d = DATE_ADD(start_date, INTERVAL i DAY);
        SET w = DAYOFWEEK(d);
        IF w BETWEEN 2 AND 6 THEN
            SET u = start_user;
            WHILE u <= end_user DO
                SET r = RAND() * 100;
                IF r < 85 THEN
                    SET in_t = TIME('08:55:00') + INTERVAL (RAND() * 10) SECOND;
                    SET out_t = TIME('18:05:00') + INTERVAL (RAND() * 10) SECOND;
                    SET stat = 'normal';
                ELSEIF r < 95 THEN
                    SET in_t = TIME('09:05:00') + INTERVAL (RAND() * 30) SECOND;
                    SET out_t = NULL;
                    SET stat = 'late';
                ELSEIF r < 98 THEN
                    SET in_t = NULL;
                    SET out_t = TIME('17:45:00') + INTERVAL (RAND() * 10) SECOND;
                    SET stat = 'early';
                ELSE
                    SET in_t = NULL;
                    SET out_t = NULL;
                    SET stat = 'absent';
                END IF;
                INSERT INTO attendance_attendance (date, check_in_time, check_out_time, status, created_at, updated_at, user_id)
                VALUES (d, in_t, out_t, stat, NOW(), NOW(), u);
                SET u = u + 1;
            END WHILE;
        END IF;
        SET i = i + 1;
    END WHILE;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for generate_salary
-- ----------------------------
DROP PROCEDURE IF EXISTS `generate_salary`;
delimiter ;;
CREATE PROCEDURE `generate_salary`(IN start_user INT, IN end_user INT, IN sal_month VARCHAR(7))
BEGIN
    DECLARE u INT;
    DECLARE base DEC(10,2);
    DECLARE ot_hours DEC(6,1);
    DECLARE ot_pay DEC(10,2);
    DECLARE late_cnt INT;
    DECLARE early_cnt INT;
    DECLARE ded DEC(10,2);
    DECLARE final DEC(10,2);
    DECLARE r INT;

    SET u = start_user;
    WHILE u <= end_user DO
        SELECT salary_base INTO base FROM employee_employeeprofile WHERE user_id = u LIMIT 1;
        IF base IS NOT NULL THEN
            SET ot_hours = RAND() * 20;
            SET ot_pay = ROUND(ot_hours * (base / 22 / 8), 2);
            SET late_cnt = FLOOR(RAND() * 5);
            SET early_cnt = FLOOR(RAND() * 3);
            SET ded = (late_cnt + early_cnt) * 50;
            SET final = base + ot_pay - ded;
            SET r = RAND() * 100;
            IF r < 80 THEN
                INSERT INTO salary_salaryrecord (month, base_salary, overtime_hours, overtime_pay, late_count, early_count, attendance_deduction, final_salary, status, created_at, updated_at, user_id)
                VALUES (sal_month, base, ot_hours, ot_pay, late_cnt, early_cnt, ded, final, 'published', NOW(), NOW(), u);
            ELSE
                INSERT INTO salary_salaryrecord (month, base_salary, overtime_hours, overtime_pay, late_count, early_count, attendance_deduction, final_salary, status, created_at, updated_at, user_id)
                VALUES (sal_month, base, ot_hours, ot_pay, late_cnt, early_cnt, ded, final, 'draft', NOW(), NOW(), u);
            END IF;
        END IF;
        SET u = u + 1;
    END WHILE;
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
