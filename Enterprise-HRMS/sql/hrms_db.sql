/*
 Navicat Premium Dump SQL

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80027 (8.0.27)
 Source Host           : localhost:3306
 Source Schema         : hrms_db

 Target Server Type    : MySQL
 Target Server Version : 80027 (8.0.27)
 File Encoding         : 65001

 Date: 27/01/2026 15:29:00
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
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of accounts_rolepermission
-- ----------------------------
INSERT INTO `accounts_rolepermission` VALUES (1, 'employee', '[\"employeeDashboard\", \"profile\", \"attendanceCenter\", \"applicationCenter\", \"salary\", \"myPerformance\", \"notices\", \"exceptionReport\"]', '[\"checkIn\", \"checkOut\", \"applyLeave\", \"applyOvertime\", \"viewSalary\", \"reportException\"]', 'self', 'self', 'self', 0, 1, '2026-01-25 06:18:05.928470', '2026-01-27 04:33:30.497714');
INSERT INTO `accounts_rolepermission` VALUES (2, 'hr', '[\"dashboard\", \"employees\", \"departments\", \"posts\", \"onboarding\", \"resignation\", \"attendance\", \"approval\", \"salary\", \"salaryException\", \"performanceReview\", \"notices\", \"profile\"]', '[\"createEmployee\", \"editEmployee\", \"deleteEmployee\", \"approveLeave\", \"approveOvertime\", \"calculateSalary\", \"publishSalary\", \"createNotice\"]', 'all', 'all', 'all', 1, 1, '2026-01-25 06:18:05.931487', '2026-01-27 06:59:41.558369');
INSERT INTO `accounts_rolepermission` VALUES (3, 'admin', '[\"dashboard\", \"users\", \"permissionConfig\", \"securityConfig\", \"dataCenter\", \"noticeManagement\", \"salaryException\", \"profile\"]', '[\"manageUsers\", \"resetPassword\", \"configurePermissions\", \"viewSalary\"]', 'all', 'all', 'all', 1, 1, '2026-01-25 06:18:05.934544', '2026-01-26 15:12:39.435318');

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
  `password_storage_mode` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  CONSTRAINT `accounts_systemconfig_chk_1` CHECK (`password_min_length` >= 0),
  CONSTRAINT `accounts_systemconfig_chk_2` CHECK (`max_login_attempts` >= 0),
  CONSTRAINT `accounts_systemconfig_chk_3` CHECK (`login_lockout_duration` >= 0),
  CONSTRAINT `accounts_systemconfig_chk_4` CHECK (`session_timeout` >= 0)
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of accounts_systemconfig
-- ----------------------------
INSERT INTO `accounts_systemconfig` VALUES (1, 0, 6, 0, 1, 1, 0, 5, 30, 120, 1, '2026-01-25 09:38:48.100085', '2026-01-27 07:28:16.459183', 'encrypted');

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
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `emergency_contact` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `id_card` varchar(18) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE,
  UNIQUE INDEX `phone`(`phone` ASC) USING BTREE,
  UNIQUE INDEX `email`(`email` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 420 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of accounts_user
-- ----------------------------
INSERT INTO `accounts_user` VALUES (1, 'pbkdf2_sha256$1200000$TVg75PBUb2acPoaOWj7lZb$74yqszp/nqu6Ipf2u8x1x/i0eme0cc2tahenb69y4nc=', '2026-01-24 16:10:19.000000', 1, 'admin', '', '', 1, 1, '2024-01-01 00:00:00.000000', '18199987365', 'admin', '系统管理员', 'admin@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (2, 'pbkdf2_sha256$1000000$lDNodM8tMbW3RLVSajVdl8$QMcvAzSPhPPYUf9s/7MjW1UdqYMSm/z9Oi8VwMIYzB8=', '2026-01-24 16:10:19.000000', 0, 'hr001', '', '', 1, 1, '2024-01-15 00:00:00.000000', '13800000002', 'hr', '张人事', 'hr001@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (3, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'hr002', '', '', 1, 1, '2024-02-01 00:00:00.000000', '13800000003', 'hr', '李人事', 'hr002@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (4, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'hr003', '', '', 1, 1, '2024-03-01 00:00:00.000000', '13800000004', 'hr', '王人事', 'hr003@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (5, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0001', '', '', 0, 0, '2024-01-10 00:00:00.000000', '13800000005', 'employee', '张伟', 'zhangwei@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (6, 'pbkdf2_sha256$1200000$vo4CNrAGpG9TomyqQkSGrK$xKOH8kTZJy32dT0k7dBOrWPERKCT2AKPHUbCW3TFbXo=', '2026-01-24 16:10:19.000000', 0, 'emp0002', '', '', 0, 1, '2024-01-15 00:00:00.000000', '13800000006', 'employee', '李娜', 'lina@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (7, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0003', '', '', 0, 1, '2024-02-01 00:00:00.000000', '13800000007', 'employee', '王强', 'wangqiang@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (8, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0004', '', '', 0, 1, '2024-02-10 00:00:00.000000', '13800000008', 'employee', '刘洋', 'liuyang@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (9, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0005', '', '', 0, 1, '2024-02-20 00:00:00.000000', '13800000009', 'employee', '陈静', 'chenjing@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (10, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0006', '', '', 0, 1, '2024-03-01 00:00:00.000000', '13800000010', 'employee', '赵磊', 'zhaolei@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (11, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0007', '', '', 0, 1, '2024-03-05 00:00:00.000000', '13800000011', 'employee', '吴敏', 'wumin@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (12, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0008', '', '', 0, 1, '2024-03-10 00:00:00.000000', '13800000012', 'employee', '周杰', 'zhoujie@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (13, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0009', '', '', 0, 1, '2024-03-15 00:00:00.000000', '13800000013', 'employee', '徐丽', 'xuli@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (14, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0010', '', '', 0, 1, '2024-03-20 00:00:00.000000', '13800000014', 'employee', '孙鹏', 'sunpeng@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (15, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0011', '', '', 0, 1, '2024-04-01 00:00:00.000000', '13800000015', 'employee', '马艳', 'mayan@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (16, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0012', '', '', 0, 1, '2024-04-05 00:00:00.000000', '13800000016', 'employee', '朱浩', 'zhuhao@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (17, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0013', '', '', 0, 1, '2024-04-10 00:00:00.000000', '13800000017', 'employee', '胡芳', 'hufang@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (18, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0014', '', '', 0, 1, '2024-04-15 00:00:00.000000', '13800000018', 'employee', '林宇', 'linyu@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (19, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0015', '', '', 0, 1, '2024-04-20 00:00:00.000000', '13800000019', 'employee', '韩梅', 'hanmei@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (20, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0016', '', '', 0, 1, '2024-05-01 00:00:00.000000', '13800000020', 'employee', '高健', 'gaojian@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (21, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0017', '', '', 0, 1, '2024-05-05 00:00:00.000000', '13800000021', 'employee', '谢婷', 'xieting@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (22, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0018', '', '', 0, 1, '2024-05-10 00:00:00.000000', '13800000022', 'employee', '唐伟', 'tangwei@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (23, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0019', '', '', 0, 1, '2024-05-15 00:00:00.000000', '13800000023', 'employee', '董雪', 'dongxue@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (24, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0020', '', '', 0, 1, '2024-05-20 00:00:00.000000', '13800000024', 'employee', '冯涛', 'fengtao@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (25, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0021', '', '', 0, 1, '2024-01-20 00:00:00.000000', '13800000025', 'employee', '曹鹏', 'caopeng@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (26, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0022', '', '', 0, 1, '2024-02-15 00:00:00.000000', '13800000026', 'employee', '邓琴', 'dengqin@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (27, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0023', '', '', 0, 1, '2024-03-01 00:00:00.000000', '13800000027', 'employee', '苏磊', 'sulei@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (28, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0024', '', '', 0, 1, '2024-03-20 00:00:00.000000', '13800000028', 'employee', '杨帆', 'yangfan@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (29, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0025', '', '', 0, 1, '2024-04-01 00:00:00.000000', '13800000029', 'employee', '于慧', 'yuhui@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (30, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0026', '', '', 0, 1, '2024-04-15 00:00:00.000000', '13800000030', 'employee', '何刚', 'hegang@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (31, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0027', '', '', 0, 1, '2024-05-01 00:00:00.000000', '13800000031', 'employee', '吕娜', 'lvna@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (32, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0028', '', '', 0, 1, '2024-05-10 00:00:00.000000', '13800000032', 'employee', '潘明', 'panming@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (33, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0029', '', '', 0, 1, '2024-05-20 00:00:00.000000', '13800000033', 'employee', '罗娟', 'luojuan@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (34, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0030', '', '', 0, 1, '2024-06-01 00:00:00.000000', '13800000034', 'employee', '肖鹏', 'xiaopeng@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (35, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0031', '', '', 0, 0, '2024-01-25 00:00:00.000000', '13800000035', 'employee', '梁伟', 'liangwei@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (36, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0032', '', '', 0, 1, '2024-02-20 00:00:00.000000', '13800000036', 'employee', '田莉', 'tianli@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (37, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0033', '', '', 0, 1, '2024-03-10 00:00:00.000000', '13800000037', 'employee', '蒋明', 'jiangming@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (38, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0034', '', '', 0, 1, '2024-03-25 00:00:00.000000', '13800000038', 'employee', '雷艳', 'leiyan@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (39, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0035', '', '', 0, 1, '2024-04-05 00:00:00.000000', '13800000039', 'employee', '段强', 'duanqiang@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (40, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0036', '', '', 0, 1, '2024-04-20 00:00:00.000000', '13800000040', 'employee', '武娜', 'wuna@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (41, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0037', '', '', 0, 1, '2024-05-05 00:00:00.000000', '13800000041', 'employee', '贺鹏', 'hepeng@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (42, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0038', '', '', 0, 1, '2024-05-15 00:00:00.000000', '13800000042', 'employee', '康芳', 'kangfang@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (43, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0039', '', '', 0, 1, '2024-06-01 00:00:00.000000', '13800000043', 'employee', '姚磊', 'yaolei@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (44, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0040', '', '', 0, 1, '2024-06-10 00:00:00.000000', '13800000044', 'employee', '姜莉', 'jiangli@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (45, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0041', '', '', 0, 1, '2024-02-01 00:00:00.000000', '13800000045', 'employee', '范明', 'fanming@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (46, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0042', '', '', 0, 1, '2024-03-01 00:00:00.000000', '13800000046', 'employee', '丁倩', 'dingqian@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (47, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0043', '', '', 0, 1, '2024-04-01 00:00:00.000000', '13800000047', 'employee', '魏强', 'weiqiang@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (48, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0044', '', '', 0, 1, '2024-05-01 00:00:00.000000', '13800000048', 'employee', '秦艳', 'qinyan@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (49, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0045', '', '', 0, 0, '2024-06-01 00:00:00.000000', '13800000049', 'employee', '彭鹏', 'pengpeng@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (50, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0046', '', '', 0, 1, '2024-01-10 00:00:00.000000', '13800000050', 'employee', '邵杰', 'shaojie@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (51, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0047', '', '', 0, 1, '2024-02-15 00:00:00.000000', '13800000051', 'employee', '阎丽', 'yanli@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (52, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0048', '', '', 0, 1, '2024-03-01 00:00:00.000000', '13800000052', 'employee', '薛磊', 'xuelei@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (53, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0049', '', '', 0, 1, '2024-03-20 00:00:00.000000', '13800000053', 'employee', '余娜', 'yuna@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (54, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0050', '', '', 0, 1, '2024-04-05 00:00:00.000000', '13800000054', 'employee', '郝鹏', 'haopeng@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (55, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0051', '', '', 0, 1, '2024-04-20 00:00:00.000000', '13800000055', 'employee', '侯芳', 'houfang@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (56, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0052', '', '', 0, 1, '2024-05-05 00:00:00.000000', '13800000056', 'employee', '毛强', 'maoqiang@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (57, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0053', '', '', 0, 1, '2024-05-20 00:00:00.000000', '13800000057', 'employee', '郭倩', 'guoqian@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (58, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0054', '', '', 0, 0, '2024-01-20 00:00:00.000000', '13800000058', 'employee', '戴伟', 'daiwei@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (59, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0055', '', '', 0, 1, '2024-02-10 00:00:00.000000', '13800000059', 'employee', '任莉', 'renli@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (60, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0056', '', '', 0, 1, '2024-02-28 00:00:00.000000', '13800000060', 'employee', '袁明', 'yuanming@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (61, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0057', '', '', 0, 1, '2024-03-15 00:00:00.000000', '13800000061', 'employee', '金艳', 'jinyan@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (62, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0058', '', '', 0, 1, '2024-04-01 00:00:00.000000', '13800000062', 'employee', '戚强', 'qiqiang@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (63, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0059', '', '', 0, 1, '2024-04-15 00:00:00.000000', '13800000063', 'employee', '谢娜', 'xiena@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (64, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0060', '', '', 0, 1, '2024-04-30 00:00:00.000000', '13800000064', 'employee', '喻鹏', 'yupeng@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (65, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0061', '', '', 0, 1, '2024-05-10 00:00:00.000000', '13800000065', 'employee', '柏芳', 'baifang@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (66, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0062', '', '', 0, 1, '2024-05-25 00:00:00.000000', '13800000066', 'employee', '丛强', 'congqiang@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (67, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0063', '', '', 0, 1, '2024-06-05 00:00:00.000000', '13800000067', 'employee', '赖倩', 'laiqian@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (68, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0064', '', '', 0, 0, '2024-02-01 00:00:00.000000', '13800000068', 'employee', '葛伟', 'gewei@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (69, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0065', '', '', 0, 1, '2024-02-20 00:00:00.000000', '13800000069', 'employee', '瞿莉', 'quli@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (70, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0066', '', '', 0, 1, '2024-03-10 00:00:00.000000', '13800000070', 'employee', '童明', 'tongming@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (71, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0067', '', '', 0, 1, '2024-03-25 00:00:00.000000', '13800000071', 'employee', '向艳', 'xiangyan@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (72, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0068', '', '', 0, 1, '2024-04-10 00:00:00.000000', '13800000072', 'employee', '卜强', 'buqiang@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (73, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0069', '', '', 0, 1, '2024-04-25 00:00:00.000000', '13800000073', 'employee', '燕娜', 'yanna@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (74, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0070', '', '', 0, 1, '2024-05-05 00:00:00.000000', '13800000074', 'employee', '门鹏', 'menpeng@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (75, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0071', '', '', 0, 1, '2024-05-20 00:00:00.000000', '13800000075', 'employee', '农芳', 'nongfang@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (76, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0072', '', '', 0, 0, '2024-01-15 00:00:00.000000', '13800000076', 'employee', '苍伟', 'cangwei@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (77, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0073', '', '', 0, 1, '2024-02-01 00:00:00.000000', '13800000077', 'employee', '樊莉', 'fanli@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (78, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0074', '', '', 0, 1, '2024-02-20 00:00:00.000000', '13800000078', 'employee', '利明', 'liming@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (79, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0075', '', '', 0, 1, '2024-03-10 00:00:00.000000', '13800000079', 'employee', '贵艳', 'guiyan@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (80, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0076', '', '', 0, 1, '2024-03-25 00:00:00.000000', '13800000080', 'employee', '农强', 'nongqiang@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (81, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0077', '', '', 0, 1, '2024-04-05 00:00:00.000000', '13800000081', 'employee', '凡娜', 'fanna@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (82, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0078', '', '', 0, 1, '2024-04-20 00:00:00.000000', '13800000082', 'employee', '黎鹏', 'lipeng@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (83, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0079', '', '', 0, 1, '2024-05-05 00:00:00.000000', '13800000083', 'employee', '苗芳', 'miaofang@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (84, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0080', '', '', 0, 1, '2024-01-20 00:00:00.000000', '13800000084', 'employee', '禹伟', 'yuwei@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (85, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0081', '', '', 0, 1, '2024-02-15 00:00:00.000000', '13800000085', 'employee', '巴莉', 'bali@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (86, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0082', '', '', 0, 1, '2024-03-01 00:00:00.000000', '13800000086', 'employee', '蒙明', 'mengming@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (87, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0083', '', '', 0, 1, '2024-03-20 00:00:00.000000', '13800000087', 'employee', '泉艳', 'quanyan@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (88, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0084', '', '', 0, 1, '2024-04-10 00:00:00.000000', '13800000088', 'employee', '敬强', 'jingqiang@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (89, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0085', '', '', 0, 1, '2024-02-01 00:00:00.000000', '13800000089', 'employee', '湛伟', 'zhanwei@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (90, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0086', '', '', 0, 1, '2024-03-01 00:00:00.000000', '13800000090', 'employee', '晏莉', 'yanli2@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (91, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0087', '', '', 0, 1, '2024-06-01 00:00:00.000000', '13800000091', 'employee', '巩伟', 'gongwei@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (92, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0088', '', '', 0, 1, '2024-06-05 00:00:00.000000', '13800000092', 'employee', '仲莉', 'zhongli@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (93, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0089', '', '', 0, 1, '2024-06-10 00:00:00.000000', '13800000093', 'employee', '毕明', 'biming@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (94, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0090', '', '', 0, 1, '2024-06-15 00:00:00.000000', '13800000094', 'employee', '景艳', 'jingyan@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (95, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0091', '', '', 0, 1, '2024-06-20 00:00:00.000000', '13800000095', 'employee', '晏强', 'yanqiang@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (96, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0092', '', '', 0, 1, '2024-06-25 00:00:00.000000', '13800000096', 'employee', '诸娜', 'zhuna@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (97, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0093', '', '', 0, 1, '2024-06-28 00:00:00.000000', '13800000097', 'employee', '屠鹏', 'tupeng@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (98, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0094', '', '', 0, 1, '2024-06-30 00:00:00.000000', '13800000098', 'employee', '鞠芳', 'jufang@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (99, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', '2026-01-24 16:10:19.000000', 0, 'emp0095', '', '', 0, 1, '2024-07-01 00:00:00.000000', '13800000099', 'employee', '仰伟', 'yangwei@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (100, 'pbkdf2_sha256$1000000$lOIncR9jA2MJEekyudOSDO$7lK14sVM4WrLkfuuT+1RQCRMzA02fO3YLKKTzV11MZ0=', '2026-01-24 16:10:19.000000', 0, 'emp0096', '', '', 0, 1, '2024-07-05 00:00:00.000000', '13800000100', 'hr', '麦莉', 'maili@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (101, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0101', '', '', 0, 1, '2025-07-01 00:00:00.000000', '13900000101', 'employee', '新研发A', 'xinfa@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (102, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0102', '', '', 0, 1, '2025-07-15 00:00:00.000000', '13900000102', 'employee', '新研发B', 'xinfb@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (103, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0103', '', '', 0, 1, '2025-08-01 00:00:00.000000', '13900000103', 'employee', '新研发C', 'xinfc@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (104, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0104', '', '', 0, 1, '2025-09-01 00:00:00.000000', '13900000104', 'employee', '新研发D', 'xinfd@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (105, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0105', '', '', 0, 1, '2025-10-01 00:00:00.000000', '13900000105', 'employee', '新研发E', 'xinfe@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (106, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0106', '', '', 0, 1, '2025-11-01 00:00:00.000000', '13900000106', 'employee', '新研发F', 'xinff@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (107, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0107', '', '', 0, 1, '2025-12-01 00:00:00.000000', '13900000107', 'employee', '新研发G', 'xinfg@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (108, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0108', '', '', 0, 1, '2026-01-05 00:00:00.000000', '13900000108', 'employee', '新研发H', 'xinfh@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (109, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0109', '', '', 0, 1, '2025-07-10 00:00:00.000000', '13900000109', 'employee', '新产品A', 'xinprda@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (110, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0110', '', '', 0, 1, '2025-09-15 00:00:00.000000', '13900000110', 'employee', '新产品B', 'xinprdb@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (111, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0111', '', '', 0, 1, '2025-11-01 00:00:00.000000', '13900000111', 'employee', '新产品C', 'xinprdc@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (112, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0112', '', '', 0, 1, '2025-08-01 00:00:00.000000', '13900000112', 'employee', '新市场A', 'xinmkta@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (113, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0113', '', '', 0, 1, '2025-10-01 00:00:00.000000', '13900000113', 'employee', '新市场B', 'xinmktb@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (114, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0114', '', '', 0, 1, '2025-07-20 00:00:00.000000', '13900000114', 'employee', '新运营A', 'xinopsa@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (115, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0115', '', '', 0, 1, '2025-12-01 00:00:00.000000', '13900000115', 'employee', '新运营B', 'xinopsb@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (116, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0116', '', '', 0, 1, '2025-09-01 00:00:00.000000', '13900000116', 'employee', '新设计A', 'xindesa@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (117, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0117', '', '', 0, 1, '2025-08-15 00:00:00.000000', '13900000117', 'employee', '新财务A', 'xinfina@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (118, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'song芳0111', '', '', 0, 1, '2026-01-13 00:00:00.000000', '13956041258', 'employee', '宋芳', 'song芳0111@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (119, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'lv金0211', '', '', 0, 1, '2025-12-26 00:00:00.000000', '13802970771', 'employee', '吕金凤', 'lv金0211@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (120, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'he军0284', '', '', 0, 1, '2026-01-04 00:00:00.000000', '18845400364', 'employee', '何军', 'he军0284@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (121, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'guo龙0265', '', '', 0, 1, '2026-01-13 00:00:00.000000', '18616863912', 'employee', '郭龙', 'guo龙0265@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (122, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'li芳0137', '', '', 0, 1, '2026-01-17 00:00:00.000000', '15085026725', 'employee', '李芳', 'li芳0137@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (123, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'guo芳0232', '', '', 0, 1, '2026-01-14 00:00:00.000000', '15764212140', 'employee', '郭芳', 'guo芳0232@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (124, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'yao磊0319', '', '', 0, 1, '2025-12-27 00:00:00.000000', '15017448827', 'employee', '姚磊', 'yao磊0319@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (125, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'lv玉0110', '', '', 0, 1, '2026-01-19 00:00:00.000000', '18920299429', 'employee', '吕玉兰', 'lv玉0110@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (126, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'shen芬0170', '', '', 0, 1, '2026-01-17 00:00:00.000000', '15267064615', 'employee', '沈芬', 'shen芬0170@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (127, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'lin华0279', '', '', 0, 1, '2025-12-31 00:00:00.000000', '15729273850', 'employee', '林华', 'lin华0279@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (128, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'cai涛0214', '', '', 0, 1, '2026-01-24 00:00:00.000000', '13945502923', 'employee', '蔡涛', 'cai涛0214@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (129, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'lv玉0140', '', '', 0, 1, '2025-12-27 00:00:00.000000', '15898954393', 'employee', '吕玉兰', 'lv玉0140@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (130, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhong平0174', '', '', 0, 1, '2026-01-09 00:00:00.000000', '18823370756', 'employee', '钟平', 'zhong平0174@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (131, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'xie明0102', '', '', 0, 1, '2025-12-27 00:00:00.000000', '18711913447', 'employee', '谢明', 'xie明0102@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (132, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'ma桂0380', '', '', 0, 1, '2026-01-20 00:00:00.000000', '15790538016', 'employee', '马桂英', 'ma桂0380@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (133, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'wang飞0120', '', '', 0, 1, '2026-01-05 00:00:00.000000', '18773438597', 'employee', '汪飞翔', 'wang飞0120@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (134, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'wu桂0135', '', '', 0, 1, '2026-01-11 00:00:00.000000', '15709855709', 'employee', '吴桂英', 'wu桂0135@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (135, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'hu勇0228', '', '', 0, 1, '2026-01-20 00:00:00.000000', '18784961879', 'employee', '胡勇', 'hu勇0228@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (136, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'guo丽0109', '', '', 0, 1, '2026-01-17 00:00:00.000000', '18828974179', 'employee', '郭丽', 'guo丽0109@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (137, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhong刚0272', '', '', 0, 1, '2025-12-28 00:00:00.000000', '15132132328', 'employee', '钟刚', 'zhong刚0272@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (138, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, '任玉0149', '', '', 0, 1, '2026-01-23 00:00:00.000000', '15891390779', 'employee', '任玉兰', '任玉0149@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (139, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'cui飞0305', '', '', 0, 1, '2026-01-08 00:00:00.000000', '15034664250', 'employee', '崔飞', 'cui飞0305@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (140, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'lu玉0352', '', '', 0, 1, '2025-12-29 00:00:00.000000', '15811374864', 'employee', '陆玉兰', 'lu玉0352@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (141, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhang红0326', '', '', 0, 1, '2025-12-28 00:00:00.000000', '15766630793', 'employee', '张红', 'zhang红0326@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (142, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'yuan金0201', '', '', 0, 1, '2026-01-22 00:00:00.000000', '18842719276', 'employee', '袁金凤', 'yuan金0201@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (143, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'liang红0360', '', '', 0, 1, '2025-12-30 00:00:00.000000', '15756427803', 'employee', '梁红', 'liang红0360@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (144, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'gao敏0135', '', '', 0, 1, '2025-12-27 00:00:00.000000', '15814501178', 'employee', '高敏', 'gao敏0135@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (145, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'wang华0335', '', '', 0, 1, '2026-01-04 00:00:00.000000', '15873553138', 'employee', '王华', 'wang华0335@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (146, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'yu建0246', '', '', 0, 1, '2026-01-16 00:00:00.000000', '15799916025', 'employee', '于建', 'yu建0246@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (147, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'su芳0389', '', '', 0, 1, '2026-01-14 00:00:00.000000', '15141183262', 'employee', '苏芳', 'su芳0389@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (148, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'lin强0111', '', '', 0, 1, '2026-01-25 00:00:00.000000', '15226803426', 'employee', '林强', 'lin强0111@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (149, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'lin超0379', '', '', 0, 1, '2026-01-12 00:00:00.000000', '15044068924', 'employee', '林超', 'lin超0379@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (150, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'sun春0270', '', '', 0, 1, '2026-01-08 00:00:00.000000', '18893260884', 'employee', '孙春', 'sun春0270@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (151, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'yang芳0111', '', '', 0, 1, '2026-01-01 00:00:00.000000', '15897400318', 'employee', '杨芳', 'yang芳0111@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (152, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'dong娜0329', '', '', 0, 1, '2026-01-02 00:00:00.000000', '15138456395', 'employee', '董娜', 'dong娜0329@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (153, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'pan丽0371', '', '', 0, 1, '2026-01-09 00:00:00.000000', '18919428455', 'employee', '潘丽', 'pan丽0371@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (154, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'yao红0317', '', '', 0, 1, '2026-01-22 00:00:00.000000', '18706052372', 'employee', '姚红梅', 'yao红0317@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (155, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhou国0213', '', '', 0, 1, '2026-01-11 00:00:00.000000', '18974973073', 'employee', '周国', 'zhou国0213@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (156, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'deng明0212', '', '', 0, 1, '2026-01-03 00:00:00.000000', '13985721431', 'employee', '邓明', 'deng明0212@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (157, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'su秀0380', '', '', 0, 1, '2026-01-17 00:00:00.000000', '15000313453', 'employee', '苏秀英', 'su秀0380@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (158, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'fan秀0306', '', '', 0, 1, '2025-12-28 00:00:00.000000', '18986171967', 'employee', '范秀兰', 'fan秀0306@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (159, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'lu红0320', '', '', 0, 1, '2026-01-13 00:00:00.000000', '18835895923', 'employee', '卢红', 'lu红0320@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (160, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'ding刚0369', '', '', 0, 1, '2025-12-29 00:00:00.000000', '15258240136', 'employee', '丁刚', 'ding刚0369@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (161, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'guo金0292', '', '', 0, 1, '2026-01-25 00:00:00.000000', '15907371370', 'employee', '郭金凤', 'guo金0292@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (162, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'lu勇0288', '', '', 0, 1, '2026-01-18 00:00:00.000000', '15178593325', 'employee', '陆勇', 'lu勇0288@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (163, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'ye秀0266', '', '', 0, 1, '2025-12-30 00:00:00.000000', '15055047326', 'employee', '叶秀兰', 'ye秀0266@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (164, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'lu娜0345', '', '', 0, 1, '2026-01-21 00:00:00.000000', '15766560463', 'employee', '卢娜', 'lu娜0345@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (165, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'cheng飞0311', '', '', 0, 1, '2026-01-22 00:00:00.000000', '15095023952', 'employee', '程飞翔', 'cheng飞0311@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (166, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'xu洋0244', '', '', 0, 1, '2026-01-09 00:00:00.000000', '18718712770', 'employee', '许洋', 'xu洋0244@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (167, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'yao敏0329', '', '', 0, 1, '2026-01-04 00:00:00.000000', '18632850349', 'employee', '姚敏', 'yao敏0329@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (168, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'tian强0393', '', '', 0, 1, '2025-12-28 00:00:00.000000', '15137531450', 'employee', '田强', 'tian强0393@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (169, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'yang华0206', '', '', 0, 1, '2026-01-06 00:00:00.000000', '15868414764', 'employee', '杨华', 'yang华0206@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (170, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'sun鹏0166', '', '', 0, 1, '2026-01-11 00:00:00.000000', '13816597182', 'employee', '孙鹏', 'sun鹏0166@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (171, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'huang洋0152', '', '', 0, 1, '2025-12-28 00:00:00.000000', '15038724739', 'employee', '黄洋', 'huang洋0152@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (172, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'deng小0175', '', '', 0, 1, '2026-01-04 00:00:00.000000', '15904802211', 'employee', '邓小刚', 'deng小0175@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (173, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'tan娜0122', '', '', 0, 1, '2026-01-24 00:00:00.000000', '15781869301', 'employee', '谭娜', 'tan娜0122@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (174, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'liang海0303', '', '', 0, 1, '2025-12-28 00:00:00.000000', '15932912846', 'employee', '梁海燕', 'liang海0303@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (175, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'fu军0231', '', '', 0, 1, '2025-12-26 00:00:00.000000', '15126313346', 'employee', '傅军', 'fu军0231@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (176, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhao飞0240', '', '', 0, 1, '2026-01-22 00:00:00.000000', '18785518692', 'employee', '赵飞翔', 'zhao飞0240@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (177, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'lin磊0110', '', '', 0, 1, '2026-01-02 00:00:00.000000', '15825635576', 'employee', '林磊', 'lin磊0110@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (178, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'fan飞0178', '', '', 0, 1, '2026-01-18 00:00:00.000000', '13929973798', 'employee', '范飞', 'fan飞0178@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (179, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'yang龙0108', '', '', 0, 1, '2026-01-09 00:00:00.000000', '15837495562', 'employee', '杨龙', 'yang龙0108@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (180, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'huang强0173', '', '', 0, 1, '2026-01-04 00:00:00.000000', '15811287000', 'employee', '黄强', 'huang强0173@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (181, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhou娜0152', '', '', 0, 1, '2026-01-25 00:00:00.000000', '15002175925', 'employee', '周娜', 'zhou娜0152@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (182, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'cai勇0208', '', '', 0, 1, '2026-01-13 00:00:00.000000', '18985042921', 'employee', '蔡勇', 'cai勇0208@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (183, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'lu龙0360', '', '', 0, 1, '2026-01-15 00:00:00.000000', '15080322838', 'employee', '陆龙', 'lu龙0360@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (184, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'wang华0370', '', '', 0, 1, '2026-01-24 00:00:00.000000', '18930292106', 'employee', '王华', 'wang华0370@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (185, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'cui芳0332', '', '', 0, 1, '2026-01-01 00:00:00.000000', '15828046732', 'employee', '崔芳', 'cui芳0332@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (186, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, '任刚0138', '', '', 0, 1, '2025-12-30 00:00:00.000000', '13970557131', 'employee', '任刚', '任刚0138@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (187, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'yuan建0390', '', '', 0, 1, '2026-01-12 00:00:00.000000', '13989920220', 'employee', '袁建', 'yuan建0390@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (188, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'deng雪0161', '', '', 0, 1, '2025-12-30 00:00:00.000000', '13945233597', 'employee', '邓雪梅', 'deng雪0161@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (189, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'xiao刚0307', '', '', 0, 1, '2025-12-26 00:00:00.000000', '15128711717', 'employee', '萧刚', 'xiao刚0307@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (190, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'du杰0146', '', '', 0, 1, '2026-01-06 00:00:00.000000', '15961023802', 'employee', '杜杰', 'du杰0146@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (191, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'song飞0159', '', '', 0, 1, '2026-01-18 00:00:00.000000', '18722416843', 'employee', '宋飞', 'song飞0159@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (192, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'han超0209', '', '', 0, 1, '2026-01-01 00:00:00.000000', '18656477274', 'employee', '韩超', 'han超0209@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (193, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'ye海0226', '', '', 0, 1, '2026-01-01 00:00:00.000000', '15299190347', 'employee', '叶海燕', 'ye海0226@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (194, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'yu秀0157', '', '', 0, 1, '2026-01-12 00:00:00.000000', '18936130931', 'employee', '于秀兰', 'yu秀0157@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (195, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'song龙0257', '', '', 0, 1, '2026-01-11 00:00:00.000000', '15208935589', 'employee', '宋龙', 'song龙0257@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (196, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'wu龙0390', '', '', 0, 1, '2026-01-16 00:00:00.000000', '13873872059', 'employee', '吴龙', 'wu龙0390@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (197, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'yu伟0213', '', '', 0, 1, '2026-01-07 00:00:00.000000', '15246009555', 'employee', '余伟', 'yu伟0213@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (198, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'liang涛0319', '', '', 0, 1, '2026-01-09 00:00:00.000000', '15893867804', 'employee', '梁涛', 'liang涛0319@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (199, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'gao玉0198', '', '', 0, 1, '2026-01-19 00:00:00.000000', '13847728695', 'employee', '高玉兰', 'gao玉0198@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (200, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'shen杰0292', '', '', 0, 1, '2026-01-25 00:00:00.000000', '15756933023', 'employee', '沈杰', 'shen杰0292@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (201, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'yuan春0290', '', '', 0, 1, '2025-12-26 00:00:00.000000', '18626240806', 'employee', '袁春', 'yuan春0290@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (202, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, '任杰0296', '', '', 0, 1, '2025-12-31 00:00:00.000000', '15942498666', 'employee', '任杰', '任杰0296@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (203, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'shen龙0231', '', '', 0, 1, '2026-01-18 00:00:00.000000', '18690379039', 'employee', '沈龙', 'shen龙0231@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (204, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'su芬0342', '', '', 0, 1, '2026-01-19 00:00:00.000000', '18955162423', 'employee', '苏芬', 'su芬0342@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (205, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhu红0191', '', '', 0, 1, '2026-01-02 00:00:00.000000', '18803764895', 'employee', '朱红梅', 'zhu红0191@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (206, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'pan红0249', '', '', 0, 1, '2026-01-24 00:00:00.000000', '15136515364', 'employee', '潘红', 'pan红0249@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (207, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'huang洋0262', '', '', 0, 1, '2026-01-01 00:00:00.000000', '15147856171', 'employee', '黄洋', 'huang洋0262@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (208, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'ma磊0340', '', '', 0, 1, '2025-12-26 00:00:00.000000', '15954464966', 'employee', '马磊', 'ma磊0340@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (209, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'deng静0154', '', '', 0, 1, '2026-01-20 00:00:00.000000', '18988541150', 'employee', '邓静', 'deng静0154@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (210, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'liu强0389', '', '', 0, 1, '2026-01-16 00:00:00.000000', '15929046559', 'employee', '刘强', 'liu强0389@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (211, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'ye艳0303', '', '', 0, 1, '2026-01-01 00:00:00.000000', '13940805490', 'employee', '叶艳', 'ye艳0303@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (212, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'wang磊0302', '', '', 0, 1, '2026-01-20 00:00:00.000000', '18838249053', 'employee', '汪磊', 'wang磊0302@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (213, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'guo国0307', '', '', 0, 1, '2026-01-01 00:00:00.000000', '15226655727', 'employee', '郭国', 'guo国0307@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (214, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'ma春0103', '', '', 0, 1, '2025-12-31 00:00:00.000000', '15157419128', 'employee', '马春', 'ma春0103@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (215, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'wu春0294', '', '', 0, 1, '2026-01-22 00:00:00.000000', '13957916923', 'employee', '吴春', 'wu春0294@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (216, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'yuan刚0297', '', '', 0, 1, '2025-12-30 00:00:00.000000', '18874383157', 'employee', '袁刚', 'yuan刚0297@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (217, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'ma刚0319', '', '', 0, 1, '2026-01-02 00:00:00.000000', '18921812819', 'employee', '马刚', 'ma刚0319@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (218, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'wei桂0352', '', '', 0, 1, '2025-12-30 00:00:00.000000', '15127061459', 'employee', '魏桂英', 'wei桂0352@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (219, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'xiao鹏0330', '', '', 0, 1, '2026-01-01 00:00:00.000000', '18897650283', 'employee', '萧鹏', 'xiao鹏0330@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (220, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhao飞0388', '', '', 0, 1, '2026-01-03 00:00:00.000000', '15238157694', 'employee', '赵飞翔', 'zhao飞0388@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (221, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'gao静0203', '', '', 0, 1, '2026-01-17 00:00:00.000000', '18907487808', 'employee', '高静', 'gao静0203@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (222, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'yu洋0254', '', '', 0, 1, '2026-01-14 00:00:00.000000', '13878978874', 'employee', '余洋', 'yu洋0254@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (223, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'wang红0115', '', '', 0, 1, '2025-12-27 00:00:00.000000', '15006669428', 'employee', '汪红梅', 'wang红0115@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (224, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'lv敏0110', '', '', 0, 1, '2026-01-13 00:00:00.000000', '15292096264', 'employee', '吕敏', 'lv敏0110@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (225, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'lu明0262', '', '', 0, 1, '2026-01-16 00:00:00.000000', '15791698625', 'employee', '卢明', 'lu明0262@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (226, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'lv春0115', '', '', 0, 1, '2026-01-25 00:00:00.000000', '18919485094', 'employee', '吕春', 'lv春0115@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (227, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'huang超0256', '', '', 0, 1, '2026-01-02 00:00:00.000000', '15797763328', 'employee', '黄超', 'huang超0256@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (228, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'jiang洋0387', '', '', 0, 1, '2025-12-30 00:00:00.000000', '15054837149', 'employee', '蒋洋', 'jiang洋0387@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (229, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'shen秀0307', '', '', 0, 1, '2026-01-24 00:00:00.000000', '15193137047', 'employee', '沈秀兰', 'shen秀0307@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (230, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'lu小0177', '', '', 0, 1, '2025-12-26 00:00:00.000000', '15274330366', 'employee', '陆小刚', 'lu小0177@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (231, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'yu芳0120', '', '', 0, 1, '2025-12-26 00:00:00.000000', '15905993110', 'employee', '余芳', 'yu芳0120@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (232, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'deng飞0128', '', '', 0, 1, '2026-01-09 00:00:00.000000', '18828532452', 'employee', '邓飞', 'deng飞0128@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (233, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'luo国0308', '', '', 0, 1, '2026-01-11 00:00:00.000000', '15860015908', 'employee', '罗国', 'luo国0308@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (234, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'dong飞0123', '', '', 0, 1, '2025-12-29 00:00:00.000000', '15771902828', 'employee', '董飞翔', 'dong飞0123@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (235, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'yu桂0209', '', '', 0, 1, '2026-01-11 00:00:00.000000', '18661163295', 'employee', '余桂英', 'yu桂0209@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (236, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'jiang雪0125', '', '', 0, 1, '2026-01-14 00:00:00.000000', '15897621478', 'employee', '姜雪梅', 'jiang雪0125@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (237, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, '任金0303', '', '', 0, 1, '2026-01-04 00:00:00.000000', '18847588024', 'employee', '任金凤', '任金0303@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (238, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhao伟0210', '', '', 0, 1, '2026-01-07 00:00:00.000000', '15013784533', 'employee', '赵伟', 'zhao伟0210@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (239, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'tian秀0305', '', '', 0, 1, '2026-01-24 00:00:00.000000', '15012927973', 'employee', '田秀英', 'tian秀0305@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (240, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'wu刚0116', '', '', 0, 1, '2026-01-01 00:00:00.000000', '15828366529', 'employee', '吴刚', 'wu刚0116@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (241, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'fan建0304', '', '', 0, 1, '2026-01-11 00:00:00.000000', '15884828541', 'employee', '范建', 'fan建0304@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (242, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'pan芳0176', '', '', 0, 1, '2026-01-02 00:00:00.000000', '15291234605', 'employee', '潘芳', 'pan芳0176@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (243, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhu静0300', '', '', 0, 1, '2026-01-07 00:00:00.000000', '18868652024', 'employee', '朱静', 'zhu静0300@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (244, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'he秀0212', '', '', 0, 1, '2026-01-01 00:00:00.000000', '13956846594', 'employee', '何秀英', 'he秀0212@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (245, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'jiang霞0305', '', '', 0, 1, '2026-01-09 00:00:00.000000', '18885875759', 'employee', '姜霞', 'jiang霞0305@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (246, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'gao军0276', '', '', 0, 1, '2026-01-21 00:00:00.000000', '15776316959', 'employee', '高军', 'gao军0276@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (247, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'lv杰0138', '', '', 0, 1, '2025-12-30 00:00:00.000000', '18938990148', 'employee', '吕杰', 'lv杰0138@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (248, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'yu飞0135', '', '', 0, 1, '2026-01-01 00:00:00.000000', '15191564184', 'employee', '余飞', 'yu飞0135@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (249, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'tang芬0292', '', '', 0, 1, '2026-01-20 00:00:00.000000', '15990774300', 'employee', '唐芬', 'tang芬0292@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (250, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'chen霞0224', '', '', 0, 1, '2025-12-28 00:00:00.000000', '13803035858', 'employee', '陈霞', 'chen霞0224@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (251, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'yang涛0298', '', '', 0, 1, '2026-01-09 00:00:00.000000', '15047562711', 'employee', '杨涛', 'yang涛0298@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (252, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'li刚0259', '', '', 0, 1, '2026-01-02 00:00:00.000000', '18825621611', 'employee', '李刚', 'li刚0259@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (253, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'wang鹏0292', '', '', 0, 1, '2026-01-06 00:00:00.000000', '13868540868', 'employee', '王鹏', 'wang鹏0292@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (254, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhao超0132', '', '', 0, 1, '2025-12-29 00:00:00.000000', '18990927577', 'employee', '赵超', 'zhao超0132@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (255, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'song华0378', '', '', 0, 1, '2026-01-03 00:00:00.000000', '15741911279', 'employee', '宋华', 'song华0378@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (256, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'chen军0380', '', '', 0, 1, '2026-01-08 00:00:00.000000', '18974139905', 'employee', '陈军', 'chen军0380@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (257, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'han芳0348', '', '', 0, 1, '2025-12-29 00:00:00.000000', '15995617886', 'employee', '韩芳', 'han芳0348@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (258, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'tan涛0297', '', '', 0, 1, '2026-01-25 00:00:00.000000', '18641957604', 'employee', '谭涛', 'tan涛0297@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (259, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'xu红0270', '', '', 0, 1, '2026-01-22 00:00:00.000000', '15813412639', 'employee', '许红梅', 'xu红0270@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (260, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'gao超0372', '', '', 0, 1, '2025-12-26 00:00:00.000000', '13851229786', 'employee', '高超', 'gao超0372@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (261, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'tian伟0198', '', '', 0, 1, '2025-12-29 00:00:00.000000', '18910647785', 'employee', '田伟', 'tian伟0198@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (262, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'hu华0329', '', '', 0, 1, '2025-12-27 00:00:00.000000', '15112999507', 'employee', '胡华', 'hu华0329@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (263, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhang芬0191', '', '', 0, 1, '2025-12-29 00:00:00.000000', '15809272309', 'employee', '张芬', 'zhang芬0191@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (264, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'du霞0324', '', '', 0, 1, '2025-12-26 00:00:00.000000', '15051676245', 'employee', '杜霞', 'du霞0324@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (265, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'sun强0262', '', '', 0, 1, '2026-01-09 00:00:00.000000', '15736648699', 'employee', '孙强', 'sun强0262@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (266, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'feng华0379', '', '', 0, 1, '2026-01-17 00:00:00.000000', '15258920584', 'employee', '冯华', 'feng华0379@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (267, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'lu桂0257', '', '', 0, 1, '2026-01-23 00:00:00.000000', '15824795725', 'employee', '卢桂英', 'lu桂0257@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (268, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'su海0283', '', '', 0, 1, '2026-01-15 00:00:00.000000', '15974281836', 'employee', '苏海燕', 'su海0283@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (269, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'cao强0295', '', '', 0, 1, '2026-01-24 00:00:00.000000', '13926372575', 'employee', '曹强', 'cao强0295@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (270, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'lv勇0380', '', '', 0, 1, '2026-01-12 00:00:00.000000', '18614694965', 'employee', '吕勇', 'lv勇0380@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (271, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'wu玉0325', '', '', 0, 1, '2026-01-07 00:00:00.000000', '15186474585', 'employee', '吴玉兰', 'wu玉0325@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (272, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'shen丽0326', '', '', 0, 1, '2026-01-09 00:00:00.000000', '15800789298', 'employee', '沈丽', 'shen丽0326@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (273, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhang静0328', '', '', 0, 1, '2025-12-31 00:00:00.000000', '18602956191', 'employee', '张静', 'zhang静0328@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (274, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'wu国0280', '', '', 0, 1, '2025-12-27 00:00:00.000000', '18901642267', 'employee', '吴国', 'wu国0280@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (275, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'lin小0237', '', '', 0, 1, '2026-01-05 00:00:00.000000', '15076151583', 'employee', '林小刚', 'lin小0237@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (276, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'huang伟0247', '', '', 0, 1, '2025-12-29 00:00:00.000000', '18820053802', 'employee', '黄伟', 'huang伟0247@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (277, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhu敏0147', '', '', 0, 1, '2026-01-07 00:00:00.000000', '15747118501', 'employee', '朱敏', 'zhu敏0147@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (278, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'yang涛0111', '', '', 0, 1, '2025-12-26 00:00:00.000000', '15206194383', 'employee', '杨涛', 'yang涛0111@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (279, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'guo飞0317', '', '', 0, 1, '2026-01-03 00:00:00.000000', '13847015531', 'employee', '郭飞', 'guo飞0317@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (280, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'sun国0266', '', '', 0, 1, '2026-01-22 00:00:00.000000', '13837637719', 'employee', '孙国', 'sun国0266@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (281, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'peng飞0380', '', '', 0, 1, '2025-12-31 00:00:00.000000', '18923887796', 'employee', '彭飞翔', 'peng飞0380@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (282, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'tan红0177', '', '', 0, 1, '2026-01-16 00:00:00.000000', '15751489503', 'employee', '谭红梅', 'tan红0177@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (283, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, '任强0233', '', '', 0, 1, '2026-01-13 00:00:00.000000', '18866741342', 'employee', '任强', '任强0233@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (284, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'pan勇0296', '', '', 0, 1, '2026-01-22 00:00:00.000000', '18924175538', 'employee', '潘勇', 'pan勇0296@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (285, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'fu金0111', '', '', 0, 1, '2025-12-26 00:00:00.000000', '13852875351', 'employee', '傅金凤', 'fu金0111@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (286, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'wei伟0246', '', '', 0, 1, '2026-01-05 00:00:00.000000', '15139148473', 'employee', '魏伟', 'wei伟0246@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (287, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhang丽0223', '', '', 0, 1, '2026-01-18 00:00:00.000000', '15926951022', 'employee', '张丽', 'zhang丽0223@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (288, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'han海0290', '', '', 0, 1, '2026-01-24 00:00:00.000000', '13835852196', 'employee', '韩海燕', 'han海0290@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (289, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'fan桂0366', '', '', 0, 1, '2025-12-31 00:00:00.000000', '13833165142', 'employee', '范桂英', 'fan桂0366@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (290, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'su磊0183', '', '', 0, 1, '2026-01-14 00:00:00.000000', '15866865461', 'employee', '苏磊', 'su磊0183@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (291, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'huang伟0101', '', '', 0, 1, '2026-01-04 00:00:00.000000', '13830375310', 'employee', '黄伟', 'huang伟0101@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (292, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'hu玉0171', '', '', 0, 1, '2026-01-24 00:00:00.000000', '15153374183', 'employee', '胡玉兰', 'hu玉0171@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (293, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'yang金0177', '', '', 0, 1, '2026-01-09 00:00:00.000000', '18845529127', 'employee', '杨金凤', 'yang金0177@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (294, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'gao平0335', '', '', 0, 1, '2026-01-20 00:00:00.000000', '15298269208', 'employee', '高平', 'gao平0335@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (295, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'ye文0369', '', '', 0, 1, '2026-01-05 00:00:00.000000', '18993743312', 'employee', '叶文', 'ye文0369@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (296, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'lv华0101', '', '', 0, 1, '2026-01-18 00:00:00.000000', '18751017662', 'employee', '吕华', 'lv华0101@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (297, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, '任桂0309', '', '', 0, 1, '2026-01-14 00:00:00.000000', '15205008745', 'employee', '任桂英', '任桂0309@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (298, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'wei红0180', '', '', 0, 1, '2026-01-01 00:00:00.000000', '15252775211', 'employee', '魏红梅', 'wei红0180@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (299, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'jiang文0234', '', '', 0, 1, '2026-01-13 00:00:00.000000', '15928896039', 'employee', '姜文', 'jiang文0234@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (300, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'huang磊0202', '', '', 0, 1, '2026-01-25 00:00:00.000000', '15162907190', 'employee', '黄磊', 'huang磊0202@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (301, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'lu明0167', '', '', 0, 1, '2026-01-15 00:00:00.000000', '15215524062', 'employee', '陆明', 'lu明0167@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (302, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhong国0102', '', '', 0, 1, '2026-01-05 00:00:00.000000', '18995076540', 'employee', '钟国', 'zhong国0102@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (303, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'wang春0184', '', '', 0, 1, '2026-01-21 00:00:00.000000', '18803034732', 'employee', '汪春', 'wang春0184@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (304, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'deng杰0349', '', '', 0, 1, '2026-01-03 00:00:00.000000', '15909513751', 'employee', '邓杰', 'deng杰0349@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (305, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'xu华0234', '', '', 0, 1, '2026-01-05 00:00:00.000000', '13906870329', 'employee', '许华', 'xu华0234@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (306, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'yuan金0336', '', '', 0, 1, '2026-01-17 00:00:00.000000', '15822041724', 'employee', '袁金凤', 'yuan金0336@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (307, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zeng洋0180', '', '', 0, 1, '2026-01-17 00:00:00.000000', '18624669306', 'employee', '曾洋', 'zeng洋0180@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (308, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'jiang金0117', '', '', 0, 1, '2025-12-29 00:00:00.000000', '18972609541', 'employee', '姜金凤', 'jiang金0117@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (309, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'han龙0339', '', '', 0, 1, '2026-01-03 00:00:00.000000', '15228825012', 'employee', '韩龙', 'han龙0339@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (310, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'lin文0226', '', '', 0, 1, '2026-01-17 00:00:00.000000', '15849248365', 'employee', '林文', 'lin文0226@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (311, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, '任秀0204', '', '', 0, 1, '2026-01-08 00:00:00.000000', '15789251013', 'employee', '任秀英', '任秀0204@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (312, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'jiang国0316', '', '', 0, 1, '2026-01-10 00:00:00.000000', '13902694508', 'employee', '蒋国', 'jiang国0316@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (313, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'jiang强0158', '', '', 0, 1, '2026-01-07 00:00:00.000000', '13892934929', 'employee', '姜强', 'jiang强0158@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (314, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'tian娜0255', '', '', 0, 1, '2026-01-25 00:00:00.000000', '13965375164', 'employee', '田娜', 'tian娜0255@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (315, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'song勇0217', '', '', 0, 1, '2026-01-20 00:00:00.000000', '18736164188', 'employee', '宋勇', 'song勇0217@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (316, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zeng桂0141', '', '', 0, 1, '2026-01-24 00:00:00.000000', '15820460395', 'employee', '曾桂英', 'zeng桂0141@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (317, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'wang雪0238', '', '', 0, 1, '2026-01-23 00:00:00.000000', '15188311481', 'employee', '汪雪梅', 'wang雪0238@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (318, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'lu飞0271', '', '', 0, 1, '2025-12-28 00:00:00.000000', '15063481481', 'employee', '陆飞翔', 'lu飞0271@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (319, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'ding桂0376', '', '', 0, 1, '2026-01-08 00:00:00.000000', '18917689612', 'employee', '丁桂英', 'ding桂0376@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (320, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'dong红0116', '', '', 0, 1, '2026-01-16 00:00:00.000000', '15106859575', 'employee', '董红梅', 'dong红0116@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (321, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'song强0191', '', '', 0, 1, '2026-01-10 00:00:00.000000', '13991873661', 'employee', '宋强', 'song强0191@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (322, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'huang明0173', '', '', 0, 1, '2026-01-07 00:00:00.000000', '15996946660', 'employee', '黄明', 'huang明0173@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (323, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'yuan娜0213', '', '', 0, 1, '2026-01-14 00:00:00.000000', '18618548942', 'employee', '袁娜', 'yuan娜0213@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (324, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'yu雪0105', '', '', 0, 1, '2026-01-04 00:00:00.000000', '15945070712', 'employee', '于雪梅', 'yu雪0105@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (325, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'yu涛0172', '', '', 0, 1, '2026-01-05 00:00:00.000000', '13913759766', 'employee', '于涛', 'yu涛0172@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (326, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, '任霞0321', '', '', 0, 1, '2026-01-11 00:00:00.000000', '18781235104', 'employee', '任霞', '任霞0321@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (327, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'su强0209', '', '', 0, 1, '2026-01-24 00:00:00.000000', '18639480135', 'employee', '苏强', 'su强0209@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (328, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'du华0267', '', '', 0, 1, '2026-01-01 00:00:00.000000', '13870979684', 'employee', '杜华', 'du华0267@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (329, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'cao娜0238', '', '', 0, 1, '2026-01-25 00:00:00.000000', '18660430148', 'employee', '曹娜', 'cao娜0238@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (330, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'lin秀0339', '', '', 0, 1, '2026-01-06 00:00:00.000000', '15877226437', 'employee', '林秀兰', 'lin秀0339@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (331, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'wang国0369', '', '', 0, 1, '2026-01-07 00:00:00.000000', '15989678466', 'employee', '王国', 'wang国0369@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (332, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'lv洋0278', '', '', 0, 1, '2026-01-19 00:00:00.000000', '13980498536', 'employee', '吕洋', 'lv洋0278@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (333, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'xu霞0193', '', '', 0, 1, '2026-01-03 00:00:00.000000', '18625699388', 'employee', '许霞', 'xu霞0193@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (334, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'xu小0183', '', '', 0, 1, '2026-01-10 00:00:00.000000', '15743654954', 'employee', '许小刚', 'xu小0183@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (335, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'yang刚0373', '', '', 0, 1, '2025-12-30 00:00:00.000000', '15040661145', 'employee', '杨刚', 'yang刚0373@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (336, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'lin勇0273', '', '', 0, 1, '2026-01-04 00:00:00.000000', '18722599723', 'employee', '林勇', 'lin勇0273@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (337, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'yao刚0341', '', '', 0, 1, '2026-01-12 00:00:00.000000', '15159382321', 'employee', '姚刚', 'yao刚0341@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (338, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'tan磊0176', '', '', 0, 1, '2026-01-10 00:00:00.000000', '15939717307', 'employee', '谭磊', 'tan磊0176@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (339, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'liu秀0257', '', '', 0, 1, '2026-01-03 00:00:00.000000', '18636186430', 'employee', '刘秀兰', 'liu秀0257@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (340, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'cao金0149', '', '', 0, 1, '2025-12-30 00:00:00.000000', '15730636022', 'employee', '曹金凤', 'cao金0149@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (341, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'wang军0168', '', '', 0, 1, '2026-01-09 00:00:00.000000', '13912907227', 'employee', '王军', 'wang军0168@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (342, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'lv娜0105', '', '', 0, 1, '2026-01-10 00:00:00.000000', '15817611114', 'employee', '吕娜', 'lv娜0105@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (343, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhong杰0149', '', '', 0, 1, '2026-01-10 00:00:00.000000', '18888577101', 'employee', '钟杰', 'zhong杰0149@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (344, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zheng玉0313', '', '', 0, 1, '2026-01-17 00:00:00.000000', '15233649493', 'employee', '郑玉兰', 'zheng玉0313@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (345, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'li国0131', '', '', 0, 1, '2026-01-09 00:00:00.000000', '18869452008', 'employee', '李国', 'li国0131@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (346, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'song华0274', '', '', 0, 1, '2026-01-08 00:00:00.000000', '13837498405', 'employee', '宋华', 'song华0274@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (347, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhu勇0141', '', '', 0, 1, '2026-01-09 00:00:00.000000', '13886783241', 'employee', '朱勇', 'zhu勇0141@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (348, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhong飞0340', '', '', 0, 1, '2026-01-18 00:00:00.000000', '13989390323', 'employee', '钟飞', 'zhong飞0340@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (349, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'sun平0105', '', '', 0, 1, '2026-01-25 00:00:00.000000', '18616055291', 'employee', '孙平', 'sun平0105@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (350, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'tian明0301', '', '', 0, 1, '2026-01-19 00:00:00.000000', '13923049857', 'employee', '田明', 'tian明0301@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (351, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhu建0289', '', '', 0, 1, '2025-12-31 00:00:00.000000', '13912844990', 'employee', '朱建', 'zhu建0289@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (352, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'ding军0276', '', '', 0, 1, '2026-01-09 00:00:00.000000', '18739350823', 'employee', '丁军', 'ding军0276@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (353, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'ma敏0118', '', '', 0, 1, '2026-01-13 00:00:00.000000', '18955630905', 'employee', '马敏', 'ma敏0118@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (354, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'sun龙0269', '', '', 0, 1, '2025-12-26 00:00:00.000000', '18746751579', 'employee', '孙龙', 'sun龙0269@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (355, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'xu芳0251', '', '', 0, 1, '2026-01-02 00:00:00.000000', '18934899349', 'employee', '许芳', 'xu芳0251@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (356, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhang芳0322', '', '', 0, 1, '2025-12-28 00:00:00.000000', '18899918228', 'employee', '张芳', 'zhang芳0322@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (357, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'ye桂0170', '', '', 0, 1, '2026-01-11 00:00:00.000000', '15267893213', 'employee', '叶桂英', 'ye桂0170@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (358, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'fu丽0122', '', '', 0, 1, '2026-01-16 00:00:00.000000', '18736867753', 'employee', '傅丽', 'fu丽0122@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (359, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'tian文0132', '', '', 0, 1, '2026-01-22 00:00:00.000000', '15730223420', 'employee', '田文', 'tian文0132@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (360, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'yu华0103', '', '', 0, 1, '2026-01-24 00:00:00.000000', '15835749590', 'employee', '余华', 'yu华0103@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (361, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhou小0116', '', '', 0, 1, '2026-01-20 00:00:00.000000', '15262465309', 'employee', '周小刚', 'zhou小0116@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (362, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'cao杰0126', '', '', 0, 1, '2026-01-22 00:00:00.000000', '13849059497', 'employee', '曹杰', 'cao杰0126@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (363, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'he芳0178', '', '', 0, 1, '2026-01-02 00:00:00.000000', '15813463979', 'employee', '何芳', 'he芳0178@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (364, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'he洋0132', '', '', 0, 1, '2026-01-14 00:00:00.000000', '15141559062', 'employee', '何洋', 'he洋0132@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (365, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'deng芳0151', '', '', 0, 1, '2026-01-23 00:00:00.000000', '13979961147', 'employee', '邓芳', 'deng芳0151@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (366, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'ding洋0178', '', '', 0, 1, '2026-01-21 00:00:00.000000', '15178238501', 'employee', '丁洋', 'ding洋0178@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (367, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhou勇0195', '', '', 0, 1, '2026-01-16 00:00:00.000000', '15061905999', 'employee', '周勇', 'zhou勇0195@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (368, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhao秀0159', '', '', 0, 1, '2026-01-01 00:00:00.000000', '15016706711', 'employee', '赵秀兰', 'zhao秀0159@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (369, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'yao平0242', '', '', 0, 1, '2026-01-18 00:00:00.000000', '15972411581', 'employee', '姚平', 'yao平0242@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (370, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'liu平0361', '', '', 0, 1, '2026-01-12 00:00:00.000000', '18991176269', 'employee', '刘平', 'liu平0361@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (371, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zheng敏0347', '', '', 0, 1, '2026-01-18 00:00:00.000000', '15170598611', 'employee', '郑敏', 'zheng敏0347@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (372, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'dong秀0120', '', '', 0, 1, '2026-01-21 00:00:00.000000', '13884130776', 'employee', '董秀兰', 'dong秀0120@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (373, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'wu芬0285', '', '', 0, 1, '2026-01-20 00:00:00.000000', '18718045966', 'employee', '吴芬', 'wu芬0285@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (374, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'hu文0228', '', '', 0, 1, '2026-01-25 00:00:00.000000', '15778182930', 'employee', '胡文', 'hu文0228@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (375, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhu磊0160', '', '', 0, 1, '2026-01-25 00:00:00.000000', '13939012087', 'employee', '朱磊', 'zhu磊0160@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (376, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'fan芬0175', '', '', 0, 1, '2026-01-17 00:00:00.000000', '15147279372', 'employee', '范芬', 'fan芬0175@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (377, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zeng明0336', '', '', 0, 1, '2026-01-15 00:00:00.000000', '18961874905', 'employee', '曾明', 'zeng明0336@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (378, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhou海0287', '', '', 0, 1, '2025-12-27 00:00:00.000000', '18912522889', 'employee', '周海燕', 'zhou海0287@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (379, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'cui芳0143', '', '', 0, 1, '2025-12-30 00:00:00.000000', '15213268954', 'employee', '崔芳', 'cui芳0143@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (380, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'cai丽0367', '', '', 0, 1, '2026-01-19 00:00:00.000000', '18644807912', 'employee', '蔡丽', 'cai丽0367@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (381, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'hu玉0304', '', '', 0, 1, '2026-01-23 00:00:00.000000', '15019237710', 'employee', '胡玉兰', 'hu玉0304@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (382, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'gao强0239', '', '', 0, 1, '2026-01-06 00:00:00.000000', '15916015043', 'employee', '高强', 'gao强0239@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (383, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zeng国0123', '', '', 0, 1, '2026-01-24 00:00:00.000000', '18883549811', 'employee', '曾国', 'zeng国0123@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (384, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'yu磊0244', '', '', 0, 1, '2026-01-03 00:00:00.000000', '18637460612', 'employee', '于磊', 'yu磊0244@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (385, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'su飞0135', '', '', 0, 1, '2026-01-11 00:00:00.000000', '15269811043', 'employee', '苏飞', 'su飞0135@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (386, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhu平0101', '', '', 0, 1, '2025-12-28 00:00:00.000000', '18863859620', 'employee', '朱平', 'zhu平0101@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (387, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'chen静0354', '', '', 0, 1, '2026-01-06 00:00:00.000000', '18724905786', 'employee', '陈静', 'chen静0354@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (388, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'liang金0364', '', '', 0, 1, '2025-12-27 00:00:00.000000', '15067178352', 'employee', '梁金凤', 'liang金0364@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (389, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'liu明0230', '', '', 0, 1, '2026-01-04 00:00:00.000000', '15017717359', 'employee', '刘明', 'liu明0230@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (390, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'cao丽0395', '', '', 0, 1, '2026-01-12 00:00:00.000000', '18755832020', 'employee', '曹丽', 'cao丽0395@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (391, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhong国0252', '', '', 0, 1, '2025-12-31 00:00:00.000000', '15119127766', 'employee', '钟国', 'zhong国0252@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (392, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'guo飞0308', '', '', 0, 1, '2026-01-15 00:00:00.000000', '18800763620', 'employee', '郭飞翔', 'guo飞0308@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (393, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'tan霞0281', '', '', 0, 1, '2025-12-30 00:00:00.000000', '15977460936', 'employee', '谭霞', 'tan霞0281@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (394, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'tang桂0286', '', '', 0, 1, '2025-12-31 00:00:00.000000', '13859996567', 'employee', '唐桂英', 'tang桂0286@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (395, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'cheng桂0168', '', '', 0, 1, '2026-01-24 00:00:00.000000', '15117423262', 'employee', '程桂英', 'cheng桂0168@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (396, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'jiang春0228', '', '', 0, 1, '2026-01-11 00:00:00.000000', '15117066133', 'employee', '姜春', 'jiang春0228@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (397, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhong芳0217', '', '', 0, 1, '2026-01-12 00:00:00.000000', '15815003775', 'employee', '钟芳', 'zhong芳0217@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (398, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhu芳0367', '', '', 0, 1, '2026-01-04 00:00:00.000000', '13994402407', 'employee', '朱芳', 'zhu芳0367@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (399, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'wei飞0156', '', '', 0, 1, '2025-12-28 00:00:00.000000', '15835086304', 'employee', '魏飞', 'wei飞0156@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (400, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'xu华0281', '', '', 0, 1, '2026-01-02 00:00:00.000000', '15786371730', 'employee', '徐华', 'xu华0281@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (401, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhang金0200', '', '', 0, 1, '2025-12-29 00:00:00.000000', '15042848120', 'employee', '张金凤', 'zhang金0200@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (402, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'cai洋0283', '', '', 0, 1, '2025-12-31 00:00:00.000000', '18716949013', 'employee', '蔡洋', 'cai洋0283@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (403, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'wang春0196', '', '', 0, 1, '2026-01-12 00:00:00.000000', '13965683397', 'employee', '王春', 'wang春0196@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (404, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'ding磊0295', '', '', 0, 1, '2026-01-21 00:00:00.000000', '18693805030', 'employee', '丁磊', 'ding磊0295@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (405, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'lu平0277', '', '', 0, 1, '2026-01-04 00:00:00.000000', '13975536816', 'employee', '陆平', 'lu平0277@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (406, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'chen刚0259', '', '', 0, 1, '2026-01-08 00:00:00.000000', '18932775693', 'employee', '陈刚', 'chen刚0259@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (407, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'yu华0317', '', '', 0, 1, '2026-01-21 00:00:00.000000', '15126977296', 'employee', '余华', 'yu华0317@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (408, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'lv磊0153', '', '', 0, 1, '2026-01-21 00:00:00.000000', '15756219376', 'employee', '吕磊', 'lv磊0153@hrms.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (409, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'song军0332', '', '', 0, 1, '2025-12-28 00:00:00.000000', '13846256873', 'employee', '宋军', 'song军0332@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (410, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'ma芬0375', '', '', 0, 1, '2026-01-07 00:00:00.000000', '13810658846', 'employee', '马芬', 'ma芬0375@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (411, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'guo伟0152', '', '', 0, 1, '2026-01-03 00:00:00.000000', '15897086230', 'employee', '郭伟', 'guo伟0152@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (412, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'deng鹏0295', '', '', 0, 1, '2025-12-26 00:00:00.000000', '15995904957', 'employee', '邓鹏', 'deng鹏0295@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (413, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'liu鹏0133', '', '', 0, 1, '2026-01-09 00:00:00.000000', '15069244795', 'employee', '刘鹏', 'liu鹏0133@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (414, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'liang小0107', '', '', 0, 1, '2026-01-17 00:00:00.000000', '18877339230', 'employee', '梁小刚', 'liang小0107@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (415, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'deng建0283', '', '', 0, 1, '2025-12-29 00:00:00.000000', '18697590879', 'employee', '邓建', 'deng建0283@example.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (416, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'feng文0271', '', '', 0, 1, '2026-01-22 00:00:00.000000', '13833305291', 'employee', '冯文', 'feng文0271@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (417, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'zhu杰0115', '', '', 0, 1, '2026-01-01 00:00:00.000000', '13876362281', 'employee', '朱杰', 'zhu杰0115@test.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (418, 'pbkdf2_sha256$1200000$lM446u3AXKKo0CfufaX2RB$TuYMi/+D9zD6PQMVya/Gonc1IXXAQwhmHJ88rM2/gHA=', NULL, 0, 'yuwen', '', '', 0, 1, '2026-01-27 06:45:40.785460', '18998766789', 'employee', 'yuwen', 'yuwen@qq.com', NULL, NULL, NULL);
INSERT INTO `accounts_user` VALUES (419, 'zhoucan123.', NULL, 0, 'zhoucan', '', '', 0, 1, '2026-01-27 07:27:27.872769', '17887655678', 'employee', 'zhoucan', 'zhoucan@qq.com', NULL, NULL, NULL);

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
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of accounts_usereditrequest
-- ----------------------------
INSERT INTO `accounts_usereditrequest` VALUES (1, 'phone', '13800000001', '18199987365', '新手机号', 'approved', '', '2026-01-25 02:58:48.366856', '2026-01-25 02:59:02.691481', 1, 1);
INSERT INTO `accounts_usereditrequest` VALUES (2, 'phone', '13800000006', '13132145678', '新手机号', 'pending', '', '2026-01-25 03:07:21.764428', '2026-01-25 03:07:21.764428', NULL, 6);
INSERT INTO `accounts_usereditrequest` VALUES (3, 'email', 'lina@hrms.com', 'lina993@qq.com', '新邮箱', 'pending', '', '2026-01-25 03:07:57.535313', '2026-01-25 03:07:57.535313', NULL, 6);
INSERT INTO `accounts_usereditrequest` VALUES (4, 'department', '技术研发部', '产品部', '内部转岗', 'approved', '同意转岗申请', '2026-01-25 19:53:50.000000', '2026-01-25 19:53:50.000000', 2, 6);
INSERT INTO `accounts_usereditrequest` VALUES (5, 'post', '初级开发工程师', '中级开发工程师', '职级晋升', 'approved', '晋升评审通过', '2026-01-25 19:53:50.000000', '2026-01-25 19:53:50.000000', 2, 7);
INSERT INTO `accounts_usereditrequest` VALUES (6, 'salary_base', '9000.00', '10000.00', '年度调薪', 'approved', '符合调薪标准', '2026-01-25 19:53:50.000000', '2026-01-25 19:53:50.000000', 2, 8);
INSERT INTO `accounts_usereditrequest` VALUES (7, 'emergency_contact', '', '15512345543', 'test', 'pending', '', '2026-01-27 04:37:18.263190', '2026-01-27 04:37:18.263190', NULL, 6);

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
) ENGINE = InnoDB AUTO_INCREMENT = 22 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of approval_approvalrequest
-- ----------------------------
INSERT INTO `approval_approvalrequest` VALUES (1, 'leave', 'personal', '2026-01-23 16:00:00.000000', '2026-01-24 16:00:00.000000', '测试事假', NULL, 'approved', '通过', '2026-01-24 12:07:24.802552', '2026-01-24 12:09:59.328108', 1, 1);
INSERT INTO `approval_approvalrequest` VALUES (2, 'overtime', NULL, '2026-01-23 16:00:00.000000', '2026-01-24 16:00:00.000000', '123', 2.0, 'approved', '通过', '2026-01-24 12:07:55.087964', '2026-01-24 12:10:09.251437', 1, 1);
INSERT INTO `approval_approvalrequest` VALUES (3, 'leave', 'personal', '2026-01-23 16:00:00.000000', '2026-01-24 16:00:00.000000', '111', NULL, 'pending', NULL, '2026-01-24 12:10:43.421461', '2026-01-24 12:10:43.421461', NULL, 1);
INSERT INTO `approval_approvalrequest` VALUES (4, 'leave', 'personal', '2026-01-23 16:00:00.000000', '2026-01-24 16:00:00.000000', '嘿嘿', NULL, 'pending', NULL, '2026-01-24 12:13:27.232338', '2026-01-24 12:13:27.232338', NULL, 1);
INSERT INTO `approval_approvalrequest` VALUES (5, 'leave', 'personal', '2026-01-23 16:00:00.000000', '2026-01-24 16:00:00.000000', '请假交材料', NULL, 'pending', NULL, '2026-01-24 15:59:01.754148', '2026-01-24 15:59:01.754148', NULL, 6);
INSERT INTO `approval_approvalrequest` VALUES (6, 'leave', 'annual', '2025-07-15 09:00:00.000000', '2025-07-16 18:00:00.000000', '年假回家探亲', NULL, 'approved', '同意，请注意安全', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 2, 6);
INSERT INTO `approval_approvalrequest` VALUES (7, 'leave', 'sick', '2025-08-20 09:00:00.000000', '2025-08-21 18:00:00.000000', '身体不适需要休息', NULL, 'approved', '批准，好好休息', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 2, 7);
INSERT INTO `approval_approvalrequest` VALUES (8, 'leave', 'personal', '2025-09-10 09:00:00.000000', '2025-09-12 18:00:00.000000', '处理家庭事务', NULL, 'approved', '已批准', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 2, 8);
INSERT INTO `approval_approvalrequest` VALUES (9, 'leave', 'annual', '2025-10-01 09:00:00.000000', '2025-10-07 18:00:00.000000', '国庆假期出游', NULL, 'approved', '国庆假期不用单独审批', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 2, 6);
INSERT INTO `approval_approvalrequest` VALUES (10, 'leave', 'personal', '2025-11-15 09:00:00.000000', '2025-11-15 18:00:00.000000', '个人事务需要处理', NULL, 'approved', '批准', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 2, 7);
INSERT INTO `approval_approvalrequest` VALUES (11, 'leave', 'sick', '2025-12-05 09:00:00.000000', '2025-12-05 18:00:00.000000', '感冒发烧', NULL, 'approved', '注意身体', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 2, 6);
INSERT INTO `approval_approvalrequest` VALUES (12, 'leave', 'annual', '2025-12-30 09:00:00.000000', '2026-01-02 18:00:00.000000', '年末休假', NULL, 'pending', NULL, '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', NULL, 8);
INSERT INTO `approval_approvalrequest` VALUES (13, 'leave', 'personal', '2026-01-20 09:00:00.000000', '2026-01-21 18:00:00.000000', '处理私人事务', NULL, 'pending', NULL, '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', NULL, 6);
INSERT INTO `approval_approvalrequest` VALUES (14, 'overtime', NULL, '2025-07-10 18:00:00.000000', '2025-07-10 21:00:00.000000', '项目上线需要', 3.0, 'approved', '项目紧急，批准加班', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 2, 6);
INSERT INTO `approval_approvalrequest` VALUES (15, 'overtime', NULL, '2025-08-15 18:00:00.000000', '2025-08-15 22:00:00.000000', '功能开发赶进度', 4.0, 'approved', '批准', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 2, 7);
INSERT INTO `approval_approvalrequest` VALUES (16, 'overtime', NULL, '2025-09-20 18:00:00.000000', '2025-09-20 20:00:00.000000', 'bug修复', 2.0, 'approved', '批准', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 2, 8);
INSERT INTO `approval_approvalrequest` VALUES (17, 'overtime', NULL, '2025-10-15 18:00:00.000000', '2025-10-15 23:00:00.000000', '版本发布', 5.0, 'approved', '发布日加班正常', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 2, 6);
INSERT INTO `approval_approvalrequest` VALUES (18, 'overtime', NULL, '2025-11-25 18:00:00.000000', '2025-11-25 21:00:00.000000', '需求开发', 3.0, 'approved', '批准', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 2, 7);
INSERT INTO `approval_approvalrequest` VALUES (19, 'overtime', NULL, '2025-12-20 18:00:00.000000', '2025-12-20 22:00:00.000000', '年终总结开发', 4.0, 'approved', '批准', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 2, 8);
INSERT INTO `approval_approvalrequest` VALUES (20, 'overtime', NULL, '2026-01-15 18:00:00.000000', '2026-01-15 21:00:00.000000', '新功能开发', 3.0, 'approved', '批准', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 2, 6);
INSERT INTO `approval_approvalrequest` VALUES (21, 'overtime', NULL, '2026-01-20 18:00:00.000000', '2026-01-20 20:00:00.000000', '代码优化', 2.0, 'pending', NULL, '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', NULL, 7);

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
  `department_id` bigint NULL DEFAULT NULL,
  `post_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `attendance_attendance_user_id_date_407a5a02_uniq`(`user_id` ASC, `date` ASC) USING BTREE,
  INDEX `attendance_attendance_date_3c949aa8`(`date` ASC) USING BTREE,
  INDEX `attendance_attendanc_department_id_564fe717_fk_organizat`(`department_id` ASC) USING BTREE,
  INDEX `attendance_attendance_post_id_6c131748_fk_organization_post_id`(`post_id` ASC) USING BTREE,
  CONSTRAINT `attendance_attendance_user_id_2bd82a2c_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `attendance_attendanc_department_id_564fe717_fk_organizat` FOREIGN KEY (`department_id`) REFERENCES `organization_department` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `attendance_attendance_post_id_6c131748_fk_organization_post_id` FOREIGN KEY (`post_id`) REFERENCES `organization_post` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2094 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of attendance_attendance
-- ----------------------------
INSERT INTO `attendance_attendance` VALUES (1, '2026-01-24', '16:10:58.000000', NULL, 'late', '2026-01-24 08:10:58.695201', '2026-01-24 09:26:05.293782', 1, NULL, NULL);
INSERT INTO `attendance_attendance` VALUES (2, '2024-12-02', '08:55:06.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 5, 1, 1);
INSERT INTO `attendance_attendance` VALUES (3, '2024-12-02', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (4, '2024-12-02', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (5, '2024-12-02', '08:55:00.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 8, 1, 2);
INSERT INTO `attendance_attendance` VALUES (6, '2024-12-02', '09:05:14.000000', NULL, 'late', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 9, 1, 2);
INSERT INTO `attendance_attendance` VALUES (7, '2024-12-02', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 10, 1, 3);
INSERT INTO `attendance_attendance` VALUES (8, '2024-12-02', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 11, 1, 3);
INSERT INTO `attendance_attendance` VALUES (9, '2024-12-02', '08:55:07.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 12, 1, 3);
INSERT INTO `attendance_attendance` VALUES (10, '2024-12-02', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 13, 1, 3);
INSERT INTO `attendance_attendance` VALUES (11, '2024-12-02', '08:55:02.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 14, 1, 4);
INSERT INTO `attendance_attendance` VALUES (12, '2024-12-02', '08:55:05.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 15, 1, 1);
INSERT INTO `attendance_attendance` VALUES (13, '2024-12-02', '08:55:02.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 16, 1, 1);
INSERT INTO `attendance_attendance` VALUES (14, '2024-12-02', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 17, 1, 2);
INSERT INTO `attendance_attendance` VALUES (15, '2024-12-02', '08:55:08.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 18, 1, 2);
INSERT INTO `attendance_attendance` VALUES (16, '2024-12-02', '08:55:00.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 19, 1, 2);
INSERT INTO `attendance_attendance` VALUES (17, '2024-12-02', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 20, 1, 3);
INSERT INTO `attendance_attendance` VALUES (18, '2024-12-02', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 21, 1, 3);
INSERT INTO `attendance_attendance` VALUES (19, '2024-12-02', '08:55:07.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 22, 1, 3);
INSERT INTO `attendance_attendance` VALUES (20, '2024-12-02', '08:55:07.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 23, 1, 3);
INSERT INTO `attendance_attendance` VALUES (21, '2024-12-02', NULL, '17:45:07.000000', 'early', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 24, 1, 4);
INSERT INTO `attendance_attendance` VALUES (22, '2024-12-02', '09:05:03.000000', NULL, 'late', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 25, 2, 5);
INSERT INTO `attendance_attendance` VALUES (23, '2024-12-02', NULL, '17:45:04.000000', 'early', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 26, 2, 5);
INSERT INTO `attendance_attendance` VALUES (24, '2024-12-02', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 27, 2, 5);
INSERT INTO `attendance_attendance` VALUES (25, '2024-12-02', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 28, 2, 5);
INSERT INTO `attendance_attendance` VALUES (26, '2024-12-02', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 29, 2, 5);
INSERT INTO `attendance_attendance` VALUES (27, '2024-12-02', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 30, 2, 5);
INSERT INTO `attendance_attendance` VALUES (28, '2024-12-02', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 31, 2, 5);
INSERT INTO `attendance_attendance` VALUES (29, '2024-12-02', '08:55:06.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 32, 2, 5);
INSERT INTO `attendance_attendance` VALUES (30, '2024-12-02', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 33, 2, 5);
INSERT INTO `attendance_attendance` VALUES (31, '2024-12-02', '08:55:07.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 34, 2, 5);
INSERT INTO `attendance_attendance` VALUES (32, '2024-12-02', '08:55:00.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 35, 3, 1);
INSERT INTO `attendance_attendance` VALUES (33, '2024-12-02', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 36, 3, 1);
INSERT INTO `attendance_attendance` VALUES (34, '2024-12-02', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 37, 3, 2);
INSERT INTO `attendance_attendance` VALUES (35, '2024-12-02', '09:05:10.000000', NULL, 'late', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 38, 3, 2);
INSERT INTO `attendance_attendance` VALUES (36, '2024-12-02', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 39, 3, 2);
INSERT INTO `attendance_attendance` VALUES (37, '2024-12-02', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 40, 3, 2);
INSERT INTO `attendance_attendance` VALUES (38, '2024-12-02', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 41, 3, 3);
INSERT INTO `attendance_attendance` VALUES (39, '2024-12-02', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 42, 3, 3);
INSERT INTO `attendance_attendance` VALUES (40, '2024-12-02', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 43, 3, 3);
INSERT INTO `attendance_attendance` VALUES (41, '2024-12-02', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 44, 3, 3);
INSERT INTO `attendance_attendance` VALUES (42, '2024-12-02', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 45, 4, 7);
INSERT INTO `attendance_attendance` VALUES (43, '2024-12-02', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 46, 4, 7);
INSERT INTO `attendance_attendance` VALUES (44, '2024-12-02', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 47, 4, 7);
INSERT INTO `attendance_attendance` VALUES (45, '2024-12-02', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 48, 4, 7);
INSERT INTO `attendance_attendance` VALUES (46, '2024-12-02', '08:55:06.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 49, 4, 7);
INSERT INTO `attendance_attendance` VALUES (47, '2024-12-02', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 50, 5, 8);
INSERT INTO `attendance_attendance` VALUES (48, '2024-12-02', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 51, 5, 8);
INSERT INTO `attendance_attendance` VALUES (49, '2024-12-02', '08:55:01.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 52, 5, 8);
INSERT INTO `attendance_attendance` VALUES (50, '2024-12-02', '08:55:08.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 53, 5, 8);
INSERT INTO `attendance_attendance` VALUES (51, '2024-12-02', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 54, 5, 8);
INSERT INTO `attendance_attendance` VALUES (52, '2024-12-02', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 55, 5, 8);
INSERT INTO `attendance_attendance` VALUES (53, '2024-12-02', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 56, 5, 8);
INSERT INTO `attendance_attendance` VALUES (54, '2024-12-02', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 57, 5, 8);
INSERT INTO `attendance_attendance` VALUES (55, '2024-12-02', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 58, 6, 9);
INSERT INTO `attendance_attendance` VALUES (56, '2024-12-02', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 59, 6, 9);
INSERT INTO `attendance_attendance` VALUES (57, '2024-12-02', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 60, 6, 9);
INSERT INTO `attendance_attendance` VALUES (58, '2024-12-02', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 61, 6, 9);
INSERT INTO `attendance_attendance` VALUES (59, '2024-12-02', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 62, 6, 9);
INSERT INTO `attendance_attendance` VALUES (60, '2024-12-02', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 63, 6, 9);
INSERT INTO `attendance_attendance` VALUES (61, '2024-12-02', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 64, 6, 9);
INSERT INTO `attendance_attendance` VALUES (62, '2024-12-02', '08:55:06.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 65, 6, 9);
INSERT INTO `attendance_attendance` VALUES (63, '2024-12-02', '09:05:29.000000', NULL, 'late', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 66, 6, 9);
INSERT INTO `attendance_attendance` VALUES (64, '2024-12-02', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 67, 6, 9);
INSERT INTO `attendance_attendance` VALUES (65, '2024-12-02', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 68, 7, 6);
INSERT INTO `attendance_attendance` VALUES (66, '2024-12-02', '09:05:10.000000', NULL, 'late', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 69, 7, 6);
INSERT INTO `attendance_attendance` VALUES (67, '2024-12-02', '08:55:00.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 70, 7, 6);
INSERT INTO `attendance_attendance` VALUES (68, '2024-12-02', '08:55:07.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 71, 7, 6);
INSERT INTO `attendance_attendance` VALUES (69, '2024-12-02', '09:05:26.000000', NULL, 'late', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 72, 7, 6);
INSERT INTO `attendance_attendance` VALUES (70, '2024-12-02', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 73, 7, 6);
INSERT INTO `attendance_attendance` VALUES (71, '2024-12-02', '08:55:05.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 74, 7, 6);
INSERT INTO `attendance_attendance` VALUES (72, '2024-12-02', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 75, 7, 6);
INSERT INTO `attendance_attendance` VALUES (73, '2024-12-02', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 76, 8, 10);
INSERT INTO `attendance_attendance` VALUES (74, '2024-12-02', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 77, 8, 10);
INSERT INTO `attendance_attendance` VALUES (75, '2024-12-02', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 78, 8, 10);
INSERT INTO `attendance_attendance` VALUES (76, '2024-12-02', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 79, 8, 10);
INSERT INTO `attendance_attendance` VALUES (77, '2024-12-02', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 80, 8, 10);
INSERT INTO `attendance_attendance` VALUES (78, '2024-12-02', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 81, 8, 10);
INSERT INTO `attendance_attendance` VALUES (79, '2024-12-02', NULL, NULL, 'absent', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 82, 8, 10);
INSERT INTO `attendance_attendance` VALUES (80, '2024-12-02', '08:55:10.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 83, 8, 10);
INSERT INTO `attendance_attendance` VALUES (81, '2024-12-02', '08:55:08.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 84, 9, 1);
INSERT INTO `attendance_attendance` VALUES (82, '2024-12-02', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 85, 9, 1);
INSERT INTO `attendance_attendance` VALUES (83, '2024-12-02', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 86, 9, 1);
INSERT INTO `attendance_attendance` VALUES (84, '2024-12-02', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 87, 9, 1);
INSERT INTO `attendance_attendance` VALUES (85, '2024-12-02', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 88, 9, 1);
INSERT INTO `attendance_attendance` VALUES (86, '2024-12-02', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 89, 10, 1);
INSERT INTO `attendance_attendance` VALUES (87, '2024-12-02', '08:55:00.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 90, 10, 1);
INSERT INTO `attendance_attendance` VALUES (88, '2024-12-02', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 91, 1, 2);
INSERT INTO `attendance_attendance` VALUES (89, '2024-12-02', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 92, 2, 5);
INSERT INTO `attendance_attendance` VALUES (90, '2024-12-02', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 93, 3, 1);
INSERT INTO `attendance_attendance` VALUES (91, '2024-12-02', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 94, 6, 9);
INSERT INTO `attendance_attendance` VALUES (92, '2024-12-02', '08:55:08.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 95, 5, 8);
INSERT INTO `attendance_attendance` VALUES (93, '2024-12-02', '08:55:07.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 96, 8, 10);
INSERT INTO `attendance_attendance` VALUES (94, '2024-12-02', '09:05:28.000000', NULL, 'late', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 97, 7, 6);
INSERT INTO `attendance_attendance` VALUES (95, '2024-12-02', NULL, '17:45:10.000000', 'early', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 98, 4, 7);
INSERT INTO `attendance_attendance` VALUES (96, '2024-12-02', '09:05:25.000000', NULL, 'late', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 99, 9, 1);
INSERT INTO `attendance_attendance` VALUES (97, '2024-12-02', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 100, 10, 1);
INSERT INTO `attendance_attendance` VALUES (98, '2024-12-03', '08:55:08.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 5, 1, 1);
INSERT INTO `attendance_attendance` VALUES (99, '2024-12-03', '08:55:09.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (100, '2024-12-03', '09:05:29.000000', NULL, 'late', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (101, '2024-12-03', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 8, 1, 2);
INSERT INTO `attendance_attendance` VALUES (102, '2024-12-03', '08:55:00.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 9, 1, 2);
INSERT INTO `attendance_attendance` VALUES (103, '2024-12-03', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 10, 1, 3);
INSERT INTO `attendance_attendance` VALUES (104, '2024-12-03', '08:55:10.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 11, 1, 3);
INSERT INTO `attendance_attendance` VALUES (105, '2024-12-03', '09:05:14.000000', NULL, 'late', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 12, 1, 3);
INSERT INTO `attendance_attendance` VALUES (106, '2024-12-03', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 13, 1, 3);
INSERT INTO `attendance_attendance` VALUES (107, '2024-12-03', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 14, 1, 4);
INSERT INTO `attendance_attendance` VALUES (108, '2024-12-03', NULL, NULL, 'absent', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 15, 1, 1);
INSERT INTO `attendance_attendance` VALUES (109, '2024-12-03', NULL, '17:45:09.000000', 'early', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 16, 1, 1);
INSERT INTO `attendance_attendance` VALUES (110, '2024-12-03', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 17, 1, 2);
INSERT INTO `attendance_attendance` VALUES (111, '2024-12-03', '08:55:00.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 18, 1, 2);
INSERT INTO `attendance_attendance` VALUES (112, '2024-12-03', '09:05:29.000000', NULL, 'late', '2026-01-24 16:13:19.000000', '2026-01-24 16:13:19.000000', 19, 1, 2);
INSERT INTO `attendance_attendance` VALUES (113, '2024-12-03', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 20, 1, 3);
INSERT INTO `attendance_attendance` VALUES (114, '2024-12-03', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 21, 1, 3);
INSERT INTO `attendance_attendance` VALUES (115, '2024-12-03', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 22, 1, 3);
INSERT INTO `attendance_attendance` VALUES (116, '2024-12-03', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 23, 1, 3);
INSERT INTO `attendance_attendance` VALUES (117, '2024-12-03', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 24, 1, 4);
INSERT INTO `attendance_attendance` VALUES (118, '2024-12-03', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 25, 2, 5);
INSERT INTO `attendance_attendance` VALUES (119, '2024-12-03', '09:05:15.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 26, 2, 5);
INSERT INTO `attendance_attendance` VALUES (120, '2024-12-03', '08:55:00.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 27, 2, 5);
INSERT INTO `attendance_attendance` VALUES (121, '2024-12-03', '08:55:07.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 28, 2, 5);
INSERT INTO `attendance_attendance` VALUES (122, '2024-12-03', '09:05:16.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 29, 2, 5);
INSERT INTO `attendance_attendance` VALUES (123, '2024-12-03', NULL, '17:45:02.000000', 'early', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 30, 2, 5);
INSERT INTO `attendance_attendance` VALUES (124, '2024-12-03', '08:55:03.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 31, 2, 5);
INSERT INTO `attendance_attendance` VALUES (125, '2024-12-03', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 32, 2, 5);
INSERT INTO `attendance_attendance` VALUES (126, '2024-12-03', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 33, 2, 5);
INSERT INTO `attendance_attendance` VALUES (127, '2024-12-03', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 34, 2, 5);
INSERT INTO `attendance_attendance` VALUES (128, '2024-12-03', '09:05:26.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 35, 3, 1);
INSERT INTO `attendance_attendance` VALUES (129, '2024-12-03', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 36, 3, 1);
INSERT INTO `attendance_attendance` VALUES (130, '2024-12-03', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 37, 3, 2);
INSERT INTO `attendance_attendance` VALUES (131, '2024-12-03', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 38, 3, 2);
INSERT INTO `attendance_attendance` VALUES (132, '2024-12-03', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 39, 3, 2);
INSERT INTO `attendance_attendance` VALUES (133, '2024-12-03', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 40, 3, 2);
INSERT INTO `attendance_attendance` VALUES (134, '2024-12-03', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 41, 3, 3);
INSERT INTO `attendance_attendance` VALUES (135, '2024-12-03', '08:55:01.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 42, 3, 3);
INSERT INTO `attendance_attendance` VALUES (136, '2024-12-03', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 43, 3, 3);
INSERT INTO `attendance_attendance` VALUES (137, '2024-12-03', '08:55:10.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 44, 3, 3);
INSERT INTO `attendance_attendance` VALUES (138, '2024-12-03', '08:55:05.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 45, 4, 7);
INSERT INTO `attendance_attendance` VALUES (139, '2024-12-03', '08:55:00.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 46, 4, 7);
INSERT INTO `attendance_attendance` VALUES (140, '2024-12-03', '08:55:03.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 47, 4, 7);
INSERT INTO `attendance_attendance` VALUES (141, '2024-12-03', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 48, 4, 7);
INSERT INTO `attendance_attendance` VALUES (142, '2024-12-03', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 49, 4, 7);
INSERT INTO `attendance_attendance` VALUES (143, '2024-12-03', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 50, 5, 8);
INSERT INTO `attendance_attendance` VALUES (144, '2024-12-03', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 51, 5, 8);
INSERT INTO `attendance_attendance` VALUES (145, '2024-12-03', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 52, 5, 8);
INSERT INTO `attendance_attendance` VALUES (146, '2024-12-03', '09:05:07.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 53, 5, 8);
INSERT INTO `attendance_attendance` VALUES (147, '2024-12-03', '08:55:10.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 54, 5, 8);
INSERT INTO `attendance_attendance` VALUES (148, '2024-12-03', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 55, 5, 8);
INSERT INTO `attendance_attendance` VALUES (149, '2024-12-03', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 56, 5, 8);
INSERT INTO `attendance_attendance` VALUES (150, '2024-12-03', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 57, 5, 8);
INSERT INTO `attendance_attendance` VALUES (151, '2024-12-03', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 58, 6, 9);
INSERT INTO `attendance_attendance` VALUES (152, '2024-12-03', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 59, 6, 9);
INSERT INTO `attendance_attendance` VALUES (153, '2024-12-03', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 60, 6, 9);
INSERT INTO `attendance_attendance` VALUES (154, '2024-12-03', '08:55:01.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 61, 6, 9);
INSERT INTO `attendance_attendance` VALUES (155, '2024-12-03', NULL, NULL, 'absent', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 62, 6, 9);
INSERT INTO `attendance_attendance` VALUES (156, '2024-12-03', '08:55:02.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 63, 6, 9);
INSERT INTO `attendance_attendance` VALUES (157, '2024-12-03', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 64, 6, 9);
INSERT INTO `attendance_attendance` VALUES (158, '2024-12-03', '09:05:18.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 65, 6, 9);
INSERT INTO `attendance_attendance` VALUES (159, '2024-12-03', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 66, 6, 9);
INSERT INTO `attendance_attendance` VALUES (160, '2024-12-03', '09:05:21.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 67, 6, 9);
INSERT INTO `attendance_attendance` VALUES (161, '2024-12-03', '08:55:04.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 68, 7, 6);
INSERT INTO `attendance_attendance` VALUES (162, '2024-12-03', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 69, 7, 6);
INSERT INTO `attendance_attendance` VALUES (163, '2024-12-03', '08:55:04.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 70, 7, 6);
INSERT INTO `attendance_attendance` VALUES (164, '2024-12-03', '09:05:13.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 71, 7, 6);
INSERT INTO `attendance_attendance` VALUES (165, '2024-12-03', '08:55:01.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 72, 7, 6);
INSERT INTO `attendance_attendance` VALUES (166, '2024-12-03', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 73, 7, 6);
INSERT INTO `attendance_attendance` VALUES (167, '2024-12-03', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 74, 7, 6);
INSERT INTO `attendance_attendance` VALUES (168, '2024-12-03', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 75, 7, 6);
INSERT INTO `attendance_attendance` VALUES (169, '2024-12-03', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 76, 8, 10);
INSERT INTO `attendance_attendance` VALUES (170, '2024-12-03', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 77, 8, 10);
INSERT INTO `attendance_attendance` VALUES (171, '2024-12-03', '08:55:07.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 78, 8, 10);
INSERT INTO `attendance_attendance` VALUES (172, '2024-12-03', '08:55:07.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 79, 8, 10);
INSERT INTO `attendance_attendance` VALUES (173, '2024-12-03', '08:55:02.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 80, 8, 10);
INSERT INTO `attendance_attendance` VALUES (174, '2024-12-03', '09:05:09.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 81, 8, 10);
INSERT INTO `attendance_attendance` VALUES (175, '2024-12-03', '09:05:17.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 82, 8, 10);
INSERT INTO `attendance_attendance` VALUES (176, '2024-12-03', '08:55:03.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 83, 8, 10);
INSERT INTO `attendance_attendance` VALUES (177, '2024-12-03', '08:55:10.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 84, 9, 1);
INSERT INTO `attendance_attendance` VALUES (178, '2024-12-03', '09:05:14.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 85, 9, 1);
INSERT INTO `attendance_attendance` VALUES (179, '2024-12-03', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 86, 9, 1);
INSERT INTO `attendance_attendance` VALUES (180, '2024-12-03', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 87, 9, 1);
INSERT INTO `attendance_attendance` VALUES (181, '2024-12-03', '09:05:09.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 88, 9, 1);
INSERT INTO `attendance_attendance` VALUES (182, '2024-12-03', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 89, 10, 1);
INSERT INTO `attendance_attendance` VALUES (183, '2024-12-03', NULL, NULL, 'absent', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 90, 10, 1);
INSERT INTO `attendance_attendance` VALUES (184, '2024-12-03', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 91, 1, 2);
INSERT INTO `attendance_attendance` VALUES (185, '2024-12-03', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 92, 2, 5);
INSERT INTO `attendance_attendance` VALUES (186, '2024-12-03', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 93, 3, 1);
INSERT INTO `attendance_attendance` VALUES (187, '2024-12-03', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 94, 6, 9);
INSERT INTO `attendance_attendance` VALUES (188, '2024-12-03', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 95, 5, 8);
INSERT INTO `attendance_attendance` VALUES (189, '2024-12-03', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 96, 8, 10);
INSERT INTO `attendance_attendance` VALUES (190, '2024-12-03', '08:55:10.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 97, 7, 6);
INSERT INTO `attendance_attendance` VALUES (191, '2024-12-03', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 98, 4, 7);
INSERT INTO `attendance_attendance` VALUES (192, '2024-12-03', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 99, 9, 1);
INSERT INTO `attendance_attendance` VALUES (193, '2024-12-03', '08:55:03.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 100, 10, 1);
INSERT INTO `attendance_attendance` VALUES (194, '2024-12-04', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 5, 1, 1);
INSERT INTO `attendance_attendance` VALUES (195, '2024-12-04', '08:55:03.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (196, '2024-12-04', '08:55:06.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (197, '2024-12-04', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 8, 1, 2);
INSERT INTO `attendance_attendance` VALUES (198, '2024-12-04', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 9, 1, 2);
INSERT INTO `attendance_attendance` VALUES (199, '2024-12-04', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 10, 1, 3);
INSERT INTO `attendance_attendance` VALUES (200, '2024-12-04', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 11, 1, 3);
INSERT INTO `attendance_attendance` VALUES (201, '2024-12-04', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 12, 1, 3);
INSERT INTO `attendance_attendance` VALUES (202, '2024-12-04', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 13, 1, 3);
INSERT INTO `attendance_attendance` VALUES (203, '2024-12-04', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 14, 1, 4);
INSERT INTO `attendance_attendance` VALUES (204, '2024-12-04', '08:55:08.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 15, 1, 1);
INSERT INTO `attendance_attendance` VALUES (205, '2024-12-04', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 16, 1, 1);
INSERT INTO `attendance_attendance` VALUES (206, '2024-12-04', '08:55:08.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 17, 1, 2);
INSERT INTO `attendance_attendance` VALUES (207, '2024-12-04', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 18, 1, 2);
INSERT INTO `attendance_attendance` VALUES (208, '2024-12-04', '08:55:08.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 19, 1, 2);
INSERT INTO `attendance_attendance` VALUES (209, '2024-12-04', '08:55:02.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 20, 1, 3);
INSERT INTO `attendance_attendance` VALUES (210, '2024-12-04', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 21, 1, 3);
INSERT INTO `attendance_attendance` VALUES (211, '2024-12-04', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 22, 1, 3);
INSERT INTO `attendance_attendance` VALUES (212, '2024-12-04', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 23, 1, 3);
INSERT INTO `attendance_attendance` VALUES (213, '2024-12-04', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 24, 1, 4);
INSERT INTO `attendance_attendance` VALUES (214, '2024-12-04', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 25, 2, 5);
INSERT INTO `attendance_attendance` VALUES (215, '2024-12-04', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 26, 2, 5);
INSERT INTO `attendance_attendance` VALUES (216, '2024-12-04', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 27, 2, 5);
INSERT INTO `attendance_attendance` VALUES (217, '2024-12-04', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 28, 2, 5);
INSERT INTO `attendance_attendance` VALUES (218, '2024-12-04', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 29, 2, 5);
INSERT INTO `attendance_attendance` VALUES (219, '2024-12-04', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 30, 2, 5);
INSERT INTO `attendance_attendance` VALUES (220, '2024-12-04', '09:05:28.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 31, 2, 5);
INSERT INTO `attendance_attendance` VALUES (221, '2024-12-04', '09:05:20.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 32, 2, 5);
INSERT INTO `attendance_attendance` VALUES (222, '2024-12-04', '08:55:04.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 33, 2, 5);
INSERT INTO `attendance_attendance` VALUES (223, '2024-12-04', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 34, 2, 5);
INSERT INTO `attendance_attendance` VALUES (224, '2024-12-04', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 35, 3, 1);
INSERT INTO `attendance_attendance` VALUES (225, '2024-12-04', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 36, 3, 1);
INSERT INTO `attendance_attendance` VALUES (226, '2024-12-04', '08:55:05.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 37, 3, 2);
INSERT INTO `attendance_attendance` VALUES (227, '2024-12-04', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 38, 3, 2);
INSERT INTO `attendance_attendance` VALUES (228, '2024-12-04', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 39, 3, 2);
INSERT INTO `attendance_attendance` VALUES (229, '2024-12-04', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 40, 3, 2);
INSERT INTO `attendance_attendance` VALUES (230, '2024-12-04', '08:55:06.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 41, 3, 3);
INSERT INTO `attendance_attendance` VALUES (231, '2024-12-04', '08:55:00.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 42, 3, 3);
INSERT INTO `attendance_attendance` VALUES (232, '2024-12-04', NULL, '17:45:10.000000', 'early', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 43, 3, 3);
INSERT INTO `attendance_attendance` VALUES (233, '2024-12-04', NULL, NULL, 'absent', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 44, 3, 3);
INSERT INTO `attendance_attendance` VALUES (234, '2024-12-04', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 45, 4, 7);
INSERT INTO `attendance_attendance` VALUES (235, '2024-12-04', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 46, 4, 7);
INSERT INTO `attendance_attendance` VALUES (236, '2024-12-04', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 47, 4, 7);
INSERT INTO `attendance_attendance` VALUES (237, '2024-12-04', '08:55:00.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 48, 4, 7);
INSERT INTO `attendance_attendance` VALUES (238, '2024-12-04', '08:55:04.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 49, 4, 7);
INSERT INTO `attendance_attendance` VALUES (239, '2024-12-04', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 50, 5, 8);
INSERT INTO `attendance_attendance` VALUES (240, '2024-12-04', '08:55:06.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 51, 5, 8);
INSERT INTO `attendance_attendance` VALUES (241, '2024-12-04', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 52, 5, 8);
INSERT INTO `attendance_attendance` VALUES (242, '2024-12-04', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 53, 5, 8);
INSERT INTO `attendance_attendance` VALUES (243, '2024-12-04', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 54, 5, 8);
INSERT INTO `attendance_attendance` VALUES (244, '2024-12-04', '08:55:06.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 55, 5, 8);
INSERT INTO `attendance_attendance` VALUES (245, '2024-12-04', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 56, 5, 8);
INSERT INTO `attendance_attendance` VALUES (246, '2024-12-04', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 57, 5, 8);
INSERT INTO `attendance_attendance` VALUES (247, '2024-12-04', '09:05:09.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 58, 6, 9);
INSERT INTO `attendance_attendance` VALUES (248, '2024-12-04', '08:55:07.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 59, 6, 9);
INSERT INTO `attendance_attendance` VALUES (249, '2024-12-04', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 60, 6, 9);
INSERT INTO `attendance_attendance` VALUES (250, '2024-12-04', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 61, 6, 9);
INSERT INTO `attendance_attendance` VALUES (251, '2024-12-04', '08:55:07.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 62, 6, 9);
INSERT INTO `attendance_attendance` VALUES (252, '2024-12-04', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 63, 6, 9);
INSERT INTO `attendance_attendance` VALUES (253, '2024-12-04', '08:55:05.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 64, 6, 9);
INSERT INTO `attendance_attendance` VALUES (254, '2024-12-04', '08:55:10.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 65, 6, 9);
INSERT INTO `attendance_attendance` VALUES (255, '2024-12-04', '08:55:10.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 66, 6, 9);
INSERT INTO `attendance_attendance` VALUES (256, '2024-12-04', '08:55:08.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 67, 6, 9);
INSERT INTO `attendance_attendance` VALUES (257, '2024-12-04', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 68, 7, 6);
INSERT INTO `attendance_attendance` VALUES (258, '2024-12-04', '08:55:10.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 69, 7, 6);
INSERT INTO `attendance_attendance` VALUES (259, '2024-12-04', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 70, 7, 6);
INSERT INTO `attendance_attendance` VALUES (260, '2024-12-04', '08:55:05.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 71, 7, 6);
INSERT INTO `attendance_attendance` VALUES (261, '2024-12-04', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 72, 7, 6);
INSERT INTO `attendance_attendance` VALUES (262, '2024-12-04', '09:05:16.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 73, 7, 6);
INSERT INTO `attendance_attendance` VALUES (263, '2024-12-04', '08:55:04.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 74, 7, 6);
INSERT INTO `attendance_attendance` VALUES (264, '2024-12-04', NULL, NULL, 'absent', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 75, 7, 6);
INSERT INTO `attendance_attendance` VALUES (265, '2024-12-04', '08:55:09.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 76, 8, 10);
INSERT INTO `attendance_attendance` VALUES (266, '2024-12-04', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 77, 8, 10);
INSERT INTO `attendance_attendance` VALUES (267, '2024-12-04', '08:55:04.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 78, 8, 10);
INSERT INTO `attendance_attendance` VALUES (268, '2024-12-04', '08:55:02.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 79, 8, 10);
INSERT INTO `attendance_attendance` VALUES (269, '2024-12-04', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 80, 8, 10);
INSERT INTO `attendance_attendance` VALUES (270, '2024-12-04', '08:55:00.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 81, 8, 10);
INSERT INTO `attendance_attendance` VALUES (271, '2024-12-04', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 82, 8, 10);
INSERT INTO `attendance_attendance` VALUES (272, '2024-12-04', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 83, 8, 10);
INSERT INTO `attendance_attendance` VALUES (273, '2024-12-04', '08:55:10.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 84, 9, 1);
INSERT INTO `attendance_attendance` VALUES (274, '2024-12-04', '08:55:03.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 85, 9, 1);
INSERT INTO `attendance_attendance` VALUES (275, '2024-12-04', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 86, 9, 1);
INSERT INTO `attendance_attendance` VALUES (276, '2024-12-04', '09:05:02.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 87, 9, 1);
INSERT INTO `attendance_attendance` VALUES (277, '2024-12-04', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 88, 9, 1);
INSERT INTO `attendance_attendance` VALUES (278, '2024-12-04', '08:55:07.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 89, 10, 1);
INSERT INTO `attendance_attendance` VALUES (279, '2024-12-04', '08:55:03.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 90, 10, 1);
INSERT INTO `attendance_attendance` VALUES (280, '2024-12-04', '08:55:06.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 91, 1, 2);
INSERT INTO `attendance_attendance` VALUES (281, '2024-12-04', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 92, 2, 5);
INSERT INTO `attendance_attendance` VALUES (282, '2024-12-04', '08:55:00.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 93, 3, 1);
INSERT INTO `attendance_attendance` VALUES (283, '2024-12-04', '08:55:06.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 94, 6, 9);
INSERT INTO `attendance_attendance` VALUES (284, '2024-12-04', '09:05:21.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 95, 5, 8);
INSERT INTO `attendance_attendance` VALUES (285, '2024-12-04', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 96, 8, 10);
INSERT INTO `attendance_attendance` VALUES (286, '2024-12-04', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 97, 7, 6);
INSERT INTO `attendance_attendance` VALUES (287, '2024-12-04', '08:55:10.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 98, 4, 7);
INSERT INTO `attendance_attendance` VALUES (288, '2024-12-04', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 99, 9, 1);
INSERT INTO `attendance_attendance` VALUES (289, '2024-12-04', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 100, 10, 1);
INSERT INTO `attendance_attendance` VALUES (290, '2024-12-05', '08:55:09.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 5, 1, 1);
INSERT INTO `attendance_attendance` VALUES (291, '2024-12-05', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (292, '2024-12-05', '08:55:06.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (293, '2024-12-05', '09:05:20.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 8, 1, 2);
INSERT INTO `attendance_attendance` VALUES (294, '2024-12-05', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 9, 1, 2);
INSERT INTO `attendance_attendance` VALUES (295, '2024-12-05', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 10, 1, 3);
INSERT INTO `attendance_attendance` VALUES (296, '2024-12-05', '08:55:06.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 11, 1, 3);
INSERT INTO `attendance_attendance` VALUES (297, '2024-12-05', '08:55:03.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 12, 1, 3);
INSERT INTO `attendance_attendance` VALUES (298, '2024-12-05', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 13, 1, 3);
INSERT INTO `attendance_attendance` VALUES (299, '2024-12-05', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 14, 1, 4);
INSERT INTO `attendance_attendance` VALUES (300, '2024-12-05', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 15, 1, 1);
INSERT INTO `attendance_attendance` VALUES (301, '2024-12-05', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 16, 1, 1);
INSERT INTO `attendance_attendance` VALUES (302, '2024-12-05', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 17, 1, 2);
INSERT INTO `attendance_attendance` VALUES (303, '2024-12-05', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 18, 1, 2);
INSERT INTO `attendance_attendance` VALUES (304, '2024-12-05', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 19, 1, 2);
INSERT INTO `attendance_attendance` VALUES (305, '2024-12-05', NULL, NULL, 'absent', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 20, 1, 3);
INSERT INTO `attendance_attendance` VALUES (306, '2024-12-05', '08:55:00.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 21, 1, 3);
INSERT INTO `attendance_attendance` VALUES (307, '2024-12-05', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 22, 1, 3);
INSERT INTO `attendance_attendance` VALUES (308, '2024-12-05', '09:05:03.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 23, 1, 3);
INSERT INTO `attendance_attendance` VALUES (309, '2024-12-05', '08:55:07.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 24, 1, 4);
INSERT INTO `attendance_attendance` VALUES (310, '2024-12-05', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 25, 2, 5);
INSERT INTO `attendance_attendance` VALUES (311, '2024-12-05', '08:55:09.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 26, 2, 5);
INSERT INTO `attendance_attendance` VALUES (312, '2024-12-05', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 27, 2, 5);
INSERT INTO `attendance_attendance` VALUES (313, '2024-12-05', '08:55:08.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 28, 2, 5);
INSERT INTO `attendance_attendance` VALUES (314, '2024-12-05', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 29, 2, 5);
INSERT INTO `attendance_attendance` VALUES (315, '2024-12-05', '08:55:00.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 30, 2, 5);
INSERT INTO `attendance_attendance` VALUES (316, '2024-12-05', '08:55:07.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 31, 2, 5);
INSERT INTO `attendance_attendance` VALUES (317, '2024-12-05', '08:55:08.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 32, 2, 5);
INSERT INTO `attendance_attendance` VALUES (318, '2024-12-05', '08:55:05.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 33, 2, 5);
INSERT INTO `attendance_attendance` VALUES (319, '2024-12-05', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 34, 2, 5);
INSERT INTO `attendance_attendance` VALUES (320, '2024-12-05', '08:55:00.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 35, 3, 1);
INSERT INTO `attendance_attendance` VALUES (321, '2024-12-05', '08:55:03.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 36, 3, 1);
INSERT INTO `attendance_attendance` VALUES (322, '2024-12-05', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 37, 3, 2);
INSERT INTO `attendance_attendance` VALUES (323, '2024-12-05', NULL, NULL, 'absent', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 38, 3, 2);
INSERT INTO `attendance_attendance` VALUES (324, '2024-12-05', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 39, 3, 2);
INSERT INTO `attendance_attendance` VALUES (325, '2024-12-05', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 40, 3, 2);
INSERT INTO `attendance_attendance` VALUES (326, '2024-12-05', '09:05:19.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 41, 3, 3);
INSERT INTO `attendance_attendance` VALUES (327, '2024-12-05', '08:55:01.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 42, 3, 3);
INSERT INTO `attendance_attendance` VALUES (328, '2024-12-05', '08:55:08.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 43, 3, 3);
INSERT INTO `attendance_attendance` VALUES (329, '2024-12-05', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 44, 3, 3);
INSERT INTO `attendance_attendance` VALUES (330, '2024-12-05', '08:55:01.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 45, 4, 7);
INSERT INTO `attendance_attendance` VALUES (331, '2024-12-05', '08:55:01.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 46, 4, 7);
INSERT INTO `attendance_attendance` VALUES (332, '2024-12-05', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 47, 4, 7);
INSERT INTO `attendance_attendance` VALUES (333, '2024-12-05', NULL, NULL, 'absent', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 48, 4, 7);
INSERT INTO `attendance_attendance` VALUES (334, '2024-12-05', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 49, 4, 7);
INSERT INTO `attendance_attendance` VALUES (335, '2024-12-05', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 50, 5, 8);
INSERT INTO `attendance_attendance` VALUES (336, '2024-12-05', NULL, '17:45:09.000000', 'early', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 51, 5, 8);
INSERT INTO `attendance_attendance` VALUES (337, '2024-12-05', '08:55:10.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 52, 5, 8);
INSERT INTO `attendance_attendance` VALUES (338, '2024-12-05', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 53, 5, 8);
INSERT INTO `attendance_attendance` VALUES (339, '2024-12-05', '08:55:01.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 54, 5, 8);
INSERT INTO `attendance_attendance` VALUES (340, '2024-12-05', '08:55:01.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 55, 5, 8);
INSERT INTO `attendance_attendance` VALUES (341, '2024-12-05', '08:55:10.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 56, 5, 8);
INSERT INTO `attendance_attendance` VALUES (342, '2024-12-05', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 57, 5, 8);
INSERT INTO `attendance_attendance` VALUES (343, '2024-12-05', '08:55:01.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 58, 6, 9);
INSERT INTO `attendance_attendance` VALUES (344, '2024-12-05', '08:55:10.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 59, 6, 9);
INSERT INTO `attendance_attendance` VALUES (345, '2024-12-05', '08:55:07.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 60, 6, 9);
INSERT INTO `attendance_attendance` VALUES (346, '2024-12-05', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 61, 6, 9);
INSERT INTO `attendance_attendance` VALUES (347, '2024-12-05', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 62, 6, 9);
INSERT INTO `attendance_attendance` VALUES (348, '2024-12-05', '08:55:07.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 63, 6, 9);
INSERT INTO `attendance_attendance` VALUES (349, '2024-12-05', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 64, 6, 9);
INSERT INTO `attendance_attendance` VALUES (350, '2024-12-05', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 65, 6, 9);
INSERT INTO `attendance_attendance` VALUES (351, '2024-12-05', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 66, 6, 9);
INSERT INTO `attendance_attendance` VALUES (352, '2024-12-05', '08:55:07.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 67, 6, 9);
INSERT INTO `attendance_attendance` VALUES (353, '2024-12-05', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 68, 7, 6);
INSERT INTO `attendance_attendance` VALUES (354, '2024-12-05', NULL, '17:45:03.000000', 'early', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 69, 7, 6);
INSERT INTO `attendance_attendance` VALUES (355, '2024-12-05', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 70, 7, 6);
INSERT INTO `attendance_attendance` VALUES (356, '2024-12-05', '08:55:03.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 71, 7, 6);
INSERT INTO `attendance_attendance` VALUES (357, '2024-12-05', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 72, 7, 6);
INSERT INTO `attendance_attendance` VALUES (358, '2024-12-05', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 73, 7, 6);
INSERT INTO `attendance_attendance` VALUES (359, '2024-12-05', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 74, 7, 6);
INSERT INTO `attendance_attendance` VALUES (360, '2024-12-05', '08:55:06.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 75, 7, 6);
INSERT INTO `attendance_attendance` VALUES (361, '2024-12-05', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 76, 8, 10);
INSERT INTO `attendance_attendance` VALUES (362, '2024-12-05', NULL, NULL, 'absent', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 77, 8, 10);
INSERT INTO `attendance_attendance` VALUES (363, '2024-12-05', '08:55:09.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 78, 8, 10);
INSERT INTO `attendance_attendance` VALUES (364, '2024-12-05', '08:55:03.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 79, 8, 10);
INSERT INTO `attendance_attendance` VALUES (365, '2024-12-05', '09:05:26.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 80, 8, 10);
INSERT INTO `attendance_attendance` VALUES (366, '2024-12-05', '08:55:02.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 81, 8, 10);
INSERT INTO `attendance_attendance` VALUES (367, '2024-12-05', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 82, 8, 10);
INSERT INTO `attendance_attendance` VALUES (368, '2024-12-05', '08:55:06.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 83, 8, 10);
INSERT INTO `attendance_attendance` VALUES (369, '2024-12-05', '09:05:14.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 84, 9, 1);
INSERT INTO `attendance_attendance` VALUES (370, '2024-12-05', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 85, 9, 1);
INSERT INTO `attendance_attendance` VALUES (371, '2024-12-05', '08:55:01.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 86, 9, 1);
INSERT INTO `attendance_attendance` VALUES (372, '2024-12-05', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 87, 9, 1);
INSERT INTO `attendance_attendance` VALUES (373, '2024-12-05', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 88, 9, 1);
INSERT INTO `attendance_attendance` VALUES (374, '2024-12-05', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 89, 10, 1);
INSERT INTO `attendance_attendance` VALUES (375, '2024-12-05', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 90, 10, 1);
INSERT INTO `attendance_attendance` VALUES (376, '2024-12-05', '08:55:05.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 91, 1, 2);
INSERT INTO `attendance_attendance` VALUES (377, '2024-12-05', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 92, 2, 5);
INSERT INTO `attendance_attendance` VALUES (378, '2024-12-05', NULL, '17:45:04.000000', 'early', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 93, 3, 1);
INSERT INTO `attendance_attendance` VALUES (379, '2024-12-05', '09:05:15.000000', NULL, 'late', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 94, 6, 9);
INSERT INTO `attendance_attendance` VALUES (380, '2024-12-05', '08:55:05.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:20.000000', '2026-01-24 16:13:20.000000', 95, 5, 8);
INSERT INTO `attendance_attendance` VALUES (381, '2024-12-05', '08:55:00.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 96, 8, 10);
INSERT INTO `attendance_attendance` VALUES (382, '2024-12-05', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 97, 7, 6);
INSERT INTO `attendance_attendance` VALUES (383, '2024-12-05', '08:55:00.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 98, 4, 7);
INSERT INTO `attendance_attendance` VALUES (384, '2024-12-05', '08:55:01.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 99, 9, 1);
INSERT INTO `attendance_attendance` VALUES (385, '2024-12-05', '08:55:02.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 100, 10, 1);
INSERT INTO `attendance_attendance` VALUES (386, '2024-12-06', '08:55:08.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 5, 1, 1);
INSERT INTO `attendance_attendance` VALUES (387, '2024-12-06', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (388, '2024-12-06', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (389, '2024-12-06', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 8, 1, 2);
INSERT INTO `attendance_attendance` VALUES (390, '2024-12-06', NULL, NULL, 'absent', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 9, 1, 2);
INSERT INTO `attendance_attendance` VALUES (391, '2024-12-06', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 10, 1, 3);
INSERT INTO `attendance_attendance` VALUES (392, '2024-12-06', '08:55:00.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 11, 1, 3);
INSERT INTO `attendance_attendance` VALUES (393, '2024-12-06', '09:05:04.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 12, 1, 3);
INSERT INTO `attendance_attendance` VALUES (394, '2024-12-06', '08:55:01.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 13, 1, 3);
INSERT INTO `attendance_attendance` VALUES (395, '2024-12-06', '09:05:09.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 14, 1, 4);
INSERT INTO `attendance_attendance` VALUES (396, '2024-12-06', NULL, '17:45:08.000000', 'early', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 15, 1, 1);
INSERT INTO `attendance_attendance` VALUES (397, '2024-12-06', '08:55:02.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 16, 1, 1);
INSERT INTO `attendance_attendance` VALUES (398, '2024-12-06', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 17, 1, 2);
INSERT INTO `attendance_attendance` VALUES (399, '2024-12-06', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 18, 1, 2);
INSERT INTO `attendance_attendance` VALUES (400, '2024-12-06', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 19, 1, 2);
INSERT INTO `attendance_attendance` VALUES (401, '2024-12-06', '08:55:02.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 20, 1, 3);
INSERT INTO `attendance_attendance` VALUES (402, '2024-12-06', '08:55:08.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 21, 1, 3);
INSERT INTO `attendance_attendance` VALUES (403, '2024-12-06', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 22, 1, 3);
INSERT INTO `attendance_attendance` VALUES (404, '2024-12-06', '08:55:01.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 23, 1, 3);
INSERT INTO `attendance_attendance` VALUES (405, '2024-12-06', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 24, 1, 4);
INSERT INTO `attendance_attendance` VALUES (406, '2024-12-06', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 25, 2, 5);
INSERT INTO `attendance_attendance` VALUES (407, '2024-12-06', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 26, 2, 5);
INSERT INTO `attendance_attendance` VALUES (408, '2024-12-06', '08:55:02.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 27, 2, 5);
INSERT INTO `attendance_attendance` VALUES (409, '2024-12-06', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 28, 2, 5);
INSERT INTO `attendance_attendance` VALUES (410, '2024-12-06', '08:55:09.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 29, 2, 5);
INSERT INTO `attendance_attendance` VALUES (411, '2024-12-06', '08:55:07.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 30, 2, 5);
INSERT INTO `attendance_attendance` VALUES (412, '2024-12-06', '08:55:07.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 31, 2, 5);
INSERT INTO `attendance_attendance` VALUES (413, '2024-12-06', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 32, 2, 5);
INSERT INTO `attendance_attendance` VALUES (414, '2024-12-06', '08:55:01.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 33, 2, 5);
INSERT INTO `attendance_attendance` VALUES (415, '2024-12-06', '09:05:14.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 34, 2, 5);
INSERT INTO `attendance_attendance` VALUES (416, '2024-12-06', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 35, 3, 1);
INSERT INTO `attendance_attendance` VALUES (417, '2024-12-06', '08:55:10.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 36, 3, 1);
INSERT INTO `attendance_attendance` VALUES (418, '2024-12-06', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 37, 3, 2);
INSERT INTO `attendance_attendance` VALUES (419, '2024-12-06', '08:55:00.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 38, 3, 2);
INSERT INTO `attendance_attendance` VALUES (420, '2024-12-06', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 39, 3, 2);
INSERT INTO `attendance_attendance` VALUES (421, '2024-12-06', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 40, 3, 2);
INSERT INTO `attendance_attendance` VALUES (422, '2024-12-06', '08:55:05.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 41, 3, 3);
INSERT INTO `attendance_attendance` VALUES (423, '2024-12-06', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 42, 3, 3);
INSERT INTO `attendance_attendance` VALUES (424, '2024-12-06', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 43, 3, 3);
INSERT INTO `attendance_attendance` VALUES (425, '2024-12-06', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 44, 3, 3);
INSERT INTO `attendance_attendance` VALUES (426, '2024-12-06', '08:55:04.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 45, 4, 7);
INSERT INTO `attendance_attendance` VALUES (427, '2024-12-06', '08:55:05.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 46, 4, 7);
INSERT INTO `attendance_attendance` VALUES (428, '2024-12-06', '08:55:04.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 47, 4, 7);
INSERT INTO `attendance_attendance` VALUES (429, '2024-12-06', '08:55:06.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 48, 4, 7);
INSERT INTO `attendance_attendance` VALUES (430, '2024-12-06', '08:55:09.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 49, 4, 7);
INSERT INTO `attendance_attendance` VALUES (431, '2024-12-06', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 50, 5, 8);
INSERT INTO `attendance_attendance` VALUES (432, '2024-12-06', '09:05:16.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 51, 5, 8);
INSERT INTO `attendance_attendance` VALUES (433, '2024-12-06', '08:55:03.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 52, 5, 8);
INSERT INTO `attendance_attendance` VALUES (434, '2024-12-06', '08:55:01.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 53, 5, 8);
INSERT INTO `attendance_attendance` VALUES (435, '2024-12-06', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 54, 5, 8);
INSERT INTO `attendance_attendance` VALUES (436, '2024-12-06', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 55, 5, 8);
INSERT INTO `attendance_attendance` VALUES (437, '2024-12-06', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 56, 5, 8);
INSERT INTO `attendance_attendance` VALUES (438, '2024-12-06', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 57, 5, 8);
INSERT INTO `attendance_attendance` VALUES (439, '2024-12-06', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 58, 6, 9);
INSERT INTO `attendance_attendance` VALUES (440, '2024-12-06', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 59, 6, 9);
INSERT INTO `attendance_attendance` VALUES (441, '2024-12-06', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 60, 6, 9);
INSERT INTO `attendance_attendance` VALUES (442, '2024-12-06', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 61, 6, 9);
INSERT INTO `attendance_attendance` VALUES (443, '2024-12-06', '08:55:06.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 62, 6, 9);
INSERT INTO `attendance_attendance` VALUES (444, '2024-12-06', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 63, 6, 9);
INSERT INTO `attendance_attendance` VALUES (445, '2024-12-06', '08:55:05.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 64, 6, 9);
INSERT INTO `attendance_attendance` VALUES (446, '2024-12-06', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 65, 6, 9);
INSERT INTO `attendance_attendance` VALUES (447, '2024-12-06', '08:55:07.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 66, 6, 9);
INSERT INTO `attendance_attendance` VALUES (448, '2024-12-06', '09:05:23.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 67, 6, 9);
INSERT INTO `attendance_attendance` VALUES (449, '2024-12-06', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 68, 7, 6);
INSERT INTO `attendance_attendance` VALUES (450, '2024-12-06', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 69, 7, 6);
INSERT INTO `attendance_attendance` VALUES (451, '2024-12-06', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 70, 7, 6);
INSERT INTO `attendance_attendance` VALUES (452, '2024-12-06', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 71, 7, 6);
INSERT INTO `attendance_attendance` VALUES (453, '2024-12-06', '08:55:06.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 72, 7, 6);
INSERT INTO `attendance_attendance` VALUES (454, '2024-12-06', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 73, 7, 6);
INSERT INTO `attendance_attendance` VALUES (455, '2024-12-06', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 74, 7, 6);
INSERT INTO `attendance_attendance` VALUES (456, '2024-12-06', '08:55:02.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 75, 7, 6);
INSERT INTO `attendance_attendance` VALUES (457, '2024-12-06', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 76, 8, 10);
INSERT INTO `attendance_attendance` VALUES (458, '2024-12-06', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 77, 8, 10);
INSERT INTO `attendance_attendance` VALUES (459, '2024-12-06', '08:55:07.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 78, 8, 10);
INSERT INTO `attendance_attendance` VALUES (460, '2024-12-06', '08:55:00.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 79, 8, 10);
INSERT INTO `attendance_attendance` VALUES (461, '2024-12-06', NULL, '17:45:08.000000', 'early', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 80, 8, 10);
INSERT INTO `attendance_attendance` VALUES (462, '2024-12-06', '08:55:08.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 81, 8, 10);
INSERT INTO `attendance_attendance` VALUES (463, '2024-12-06', '09:05:17.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 82, 8, 10);
INSERT INTO `attendance_attendance` VALUES (464, '2024-12-06', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 83, 8, 10);
INSERT INTO `attendance_attendance` VALUES (465, '2024-12-06', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 84, 9, 1);
INSERT INTO `attendance_attendance` VALUES (466, '2024-12-06', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 85, 9, 1);
INSERT INTO `attendance_attendance` VALUES (467, '2024-12-06', NULL, '17:45:03.000000', 'early', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 86, 9, 1);
INSERT INTO `attendance_attendance` VALUES (468, '2024-12-06', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 87, 9, 1);
INSERT INTO `attendance_attendance` VALUES (469, '2024-12-06', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 88, 9, 1);
INSERT INTO `attendance_attendance` VALUES (470, '2024-12-06', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 89, 10, 1);
INSERT INTO `attendance_attendance` VALUES (471, '2024-12-06', '08:55:10.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 90, 10, 1);
INSERT INTO `attendance_attendance` VALUES (472, '2024-12-06', '09:05:10.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 91, 1, 2);
INSERT INTO `attendance_attendance` VALUES (473, '2024-12-06', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 92, 2, 5);
INSERT INTO `attendance_attendance` VALUES (474, '2024-12-06', '08:55:00.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 93, 3, 1);
INSERT INTO `attendance_attendance` VALUES (475, '2024-12-06', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 94, 6, 9);
INSERT INTO `attendance_attendance` VALUES (476, '2024-12-06', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 95, 5, 8);
INSERT INTO `attendance_attendance` VALUES (477, '2024-12-06', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 96, 8, 10);
INSERT INTO `attendance_attendance` VALUES (478, '2024-12-06', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 97, 7, 6);
INSERT INTO `attendance_attendance` VALUES (479, '2024-12-06', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 98, 4, 7);
INSERT INTO `attendance_attendance` VALUES (480, '2024-12-06', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 99, 9, 1);
INSERT INTO `attendance_attendance` VALUES (481, '2024-12-06', '08:55:06.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 100, 10, 1);
INSERT INTO `attendance_attendance` VALUES (482, '2024-12-09', '08:55:08.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 5, 1, 1);
INSERT INTO `attendance_attendance` VALUES (483, '2024-12-09', '08:55:01.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (484, '2024-12-09', '08:55:03.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (485, '2024-12-09', '08:55:05.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 8, 1, 2);
INSERT INTO `attendance_attendance` VALUES (486, '2024-12-09', '08:55:01.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 9, 1, 2);
INSERT INTO `attendance_attendance` VALUES (487, '2024-12-09', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 10, 1, 3);
INSERT INTO `attendance_attendance` VALUES (488, '2024-12-09', '09:05:22.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 11, 1, 3);
INSERT INTO `attendance_attendance` VALUES (489, '2024-12-09', '09:05:04.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 12, 1, 3);
INSERT INTO `attendance_attendance` VALUES (490, '2024-12-09', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 13, 1, 3);
INSERT INTO `attendance_attendance` VALUES (491, '2024-12-09', '08:55:10.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 14, 1, 4);
INSERT INTO `attendance_attendance` VALUES (492, '2024-12-09', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 15, 1, 1);
INSERT INTO `attendance_attendance` VALUES (493, '2024-12-09', '09:05:20.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 16, 1, 1);
INSERT INTO `attendance_attendance` VALUES (494, '2024-12-09', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 17, 1, 2);
INSERT INTO `attendance_attendance` VALUES (495, '2024-12-09', '08:55:08.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 18, 1, 2);
INSERT INTO `attendance_attendance` VALUES (496, '2024-12-09', '09:05:05.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 19, 1, 2);
INSERT INTO `attendance_attendance` VALUES (497, '2024-12-09', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 20, 1, 3);
INSERT INTO `attendance_attendance` VALUES (498, '2024-12-09', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 21, 1, 3);
INSERT INTO `attendance_attendance` VALUES (499, '2024-12-09', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 22, 1, 3);
INSERT INTO `attendance_attendance` VALUES (500, '2024-12-09', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 23, 1, 3);
INSERT INTO `attendance_attendance` VALUES (501, '2024-12-09', '08:55:02.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 24, 1, 4);
INSERT INTO `attendance_attendance` VALUES (502, '2024-12-09', '08:55:05.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 25, 2, 5);
INSERT INTO `attendance_attendance` VALUES (503, '2024-12-09', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 26, 2, 5);
INSERT INTO `attendance_attendance` VALUES (504, '2024-12-09', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 27, 2, 5);
INSERT INTO `attendance_attendance` VALUES (505, '2024-12-09', '09:05:17.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 28, 2, 5);
INSERT INTO `attendance_attendance` VALUES (506, '2024-12-09', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 29, 2, 5);
INSERT INTO `attendance_attendance` VALUES (507, '2024-12-09', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 30, 2, 5);
INSERT INTO `attendance_attendance` VALUES (508, '2024-12-09', '09:05:06.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 31, 2, 5);
INSERT INTO `attendance_attendance` VALUES (509, '2024-12-09', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 32, 2, 5);
INSERT INTO `attendance_attendance` VALUES (510, '2024-12-09', '09:05:19.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 33, 2, 5);
INSERT INTO `attendance_attendance` VALUES (511, '2024-12-09', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 34, 2, 5);
INSERT INTO `attendance_attendance` VALUES (512, '2024-12-09', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 35, 3, 1);
INSERT INTO `attendance_attendance` VALUES (513, '2024-12-09', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 36, 3, 1);
INSERT INTO `attendance_attendance` VALUES (514, '2024-12-09', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 37, 3, 2);
INSERT INTO `attendance_attendance` VALUES (515, '2024-12-09', NULL, '17:45:08.000000', 'early', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 38, 3, 2);
INSERT INTO `attendance_attendance` VALUES (516, '2024-12-09', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 39, 3, 2);
INSERT INTO `attendance_attendance` VALUES (517, '2024-12-09', '08:55:06.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 40, 3, 2);
INSERT INTO `attendance_attendance` VALUES (518, '2024-12-09', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 41, 3, 3);
INSERT INTO `attendance_attendance` VALUES (519, '2024-12-09', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 42, 3, 3);
INSERT INTO `attendance_attendance` VALUES (520, '2024-12-09', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 43, 3, 3);
INSERT INTO `attendance_attendance` VALUES (521, '2024-12-09', '09:05:17.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 44, 3, 3);
INSERT INTO `attendance_attendance` VALUES (522, '2024-12-09', '08:55:09.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 45, 4, 7);
INSERT INTO `attendance_attendance` VALUES (523, '2024-12-09', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 46, 4, 7);
INSERT INTO `attendance_attendance` VALUES (524, '2024-12-09', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 47, 4, 7);
INSERT INTO `attendance_attendance` VALUES (525, '2024-12-09', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 48, 4, 7);
INSERT INTO `attendance_attendance` VALUES (526, '2024-12-09', '08:55:06.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 49, 4, 7);
INSERT INTO `attendance_attendance` VALUES (527, '2024-12-09', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 50, 5, 8);
INSERT INTO `attendance_attendance` VALUES (528, '2024-12-09', '09:05:18.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 51, 5, 8);
INSERT INTO `attendance_attendance` VALUES (529, '2024-12-09', '08:55:09.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 52, 5, 8);
INSERT INTO `attendance_attendance` VALUES (530, '2024-12-09', '09:05:27.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 53, 5, 8);
INSERT INTO `attendance_attendance` VALUES (531, '2024-12-09', NULL, '17:45:01.000000', 'early', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 54, 5, 8);
INSERT INTO `attendance_attendance` VALUES (532, '2024-12-09', '08:55:00.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 55, 5, 8);
INSERT INTO `attendance_attendance` VALUES (533, '2024-12-09', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 56, 5, 8);
INSERT INTO `attendance_attendance` VALUES (534, '2024-12-09', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 57, 5, 8);
INSERT INTO `attendance_attendance` VALUES (535, '2024-12-09', '09:05:14.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 58, 6, 9);
INSERT INTO `attendance_attendance` VALUES (536, '2024-12-09', '08:55:01.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 59, 6, 9);
INSERT INTO `attendance_attendance` VALUES (537, '2024-12-09', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 60, 6, 9);
INSERT INTO `attendance_attendance` VALUES (538, '2024-12-09', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 61, 6, 9);
INSERT INTO `attendance_attendance` VALUES (539, '2024-12-09', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 62, 6, 9);
INSERT INTO `attendance_attendance` VALUES (540, '2024-12-09', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 63, 6, 9);
INSERT INTO `attendance_attendance` VALUES (541, '2024-12-09', '08:55:06.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 64, 6, 9);
INSERT INTO `attendance_attendance` VALUES (542, '2024-12-09', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 65, 6, 9);
INSERT INTO `attendance_attendance` VALUES (543, '2024-12-09', NULL, '17:45:07.000000', 'early', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 66, 6, 9);
INSERT INTO `attendance_attendance` VALUES (544, '2024-12-09', '08:55:01.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 67, 6, 9);
INSERT INTO `attendance_attendance` VALUES (545, '2024-12-09', '08:55:04.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 68, 7, 6);
INSERT INTO `attendance_attendance` VALUES (546, '2024-12-09', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 69, 7, 6);
INSERT INTO `attendance_attendance` VALUES (547, '2024-12-09', '08:55:05.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 70, 7, 6);
INSERT INTO `attendance_attendance` VALUES (548, '2024-12-09', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 71, 7, 6);
INSERT INTO `attendance_attendance` VALUES (549, '2024-12-09', '08:55:08.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 72, 7, 6);
INSERT INTO `attendance_attendance` VALUES (550, '2024-12-09', '09:05:26.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 73, 7, 6);
INSERT INTO `attendance_attendance` VALUES (551, '2024-12-09', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 74, 7, 6);
INSERT INTO `attendance_attendance` VALUES (552, '2024-12-09', NULL, '17:45:00.000000', 'early', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 75, 7, 6);
INSERT INTO `attendance_attendance` VALUES (553, '2024-12-09', '08:55:08.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 76, 8, 10);
INSERT INTO `attendance_attendance` VALUES (554, '2024-12-09', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 77, 8, 10);
INSERT INTO `attendance_attendance` VALUES (555, '2024-12-09', '08:55:06.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 78, 8, 10);
INSERT INTO `attendance_attendance` VALUES (556, '2024-12-09', '08:55:00.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 79, 8, 10);
INSERT INTO `attendance_attendance` VALUES (557, '2024-12-09', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 80, 8, 10);
INSERT INTO `attendance_attendance` VALUES (558, '2024-12-09', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 81, 8, 10);
INSERT INTO `attendance_attendance` VALUES (559, '2024-12-09', '08:55:03.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 82, 8, 10);
INSERT INTO `attendance_attendance` VALUES (560, '2024-12-09', '08:55:00.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 83, 8, 10);
INSERT INTO `attendance_attendance` VALUES (561, '2024-12-09', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 84, 9, 1);
INSERT INTO `attendance_attendance` VALUES (562, '2024-12-09', '09:05:13.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 85, 9, 1);
INSERT INTO `attendance_attendance` VALUES (563, '2024-12-09', '08:55:02.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 86, 9, 1);
INSERT INTO `attendance_attendance` VALUES (564, '2024-12-09', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 87, 9, 1);
INSERT INTO `attendance_attendance` VALUES (565, '2024-12-09', '08:55:00.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 88, 9, 1);
INSERT INTO `attendance_attendance` VALUES (566, '2024-12-09', '08:55:00.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 89, 10, 1);
INSERT INTO `attendance_attendance` VALUES (567, '2024-12-09', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 90, 10, 1);
INSERT INTO `attendance_attendance` VALUES (568, '2024-12-09', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 91, 1, 2);
INSERT INTO `attendance_attendance` VALUES (569, '2024-12-09', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 92, 2, 5);
INSERT INTO `attendance_attendance` VALUES (570, '2024-12-09', '08:55:00.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 93, 3, 1);
INSERT INTO `attendance_attendance` VALUES (571, '2024-12-09', '09:05:17.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 94, 6, 9);
INSERT INTO `attendance_attendance` VALUES (572, '2024-12-09', '08:55:06.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 95, 5, 8);
INSERT INTO `attendance_attendance` VALUES (573, '2024-12-09', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 96, 8, 10);
INSERT INTO `attendance_attendance` VALUES (574, '2024-12-09', '09:05:29.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 97, 7, 6);
INSERT INTO `attendance_attendance` VALUES (575, '2024-12-09', NULL, NULL, 'absent', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 98, 4, 7);
INSERT INTO `attendance_attendance` VALUES (576, '2024-12-09', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 99, 9, 1);
INSERT INTO `attendance_attendance` VALUES (577, '2024-12-09', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 100, 10, 1);
INSERT INTO `attendance_attendance` VALUES (578, '2024-12-10', '08:55:07.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 5, 1, 1);
INSERT INTO `attendance_attendance` VALUES (579, '2024-12-10', '09:05:21.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (580, '2024-12-10', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (581, '2024-12-10', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 8, 1, 2);
INSERT INTO `attendance_attendance` VALUES (582, '2024-12-10', '08:55:10.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 9, 1, 2);
INSERT INTO `attendance_attendance` VALUES (583, '2024-12-10', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 10, 1, 3);
INSERT INTO `attendance_attendance` VALUES (584, '2024-12-10', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 11, 1, 3);
INSERT INTO `attendance_attendance` VALUES (585, '2024-12-10', '08:55:07.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 12, 1, 3);
INSERT INTO `attendance_attendance` VALUES (586, '2024-12-10', '09:05:14.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 13, 1, 3);
INSERT INTO `attendance_attendance` VALUES (587, '2024-12-10', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 14, 1, 4);
INSERT INTO `attendance_attendance` VALUES (588, '2024-12-10', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 15, 1, 1);
INSERT INTO `attendance_attendance` VALUES (589, '2024-12-10', '09:05:05.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 16, 1, 1);
INSERT INTO `attendance_attendance` VALUES (590, '2024-12-10', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 17, 1, 2);
INSERT INTO `attendance_attendance` VALUES (591, '2024-12-10', '08:55:06.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 18, 1, 2);
INSERT INTO `attendance_attendance` VALUES (592, '2024-12-10', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 19, 1, 2);
INSERT INTO `attendance_attendance` VALUES (593, '2024-12-10', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 20, 1, 3);
INSERT INTO `attendance_attendance` VALUES (594, '2024-12-10', '09:05:09.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 21, 1, 3);
INSERT INTO `attendance_attendance` VALUES (595, '2024-12-10', '08:55:09.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 22, 1, 3);
INSERT INTO `attendance_attendance` VALUES (596, '2024-12-10', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 23, 1, 3);
INSERT INTO `attendance_attendance` VALUES (597, '2024-12-10', '08:55:10.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 24, 1, 4);
INSERT INTO `attendance_attendance` VALUES (598, '2024-12-10', '09:05:10.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 25, 2, 5);
INSERT INTO `attendance_attendance` VALUES (599, '2024-12-10', NULL, '17:45:09.000000', 'early', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 26, 2, 5);
INSERT INTO `attendance_attendance` VALUES (600, '2024-12-10', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 27, 2, 5);
INSERT INTO `attendance_attendance` VALUES (601, '2024-12-10', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 28, 2, 5);
INSERT INTO `attendance_attendance` VALUES (602, '2024-12-10', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 29, 2, 5);
INSERT INTO `attendance_attendance` VALUES (603, '2024-12-10', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 30, 2, 5);
INSERT INTO `attendance_attendance` VALUES (604, '2024-12-10', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 31, 2, 5);
INSERT INTO `attendance_attendance` VALUES (605, '2024-12-10', '09:05:18.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 32, 2, 5);
INSERT INTO `attendance_attendance` VALUES (606, '2024-12-10', '08:55:02.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 33, 2, 5);
INSERT INTO `attendance_attendance` VALUES (607, '2024-12-10', '08:55:01.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 34, 2, 5);
INSERT INTO `attendance_attendance` VALUES (608, '2024-12-10', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 35, 3, 1);
INSERT INTO `attendance_attendance` VALUES (609, '2024-12-10', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 36, 3, 1);
INSERT INTO `attendance_attendance` VALUES (610, '2024-12-10', '08:55:08.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 37, 3, 2);
INSERT INTO `attendance_attendance` VALUES (611, '2024-12-10', '08:55:03.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 38, 3, 2);
INSERT INTO `attendance_attendance` VALUES (612, '2024-12-10', '08:55:08.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 39, 3, 2);
INSERT INTO `attendance_attendance` VALUES (613, '2024-12-10', '08:55:06.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 40, 3, 2);
INSERT INTO `attendance_attendance` VALUES (614, '2024-12-10', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 41, 3, 3);
INSERT INTO `attendance_attendance` VALUES (615, '2024-12-10', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 42, 3, 3);
INSERT INTO `attendance_attendance` VALUES (616, '2024-12-10', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 43, 3, 3);
INSERT INTO `attendance_attendance` VALUES (617, '2024-12-10', '08:55:10.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 44, 3, 3);
INSERT INTO `attendance_attendance` VALUES (618, '2024-12-10', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 45, 4, 7);
INSERT INTO `attendance_attendance` VALUES (619, '2024-12-10', '08:55:07.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 46, 4, 7);
INSERT INTO `attendance_attendance` VALUES (620, '2024-12-10', '09:05:23.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 47, 4, 7);
INSERT INTO `attendance_attendance` VALUES (621, '2024-12-10', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 48, 4, 7);
INSERT INTO `attendance_attendance` VALUES (622, '2024-12-10', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 49, 4, 7);
INSERT INTO `attendance_attendance` VALUES (623, '2024-12-10', '08:55:01.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 50, 5, 8);
INSERT INTO `attendance_attendance` VALUES (624, '2024-12-10', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 51, 5, 8);
INSERT INTO `attendance_attendance` VALUES (625, '2024-12-10', NULL, NULL, 'absent', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 52, 5, 8);
INSERT INTO `attendance_attendance` VALUES (626, '2024-12-10', '09:05:12.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 53, 5, 8);
INSERT INTO `attendance_attendance` VALUES (627, '2024-12-10', '08:55:00.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 54, 5, 8);
INSERT INTO `attendance_attendance` VALUES (628, '2024-12-10', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 55, 5, 8);
INSERT INTO `attendance_attendance` VALUES (629, '2024-12-10', '08:55:10.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 56, 5, 8);
INSERT INTO `attendance_attendance` VALUES (630, '2024-12-10', NULL, NULL, 'absent', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 57, 5, 8);
INSERT INTO `attendance_attendance` VALUES (631, '2024-12-10', '08:55:10.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 58, 6, 9);
INSERT INTO `attendance_attendance` VALUES (632, '2024-12-10', NULL, '17:45:01.000000', 'early', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 59, 6, 9);
INSERT INTO `attendance_attendance` VALUES (633, '2024-12-10', '08:55:10.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 60, 6, 9);
INSERT INTO `attendance_attendance` VALUES (634, '2024-12-10', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 61, 6, 9);
INSERT INTO `attendance_attendance` VALUES (635, '2024-12-10', '08:55:09.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 62, 6, 9);
INSERT INTO `attendance_attendance` VALUES (636, '2024-12-10', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 63, 6, 9);
INSERT INTO `attendance_attendance` VALUES (637, '2024-12-10', '08:55:07.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 64, 6, 9);
INSERT INTO `attendance_attendance` VALUES (638, '2024-12-10', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 65, 6, 9);
INSERT INTO `attendance_attendance` VALUES (639, '2024-12-10', '08:55:10.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 66, 6, 9);
INSERT INTO `attendance_attendance` VALUES (640, '2024-12-10', '08:55:10.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 67, 6, 9);
INSERT INTO `attendance_attendance` VALUES (641, '2024-12-10', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 68, 7, 6);
INSERT INTO `attendance_attendance` VALUES (642, '2024-12-10', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 69, 7, 6);
INSERT INTO `attendance_attendance` VALUES (643, '2024-12-10', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 70, 7, 6);
INSERT INTO `attendance_attendance` VALUES (644, '2024-12-10', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 71, 7, 6);
INSERT INTO `attendance_attendance` VALUES (645, '2024-12-10', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 72, 7, 6);
INSERT INTO `attendance_attendance` VALUES (646, '2024-12-10', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 73, 7, 6);
INSERT INTO `attendance_attendance` VALUES (647, '2024-12-10', '09:05:09.000000', NULL, 'late', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 74, 7, 6);
INSERT INTO `attendance_attendance` VALUES (648, '2024-12-10', '08:55:08.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 75, 7, 6);
INSERT INTO `attendance_attendance` VALUES (649, '2024-12-10', '08:55:06.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 76, 8, 10);
INSERT INTO `attendance_attendance` VALUES (650, '2024-12-10', '08:55:02.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 77, 8, 10);
INSERT INTO `attendance_attendance` VALUES (651, '2024-12-10', '08:55:10.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 78, 8, 10);
INSERT INTO `attendance_attendance` VALUES (652, '2024-12-10', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 79, 8, 10);
INSERT INTO `attendance_attendance` VALUES (653, '2024-12-10', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 80, 8, 10);
INSERT INTO `attendance_attendance` VALUES (654, '2024-12-10', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 81, 8, 10);
INSERT INTO `attendance_attendance` VALUES (655, '2024-12-10', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:21.000000', '2026-01-24 16:13:21.000000', 82, 8, 10);
INSERT INTO `attendance_attendance` VALUES (656, '2024-12-10', '08:55:10.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 83, 8, 10);
INSERT INTO `attendance_attendance` VALUES (657, '2024-12-10', '08:55:05.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 84, 9, 1);
INSERT INTO `attendance_attendance` VALUES (658, '2024-12-10', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 85, 9, 1);
INSERT INTO `attendance_attendance` VALUES (659, '2024-12-10', '09:05:04.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 86, 9, 1);
INSERT INTO `attendance_attendance` VALUES (660, '2024-12-10', '08:55:00.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 87, 9, 1);
INSERT INTO `attendance_attendance` VALUES (661, '2024-12-10', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 88, 9, 1);
INSERT INTO `attendance_attendance` VALUES (662, '2024-12-10', '09:05:17.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 89, 10, 1);
INSERT INTO `attendance_attendance` VALUES (663, '2024-12-10', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 90, 10, 1);
INSERT INTO `attendance_attendance` VALUES (664, '2024-12-10', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 91, 1, 2);
INSERT INTO `attendance_attendance` VALUES (665, '2024-12-10', '08:55:09.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 92, 2, 5);
INSERT INTO `attendance_attendance` VALUES (666, '2024-12-10', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 93, 3, 1);
INSERT INTO `attendance_attendance` VALUES (667, '2024-12-10', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 94, 6, 9);
INSERT INTO `attendance_attendance` VALUES (668, '2024-12-10', '08:55:01.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 95, 5, 8);
INSERT INTO `attendance_attendance` VALUES (669, '2024-12-10', '09:05:06.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 96, 8, 10);
INSERT INTO `attendance_attendance` VALUES (670, '2024-12-10', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 97, 7, 6);
INSERT INTO `attendance_attendance` VALUES (671, '2024-12-10', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 98, 4, 7);
INSERT INTO `attendance_attendance` VALUES (672, '2024-12-10', '09:05:30.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 99, 9, 1);
INSERT INTO `attendance_attendance` VALUES (673, '2024-12-10', '08:55:00.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 100, 10, 1);
INSERT INTO `attendance_attendance` VALUES (674, '2024-12-11', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 5, 1, 1);
INSERT INTO `attendance_attendance` VALUES (675, '2024-12-11', '08:55:08.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (676, '2024-12-11', '08:55:03.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (677, '2024-12-11', '08:55:05.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 8, 1, 2);
INSERT INTO `attendance_attendance` VALUES (678, '2024-12-11', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 9, 1, 2);
INSERT INTO `attendance_attendance` VALUES (679, '2024-12-11', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 10, 1, 3);
INSERT INTO `attendance_attendance` VALUES (680, '2024-12-11', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 11, 1, 3);
INSERT INTO `attendance_attendance` VALUES (681, '2024-12-11', '08:55:06.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 12, 1, 3);
INSERT INTO `attendance_attendance` VALUES (682, '2024-12-11', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 13, 1, 3);
INSERT INTO `attendance_attendance` VALUES (683, '2024-12-11', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 14, 1, 4);
INSERT INTO `attendance_attendance` VALUES (684, '2024-12-11', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 15, 1, 1);
INSERT INTO `attendance_attendance` VALUES (685, '2024-12-11', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 16, 1, 1);
INSERT INTO `attendance_attendance` VALUES (686, '2024-12-11', '08:55:04.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 17, 1, 2);
INSERT INTO `attendance_attendance` VALUES (687, '2024-12-11', '08:55:10.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 18, 1, 2);
INSERT INTO `attendance_attendance` VALUES (688, '2024-12-11', '08:55:10.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 19, 1, 2);
INSERT INTO `attendance_attendance` VALUES (689, '2024-12-11', '08:55:02.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 20, 1, 3);
INSERT INTO `attendance_attendance` VALUES (690, '2024-12-11', '08:55:01.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 21, 1, 3);
INSERT INTO `attendance_attendance` VALUES (691, '2024-12-11', '08:55:07.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 22, 1, 3);
INSERT INTO `attendance_attendance` VALUES (692, '2024-12-11', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 23, 1, 3);
INSERT INTO `attendance_attendance` VALUES (693, '2024-12-11', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 24, 1, 4);
INSERT INTO `attendance_attendance` VALUES (694, '2024-12-11', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 25, 2, 5);
INSERT INTO `attendance_attendance` VALUES (695, '2024-12-11', '08:55:08.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 26, 2, 5);
INSERT INTO `attendance_attendance` VALUES (696, '2024-12-11', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 27, 2, 5);
INSERT INTO `attendance_attendance` VALUES (697, '2024-12-11', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 28, 2, 5);
INSERT INTO `attendance_attendance` VALUES (698, '2024-12-11', '08:55:10.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 29, 2, 5);
INSERT INTO `attendance_attendance` VALUES (699, '2024-12-11', '08:55:07.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 30, 2, 5);
INSERT INTO `attendance_attendance` VALUES (700, '2024-12-11', NULL, '17:45:06.000000', 'early', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 31, 2, 5);
INSERT INTO `attendance_attendance` VALUES (701, '2024-12-11', '08:55:01.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 32, 2, 5);
INSERT INTO `attendance_attendance` VALUES (702, '2024-12-11', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 33, 2, 5);
INSERT INTO `attendance_attendance` VALUES (703, '2024-12-11', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 34, 2, 5);
INSERT INTO `attendance_attendance` VALUES (704, '2024-12-11', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 35, 3, 1);
INSERT INTO `attendance_attendance` VALUES (705, '2024-12-11', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 36, 3, 1);
INSERT INTO `attendance_attendance` VALUES (706, '2024-12-11', '08:55:08.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 37, 3, 2);
INSERT INTO `attendance_attendance` VALUES (707, '2024-12-11', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 38, 3, 2);
INSERT INTO `attendance_attendance` VALUES (708, '2024-12-11', NULL, '17:45:05.000000', 'early', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 39, 3, 2);
INSERT INTO `attendance_attendance` VALUES (709, '2024-12-11', '08:55:08.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 40, 3, 2);
INSERT INTO `attendance_attendance` VALUES (710, '2024-12-11', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 41, 3, 3);
INSERT INTO `attendance_attendance` VALUES (711, '2024-12-11', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 42, 3, 3);
INSERT INTO `attendance_attendance` VALUES (712, '2024-12-11', '08:55:00.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 43, 3, 3);
INSERT INTO `attendance_attendance` VALUES (713, '2024-12-11', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 44, 3, 3);
INSERT INTO `attendance_attendance` VALUES (714, '2024-12-11', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 45, 4, 7);
INSERT INTO `attendance_attendance` VALUES (715, '2024-12-11', '08:55:00.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 46, 4, 7);
INSERT INTO `attendance_attendance` VALUES (716, '2024-12-11', '09:05:03.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 47, 4, 7);
INSERT INTO `attendance_attendance` VALUES (717, '2024-12-11', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 48, 4, 7);
INSERT INTO `attendance_attendance` VALUES (718, '2024-12-11', '08:55:02.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 49, 4, 7);
INSERT INTO `attendance_attendance` VALUES (719, '2024-12-11', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 50, 5, 8);
INSERT INTO `attendance_attendance` VALUES (720, '2024-12-11', '08:55:00.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 51, 5, 8);
INSERT INTO `attendance_attendance` VALUES (721, '2024-12-11', '08:55:03.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 52, 5, 8);
INSERT INTO `attendance_attendance` VALUES (722, '2024-12-11', '09:05:14.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 53, 5, 8);
INSERT INTO `attendance_attendance` VALUES (723, '2024-12-11', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 54, 5, 8);
INSERT INTO `attendance_attendance` VALUES (724, '2024-12-11', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 55, 5, 8);
INSERT INTO `attendance_attendance` VALUES (725, '2024-12-11', '08:55:08.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 56, 5, 8);
INSERT INTO `attendance_attendance` VALUES (726, '2024-12-11', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 57, 5, 8);
INSERT INTO `attendance_attendance` VALUES (727, '2024-12-11', '09:05:00.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 58, 6, 9);
INSERT INTO `attendance_attendance` VALUES (728, '2024-12-11', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 59, 6, 9);
INSERT INTO `attendance_attendance` VALUES (729, '2024-12-11', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 60, 6, 9);
INSERT INTO `attendance_attendance` VALUES (730, '2024-12-11', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 61, 6, 9);
INSERT INTO `attendance_attendance` VALUES (731, '2024-12-11', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 62, 6, 9);
INSERT INTO `attendance_attendance` VALUES (732, '2024-12-11', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 63, 6, 9);
INSERT INTO `attendance_attendance` VALUES (733, '2024-12-11', '08:55:01.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 64, 6, 9);
INSERT INTO `attendance_attendance` VALUES (734, '2024-12-11', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 65, 6, 9);
INSERT INTO `attendance_attendance` VALUES (735, '2024-12-11', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 66, 6, 9);
INSERT INTO `attendance_attendance` VALUES (736, '2024-12-11', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 67, 6, 9);
INSERT INTO `attendance_attendance` VALUES (737, '2024-12-11', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 68, 7, 6);
INSERT INTO `attendance_attendance` VALUES (738, '2024-12-11', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 69, 7, 6);
INSERT INTO `attendance_attendance` VALUES (739, '2024-12-11', '09:05:10.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 70, 7, 6);
INSERT INTO `attendance_attendance` VALUES (740, '2024-12-11', NULL, '17:45:07.000000', 'early', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 71, 7, 6);
INSERT INTO `attendance_attendance` VALUES (741, '2024-12-11', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 72, 7, 6);
INSERT INTO `attendance_attendance` VALUES (742, '2024-12-11', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 73, 7, 6);
INSERT INTO `attendance_attendance` VALUES (743, '2024-12-11', '08:55:05.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 74, 7, 6);
INSERT INTO `attendance_attendance` VALUES (744, '2024-12-11', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 75, 7, 6);
INSERT INTO `attendance_attendance` VALUES (745, '2024-12-11', '08:55:06.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 76, 8, 10);
INSERT INTO `attendance_attendance` VALUES (746, '2024-12-11', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 77, 8, 10);
INSERT INTO `attendance_attendance` VALUES (747, '2024-12-11', '08:55:10.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 78, 8, 10);
INSERT INTO `attendance_attendance` VALUES (748, '2024-12-11', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 79, 8, 10);
INSERT INTO `attendance_attendance` VALUES (749, '2024-12-11', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 80, 8, 10);
INSERT INTO `attendance_attendance` VALUES (750, '2024-12-11', '08:55:01.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 81, 8, 10);
INSERT INTO `attendance_attendance` VALUES (751, '2024-12-11', '08:55:08.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 82, 8, 10);
INSERT INTO `attendance_attendance` VALUES (752, '2024-12-11', '08:55:03.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 83, 8, 10);
INSERT INTO `attendance_attendance` VALUES (753, '2024-12-11', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 84, 9, 1);
INSERT INTO `attendance_attendance` VALUES (754, '2024-12-11', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 85, 9, 1);
INSERT INTO `attendance_attendance` VALUES (755, '2024-12-11', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 86, 9, 1);
INSERT INTO `attendance_attendance` VALUES (756, '2024-12-11', '09:05:27.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 87, 9, 1);
INSERT INTO `attendance_attendance` VALUES (757, '2024-12-11', '09:05:17.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 88, 9, 1);
INSERT INTO `attendance_attendance` VALUES (758, '2024-12-11', '08:55:03.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 89, 10, 1);
INSERT INTO `attendance_attendance` VALUES (759, '2024-12-11', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 90, 10, 1);
INSERT INTO `attendance_attendance` VALUES (760, '2024-12-11', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 91, 1, 2);
INSERT INTO `attendance_attendance` VALUES (761, '2024-12-11', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 92, 2, 5);
INSERT INTO `attendance_attendance` VALUES (762, '2024-12-11', '08:55:09.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 93, 3, 1);
INSERT INTO `attendance_attendance` VALUES (763, '2024-12-11', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 94, 6, 9);
INSERT INTO `attendance_attendance` VALUES (764, '2024-12-11', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 95, 5, 8);
INSERT INTO `attendance_attendance` VALUES (765, '2024-12-11', '09:05:07.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 96, 8, 10);
INSERT INTO `attendance_attendance` VALUES (766, '2024-12-11', '08:55:00.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 97, 7, 6);
INSERT INTO `attendance_attendance` VALUES (767, '2024-12-11', '08:55:07.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 98, 4, 7);
INSERT INTO `attendance_attendance` VALUES (768, '2024-12-11', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 99, 9, 1);
INSERT INTO `attendance_attendance` VALUES (769, '2024-12-11', '09:05:12.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 100, 10, 1);
INSERT INTO `attendance_attendance` VALUES (770, '2024-12-12', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 5, 1, 1);
INSERT INTO `attendance_attendance` VALUES (771, '2024-12-12', NULL, '17:45:09.000000', 'early', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (772, '2024-12-12', '08:55:00.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (773, '2024-12-12', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 8, 1, 2);
INSERT INTO `attendance_attendance` VALUES (774, '2024-12-12', '08:55:00.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 9, 1, 2);
INSERT INTO `attendance_attendance` VALUES (775, '2024-12-12', '08:55:01.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 10, 1, 3);
INSERT INTO `attendance_attendance` VALUES (776, '2024-12-12', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 11, 1, 3);
INSERT INTO `attendance_attendance` VALUES (777, '2024-12-12', '09:05:15.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 12, 1, 3);
INSERT INTO `attendance_attendance` VALUES (778, '2024-12-12', '09:05:04.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 13, 1, 3);
INSERT INTO `attendance_attendance` VALUES (779, '2024-12-12', '09:05:29.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 14, 1, 4);
INSERT INTO `attendance_attendance` VALUES (780, '2024-12-12', '08:55:00.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 15, 1, 1);
INSERT INTO `attendance_attendance` VALUES (781, '2024-12-12', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 16, 1, 1);
INSERT INTO `attendance_attendance` VALUES (782, '2024-12-12', NULL, '17:45:04.000000', 'early', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 17, 1, 2);
INSERT INTO `attendance_attendance` VALUES (783, '2024-12-12', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 18, 1, 2);
INSERT INTO `attendance_attendance` VALUES (784, '2024-12-12', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 19, 1, 2);
INSERT INTO `attendance_attendance` VALUES (785, '2024-12-12', NULL, '17:45:09.000000', 'early', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 20, 1, 3);
INSERT INTO `attendance_attendance` VALUES (786, '2024-12-12', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 21, 1, 3);
INSERT INTO `attendance_attendance` VALUES (787, '2024-12-12', '08:55:06.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 22, 1, 3);
INSERT INTO `attendance_attendance` VALUES (788, '2024-12-12', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 23, 1, 3);
INSERT INTO `attendance_attendance` VALUES (789, '2024-12-12', NULL, '17:45:03.000000', 'early', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 24, 1, 4);
INSERT INTO `attendance_attendance` VALUES (790, '2024-12-12', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 25, 2, 5);
INSERT INTO `attendance_attendance` VALUES (791, '2024-12-12', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 26, 2, 5);
INSERT INTO `attendance_attendance` VALUES (792, '2024-12-12', '08:55:10.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 27, 2, 5);
INSERT INTO `attendance_attendance` VALUES (793, '2024-12-12', '08:55:04.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 28, 2, 5);
INSERT INTO `attendance_attendance` VALUES (794, '2024-12-12', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 29, 2, 5);
INSERT INTO `attendance_attendance` VALUES (795, '2024-12-12', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 30, 2, 5);
INSERT INTO `attendance_attendance` VALUES (796, '2024-12-12', NULL, '17:45:03.000000', 'early', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 31, 2, 5);
INSERT INTO `attendance_attendance` VALUES (797, '2024-12-12', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 32, 2, 5);
INSERT INTO `attendance_attendance` VALUES (798, '2024-12-12', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 33, 2, 5);
INSERT INTO `attendance_attendance` VALUES (799, '2024-12-12', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 34, 2, 5);
INSERT INTO `attendance_attendance` VALUES (800, '2024-12-12', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 35, 3, 1);
INSERT INTO `attendance_attendance` VALUES (801, '2024-12-12', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 36, 3, 1);
INSERT INTO `attendance_attendance` VALUES (802, '2024-12-12', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 37, 3, 2);
INSERT INTO `attendance_attendance` VALUES (803, '2024-12-12', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 38, 3, 2);
INSERT INTO `attendance_attendance` VALUES (804, '2024-12-12', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 39, 3, 2);
INSERT INTO `attendance_attendance` VALUES (805, '2024-12-12', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 40, 3, 2);
INSERT INTO `attendance_attendance` VALUES (806, '2024-12-12', '08:55:10.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 41, 3, 3);
INSERT INTO `attendance_attendance` VALUES (807, '2024-12-12', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 42, 3, 3);
INSERT INTO `attendance_attendance` VALUES (808, '2024-12-12', '08:55:00.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 43, 3, 3);
INSERT INTO `attendance_attendance` VALUES (809, '2024-12-12', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 44, 3, 3);
INSERT INTO `attendance_attendance` VALUES (810, '2024-12-12', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 45, 4, 7);
INSERT INTO `attendance_attendance` VALUES (811, '2024-12-12', '09:05:23.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 46, 4, 7);
INSERT INTO `attendance_attendance` VALUES (812, '2024-12-12', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 47, 4, 7);
INSERT INTO `attendance_attendance` VALUES (813, '2024-12-12', '08:55:05.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 48, 4, 7);
INSERT INTO `attendance_attendance` VALUES (814, '2024-12-12', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 49, 4, 7);
INSERT INTO `attendance_attendance` VALUES (815, '2024-12-12', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 50, 5, 8);
INSERT INTO `attendance_attendance` VALUES (816, '2024-12-12', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 51, 5, 8);
INSERT INTO `attendance_attendance` VALUES (817, '2024-12-12', '08:55:03.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 52, 5, 8);
INSERT INTO `attendance_attendance` VALUES (818, '2024-12-12', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 53, 5, 8);
INSERT INTO `attendance_attendance` VALUES (819, '2024-12-12', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 54, 5, 8);
INSERT INTO `attendance_attendance` VALUES (820, '2024-12-12', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 55, 5, 8);
INSERT INTO `attendance_attendance` VALUES (821, '2024-12-12', '08:55:02.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 56, 5, 8);
INSERT INTO `attendance_attendance` VALUES (822, '2024-12-12', '09:05:04.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 57, 5, 8);
INSERT INTO `attendance_attendance` VALUES (823, '2024-12-12', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 58, 6, 9);
INSERT INTO `attendance_attendance` VALUES (824, '2024-12-12', NULL, NULL, 'absent', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 59, 6, 9);
INSERT INTO `attendance_attendance` VALUES (825, '2024-12-12', '09:05:09.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 60, 6, 9);
INSERT INTO `attendance_attendance` VALUES (826, '2024-12-12', '09:05:17.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 61, 6, 9);
INSERT INTO `attendance_attendance` VALUES (827, '2024-12-12', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 62, 6, 9);
INSERT INTO `attendance_attendance` VALUES (828, '2024-12-12', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 63, 6, 9);
INSERT INTO `attendance_attendance` VALUES (829, '2024-12-12', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 64, 6, 9);
INSERT INTO `attendance_attendance` VALUES (830, '2024-12-12', '09:05:21.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 65, 6, 9);
INSERT INTO `attendance_attendance` VALUES (831, '2024-12-12', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 66, 6, 9);
INSERT INTO `attendance_attendance` VALUES (832, '2024-12-12', '09:05:29.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 67, 6, 9);
INSERT INTO `attendance_attendance` VALUES (833, '2024-12-12', '08:55:02.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 68, 7, 6);
INSERT INTO `attendance_attendance` VALUES (834, '2024-12-12', '08:55:03.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 69, 7, 6);
INSERT INTO `attendance_attendance` VALUES (835, '2024-12-12', '08:55:10.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 70, 7, 6);
INSERT INTO `attendance_attendance` VALUES (836, '2024-12-12', '08:55:09.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 71, 7, 6);
INSERT INTO `attendance_attendance` VALUES (837, '2024-12-12', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 72, 7, 6);
INSERT INTO `attendance_attendance` VALUES (838, '2024-12-12', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 73, 7, 6);
INSERT INTO `attendance_attendance` VALUES (839, '2024-12-12', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 74, 7, 6);
INSERT INTO `attendance_attendance` VALUES (840, '2024-12-12', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 75, 7, 6);
INSERT INTO `attendance_attendance` VALUES (841, '2024-12-12', '08:55:08.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 76, 8, 10);
INSERT INTO `attendance_attendance` VALUES (842, '2024-12-12', '09:05:15.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 77, 8, 10);
INSERT INTO `attendance_attendance` VALUES (843, '2024-12-12', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 78, 8, 10);
INSERT INTO `attendance_attendance` VALUES (844, '2024-12-12', '08:55:02.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 79, 8, 10);
INSERT INTO `attendance_attendance` VALUES (845, '2024-12-12', '08:55:08.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 80, 8, 10);
INSERT INTO `attendance_attendance` VALUES (846, '2024-12-12', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 81, 8, 10);
INSERT INTO `attendance_attendance` VALUES (847, '2024-12-12', '08:55:01.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 82, 8, 10);
INSERT INTO `attendance_attendance` VALUES (848, '2024-12-12', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 83, 8, 10);
INSERT INTO `attendance_attendance` VALUES (849, '2024-12-12', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 84, 9, 1);
INSERT INTO `attendance_attendance` VALUES (850, '2024-12-12', '08:55:05.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 85, 9, 1);
INSERT INTO `attendance_attendance` VALUES (851, '2024-12-12', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 86, 9, 1);
INSERT INTO `attendance_attendance` VALUES (852, '2024-12-12', '08:55:07.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 87, 9, 1);
INSERT INTO `attendance_attendance` VALUES (853, '2024-12-12', '08:55:02.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 88, 9, 1);
INSERT INTO `attendance_attendance` VALUES (854, '2024-12-12', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 89, 10, 1);
INSERT INTO `attendance_attendance` VALUES (855, '2024-12-12', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 90, 10, 1);
INSERT INTO `attendance_attendance` VALUES (856, '2024-12-12', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 91, 1, 2);
INSERT INTO `attendance_attendance` VALUES (857, '2024-12-12', '08:55:01.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 92, 2, 5);
INSERT INTO `attendance_attendance` VALUES (858, '2024-12-12', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 93, 3, 1);
INSERT INTO `attendance_attendance` VALUES (859, '2024-12-12', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 94, 6, 9);
INSERT INTO `attendance_attendance` VALUES (860, '2024-12-12', '09:05:20.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 95, 5, 8);
INSERT INTO `attendance_attendance` VALUES (861, '2024-12-12', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 96, 8, 10);
INSERT INTO `attendance_attendance` VALUES (862, '2024-12-12', '08:55:05.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 97, 7, 6);
INSERT INTO `attendance_attendance` VALUES (863, '2024-12-12', '08:55:10.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 98, 4, 7);
INSERT INTO `attendance_attendance` VALUES (864, '2024-12-12', '09:05:11.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 99, 9, 1);
INSERT INTO `attendance_attendance` VALUES (865, '2024-12-12', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 100, 10, 1);
INSERT INTO `attendance_attendance` VALUES (866, '2024-12-13', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 5, 1, 1);
INSERT INTO `attendance_attendance` VALUES (867, '2024-12-13', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (868, '2024-12-13', NULL, '17:45:08.000000', 'early', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (869, '2024-12-13', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 8, 1, 2);
INSERT INTO `attendance_attendance` VALUES (870, '2024-12-13', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 9, 1, 2);
INSERT INTO `attendance_attendance` VALUES (871, '2024-12-13', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 10, 1, 3);
INSERT INTO `attendance_attendance` VALUES (872, '2024-12-13', NULL, NULL, 'absent', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 11, 1, 3);
INSERT INTO `attendance_attendance` VALUES (873, '2024-12-13', '08:55:10.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 12, 1, 3);
INSERT INTO `attendance_attendance` VALUES (874, '2024-12-13', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 13, 1, 3);
INSERT INTO `attendance_attendance` VALUES (875, '2024-12-13', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 14, 1, 4);
INSERT INTO `attendance_attendance` VALUES (876, '2024-12-13', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 15, 1, 1);
INSERT INTO `attendance_attendance` VALUES (877, '2024-12-13', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 16, 1, 1);
INSERT INTO `attendance_attendance` VALUES (878, '2024-12-13', '08:55:05.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 17, 1, 2);
INSERT INTO `attendance_attendance` VALUES (879, '2024-12-13', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 18, 1, 2);
INSERT INTO `attendance_attendance` VALUES (880, '2024-12-13', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 19, 1, 2);
INSERT INTO `attendance_attendance` VALUES (881, '2024-12-13', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 20, 1, 3);
INSERT INTO `attendance_attendance` VALUES (882, '2024-12-13', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 21, 1, 3);
INSERT INTO `attendance_attendance` VALUES (883, '2024-12-13', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 22, 1, 3);
INSERT INTO `attendance_attendance` VALUES (884, '2024-12-13', '08:55:07.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 23, 1, 3);
INSERT INTO `attendance_attendance` VALUES (885, '2024-12-13', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 24, 1, 4);
INSERT INTO `attendance_attendance` VALUES (886, '2024-12-13', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 25, 2, 5);
INSERT INTO `attendance_attendance` VALUES (887, '2024-12-13', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 26, 2, 5);
INSERT INTO `attendance_attendance` VALUES (888, '2024-12-13', '09:05:20.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 27, 2, 5);
INSERT INTO `attendance_attendance` VALUES (889, '2024-12-13', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 28, 2, 5);
INSERT INTO `attendance_attendance` VALUES (890, '2024-12-13', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 29, 2, 5);
INSERT INTO `attendance_attendance` VALUES (891, '2024-12-13', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 30, 2, 5);
INSERT INTO `attendance_attendance` VALUES (892, '2024-12-13', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 31, 2, 5);
INSERT INTO `attendance_attendance` VALUES (893, '2024-12-13', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 32, 2, 5);
INSERT INTO `attendance_attendance` VALUES (894, '2024-12-13', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 33, 2, 5);
INSERT INTO `attendance_attendance` VALUES (895, '2024-12-13', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 34, 2, 5);
INSERT INTO `attendance_attendance` VALUES (896, '2024-12-13', '08:55:02.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 35, 3, 1);
INSERT INTO `attendance_attendance` VALUES (897, '2024-12-13', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 36, 3, 1);
INSERT INTO `attendance_attendance` VALUES (898, '2024-12-13', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 37, 3, 2);
INSERT INTO `attendance_attendance` VALUES (899, '2024-12-13', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 38, 3, 2);
INSERT INTO `attendance_attendance` VALUES (900, '2024-12-13', NULL, '17:45:05.000000', 'early', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 39, 3, 2);
INSERT INTO `attendance_attendance` VALUES (901, '2024-12-13', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 40, 3, 2);
INSERT INTO `attendance_attendance` VALUES (902, '2024-12-13', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 41, 3, 3);
INSERT INTO `attendance_attendance` VALUES (903, '2024-12-13', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 42, 3, 3);
INSERT INTO `attendance_attendance` VALUES (904, '2024-12-13', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 43, 3, 3);
INSERT INTO `attendance_attendance` VALUES (905, '2024-12-13', '09:05:26.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 44, 3, 3);
INSERT INTO `attendance_attendance` VALUES (906, '2024-12-13', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 45, 4, 7);
INSERT INTO `attendance_attendance` VALUES (907, '2024-12-13', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 46, 4, 7);
INSERT INTO `attendance_attendance` VALUES (908, '2024-12-13', '08:55:01.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 47, 4, 7);
INSERT INTO `attendance_attendance` VALUES (909, '2024-12-13', '09:05:15.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 48, 4, 7);
INSERT INTO `attendance_attendance` VALUES (910, '2024-12-13', '09:05:26.000000', NULL, 'late', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 49, 4, 7);
INSERT INTO `attendance_attendance` VALUES (911, '2024-12-13', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 50, 5, 8);
INSERT INTO `attendance_attendance` VALUES (912, '2024-12-13', '08:55:09.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 51, 5, 8);
INSERT INTO `attendance_attendance` VALUES (913, '2024-12-13', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 52, 5, 8);
INSERT INTO `attendance_attendance` VALUES (914, '2024-12-13', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 53, 5, 8);
INSERT INTO `attendance_attendance` VALUES (915, '2024-12-13', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 54, 5, 8);
INSERT INTO `attendance_attendance` VALUES (916, '2024-12-13', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 55, 5, 8);
INSERT INTO `attendance_attendance` VALUES (917, '2024-12-13', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 56, 5, 8);
INSERT INTO `attendance_attendance` VALUES (918, '2024-12-13', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 57, 5, 8);
INSERT INTO `attendance_attendance` VALUES (919, '2024-12-13', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 58, 6, 9);
INSERT INTO `attendance_attendance` VALUES (920, '2024-12-13', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 59, 6, 9);
INSERT INTO `attendance_attendance` VALUES (921, '2024-12-13', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 60, 6, 9);
INSERT INTO `attendance_attendance` VALUES (922, '2024-12-13', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 61, 6, 9);
INSERT INTO `attendance_attendance` VALUES (923, '2024-12-13', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 62, 6, 9);
INSERT INTO `attendance_attendance` VALUES (924, '2024-12-13', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 63, 6, 9);
INSERT INTO `attendance_attendance` VALUES (925, '2024-12-13', NULL, '17:45:10.000000', 'early', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 64, 6, 9);
INSERT INTO `attendance_attendance` VALUES (926, '2024-12-13', NULL, NULL, 'absent', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 65, 6, 9);
INSERT INTO `attendance_attendance` VALUES (927, '2024-12-13', NULL, '17:45:08.000000', 'early', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 66, 6, 9);
INSERT INTO `attendance_attendance` VALUES (928, '2024-12-13', '08:55:08.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:22.000000', '2026-01-24 16:13:22.000000', 67, 6, 9);
INSERT INTO `attendance_attendance` VALUES (929, '2024-12-13', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 68, 7, 6);
INSERT INTO `attendance_attendance` VALUES (930, '2024-12-13', '09:05:04.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 69, 7, 6);
INSERT INTO `attendance_attendance` VALUES (931, '2024-12-13', '09:05:06.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 70, 7, 6);
INSERT INTO `attendance_attendance` VALUES (932, '2024-12-13', '08:55:05.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 71, 7, 6);
INSERT INTO `attendance_attendance` VALUES (933, '2024-12-13', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 72, 7, 6);
INSERT INTO `attendance_attendance` VALUES (934, '2024-12-13', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 73, 7, 6);
INSERT INTO `attendance_attendance` VALUES (935, '2024-12-13', '08:55:03.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 74, 7, 6);
INSERT INTO `attendance_attendance` VALUES (936, '2024-12-13', '08:55:03.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 75, 7, 6);
INSERT INTO `attendance_attendance` VALUES (937, '2024-12-13', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 76, 8, 10);
INSERT INTO `attendance_attendance` VALUES (938, '2024-12-13', '08:55:05.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 77, 8, 10);
INSERT INTO `attendance_attendance` VALUES (939, '2024-12-13', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 78, 8, 10);
INSERT INTO `attendance_attendance` VALUES (940, '2024-12-13', '08:55:10.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 79, 8, 10);
INSERT INTO `attendance_attendance` VALUES (941, '2024-12-13', '08:55:06.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 80, 8, 10);
INSERT INTO `attendance_attendance` VALUES (942, '2024-12-13', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 81, 8, 10);
INSERT INTO `attendance_attendance` VALUES (943, '2024-12-13', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 82, 8, 10);
INSERT INTO `attendance_attendance` VALUES (944, '2024-12-13', '08:55:02.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 83, 8, 10);
INSERT INTO `attendance_attendance` VALUES (945, '2024-12-13', '09:05:03.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 84, 9, 1);
INSERT INTO `attendance_attendance` VALUES (946, '2024-12-13', '08:55:01.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 85, 9, 1);
INSERT INTO `attendance_attendance` VALUES (947, '2024-12-13', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 86, 9, 1);
INSERT INTO `attendance_attendance` VALUES (948, '2024-12-13', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 87, 9, 1);
INSERT INTO `attendance_attendance` VALUES (949, '2024-12-13', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 88, 9, 1);
INSERT INTO `attendance_attendance` VALUES (950, '2024-12-13', '08:55:07.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 89, 10, 1);
INSERT INTO `attendance_attendance` VALUES (951, '2024-12-13', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 90, 10, 1);
INSERT INTO `attendance_attendance` VALUES (952, '2024-12-13', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 91, 1, 2);
INSERT INTO `attendance_attendance` VALUES (953, '2024-12-13', '08:55:06.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 92, 2, 5);
INSERT INTO `attendance_attendance` VALUES (954, '2024-12-13', '08:55:07.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 93, 3, 1);
INSERT INTO `attendance_attendance` VALUES (955, '2024-12-13', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 94, 6, 9);
INSERT INTO `attendance_attendance` VALUES (956, '2024-12-13', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 95, 5, 8);
INSERT INTO `attendance_attendance` VALUES (957, '2024-12-13', NULL, NULL, 'absent', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 96, 8, 10);
INSERT INTO `attendance_attendance` VALUES (958, '2024-12-13', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 97, 7, 6);
INSERT INTO `attendance_attendance` VALUES (959, '2024-12-13', NULL, '17:45:01.000000', 'early', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 98, 4, 7);
INSERT INTO `attendance_attendance` VALUES (960, '2024-12-13', '08:55:02.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 99, 9, 1);
INSERT INTO `attendance_attendance` VALUES (961, '2024-12-13', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 100, 10, 1);
INSERT INTO `attendance_attendance` VALUES (962, '2024-12-16', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 5, 1, 1);
INSERT INTO `attendance_attendance` VALUES (963, '2024-12-16', NULL, NULL, 'absent', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (964, '2024-12-16', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (965, '2024-12-16', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 8, 1, 2);
INSERT INTO `attendance_attendance` VALUES (966, '2024-12-16', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 9, 1, 2);
INSERT INTO `attendance_attendance` VALUES (967, '2024-12-16', '08:55:02.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 10, 1, 3);
INSERT INTO `attendance_attendance` VALUES (968, '2024-12-16', '08:55:01.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 11, 1, 3);
INSERT INTO `attendance_attendance` VALUES (969, '2024-12-16', '08:55:01.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 12, 1, 3);
INSERT INTO `attendance_attendance` VALUES (970, '2024-12-16', '08:55:06.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 13, 1, 3);
INSERT INTO `attendance_attendance` VALUES (971, '2024-12-16', '09:05:26.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 14, 1, 4);
INSERT INTO `attendance_attendance` VALUES (972, '2024-12-16', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 15, 1, 1);
INSERT INTO `attendance_attendance` VALUES (973, '2024-12-16', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 16, 1, 1);
INSERT INTO `attendance_attendance` VALUES (974, '2024-12-16', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 17, 1, 2);
INSERT INTO `attendance_attendance` VALUES (975, '2024-12-16', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 18, 1, 2);
INSERT INTO `attendance_attendance` VALUES (976, '2024-12-16', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 19, 1, 2);
INSERT INTO `attendance_attendance` VALUES (977, '2024-12-16', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 20, 1, 3);
INSERT INTO `attendance_attendance` VALUES (978, '2024-12-16', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 21, 1, 3);
INSERT INTO `attendance_attendance` VALUES (979, '2024-12-16', '08:55:10.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 22, 1, 3);
INSERT INTO `attendance_attendance` VALUES (980, '2024-12-16', NULL, '17:45:02.000000', 'early', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 23, 1, 3);
INSERT INTO `attendance_attendance` VALUES (981, '2024-12-16', '08:55:06.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 24, 1, 4);
INSERT INTO `attendance_attendance` VALUES (982, '2024-12-16', '08:55:01.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 25, 2, 5);
INSERT INTO `attendance_attendance` VALUES (983, '2024-12-16', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 26, 2, 5);
INSERT INTO `attendance_attendance` VALUES (984, '2024-12-16', '08:55:10.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 27, 2, 5);
INSERT INTO `attendance_attendance` VALUES (985, '2024-12-16', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 28, 2, 5);
INSERT INTO `attendance_attendance` VALUES (986, '2024-12-16', NULL, NULL, 'absent', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 29, 2, 5);
INSERT INTO `attendance_attendance` VALUES (987, '2024-12-16', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 30, 2, 5);
INSERT INTO `attendance_attendance` VALUES (988, '2024-12-16', '08:55:09.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 31, 2, 5);
INSERT INTO `attendance_attendance` VALUES (989, '2024-12-16', '09:05:26.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 32, 2, 5);
INSERT INTO `attendance_attendance` VALUES (990, '2024-12-16', '08:55:06.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 33, 2, 5);
INSERT INTO `attendance_attendance` VALUES (991, '2024-12-16', '08:55:05.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 34, 2, 5);
INSERT INTO `attendance_attendance` VALUES (992, '2024-12-16', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 35, 3, 1);
INSERT INTO `attendance_attendance` VALUES (993, '2024-12-16', '08:55:00.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 36, 3, 1);
INSERT INTO `attendance_attendance` VALUES (994, '2024-12-16', '08:55:00.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 37, 3, 2);
INSERT INTO `attendance_attendance` VALUES (995, '2024-12-16', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 38, 3, 2);
INSERT INTO `attendance_attendance` VALUES (996, '2024-12-16', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 39, 3, 2);
INSERT INTO `attendance_attendance` VALUES (997, '2024-12-16', '08:55:03.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 40, 3, 2);
INSERT INTO `attendance_attendance` VALUES (998, '2024-12-16', '08:55:07.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 41, 3, 3);
INSERT INTO `attendance_attendance` VALUES (999, '2024-12-16', NULL, NULL, 'absent', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 42, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1000, '2024-12-16', '08:55:06.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 43, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1001, '2024-12-16', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 44, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1002, '2024-12-16', '08:55:02.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 45, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1003, '2024-12-16', '09:05:05.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 46, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1004, '2024-12-16', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 47, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1005, '2024-12-16', '08:55:00.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 48, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1006, '2024-12-16', '09:05:22.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 49, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1007, '2024-12-16', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 50, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1008, '2024-12-16', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 51, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1009, '2024-12-16', '08:55:01.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 52, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1010, '2024-12-16', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 53, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1011, '2024-12-16', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 54, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1012, '2024-12-16', NULL, '17:45:08.000000', 'early', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 55, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1013, '2024-12-16', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 56, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1014, '2024-12-16', '09:05:05.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 57, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1015, '2024-12-16', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 58, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1016, '2024-12-16', '09:05:15.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 59, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1017, '2024-12-16', NULL, '17:45:03.000000', 'early', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 60, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1018, '2024-12-16', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 61, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1019, '2024-12-16', '08:55:01.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 62, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1020, '2024-12-16', '08:55:00.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 63, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1021, '2024-12-16', '08:55:00.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 64, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1022, '2024-12-16', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 65, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1023, '2024-12-16', '08:55:10.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 66, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1024, '2024-12-16', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 67, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1025, '2024-12-16', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 68, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1026, '2024-12-16', '08:55:02.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 69, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1027, '2024-12-16', '08:55:00.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 70, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1028, '2024-12-16', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 71, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1029, '2024-12-16', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 72, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1030, '2024-12-16', '09:05:19.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 73, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1031, '2024-12-16', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 74, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1032, '2024-12-16', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 75, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1033, '2024-12-16', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 76, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1034, '2024-12-16', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 77, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1035, '2024-12-16', '09:05:13.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 78, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1036, '2024-12-16', '08:55:09.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 79, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1037, '2024-12-16', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 80, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1038, '2024-12-16', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 81, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1039, '2024-12-16', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 82, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1040, '2024-12-16', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 83, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1041, '2024-12-16', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 84, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1042, '2024-12-16', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 85, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1043, '2024-12-16', NULL, '17:45:01.000000', 'early', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 86, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1044, '2024-12-16', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 87, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1045, '2024-12-16', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 88, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1046, '2024-12-16', '08:55:01.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 89, 10, 1);
INSERT INTO `attendance_attendance` VALUES (1047, '2024-12-16', '08:55:03.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 90, 10, 1);
INSERT INTO `attendance_attendance` VALUES (1048, '2024-12-16', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 91, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1049, '2024-12-16', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 92, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1050, '2024-12-16', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 93, 3, 1);
INSERT INTO `attendance_attendance` VALUES (1051, '2024-12-16', '08:55:06.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 94, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1052, '2024-12-16', NULL, '17:45:04.000000', 'early', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 95, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1053, '2024-12-16', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 96, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1054, '2024-12-16', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 97, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1055, '2024-12-16', '09:05:14.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 98, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1056, '2024-12-16', '08:55:04.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 99, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1057, '2024-12-16', '09:05:26.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 100, 10, 1);
INSERT INTO `attendance_attendance` VALUES (1058, '2024-12-17', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 5, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1059, '2024-12-17', NULL, '17:45:04.000000', 'early', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1060, '2024-12-17', '08:55:10.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1061, '2024-12-17', '09:05:03.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 8, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1062, '2024-12-17', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 9, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1063, '2024-12-17', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 10, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1064, '2024-12-17', '08:55:07.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 11, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1065, '2024-12-17', '08:55:02.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 12, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1066, '2024-12-17', '08:55:08.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 13, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1067, '2024-12-17', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 14, 1, 4);
INSERT INTO `attendance_attendance` VALUES (1068, '2024-12-17', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 15, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1069, '2024-12-17', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 16, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1070, '2024-12-17', '08:55:00.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 17, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1071, '2024-12-17', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 18, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1072, '2024-12-17', '08:55:02.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 19, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1073, '2024-12-17', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 20, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1074, '2024-12-17', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 21, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1075, '2024-12-17', '08:55:08.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 22, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1076, '2024-12-17', '08:55:00.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 23, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1077, '2024-12-17', '08:55:04.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 24, 1, 4);
INSERT INTO `attendance_attendance` VALUES (1078, '2024-12-17', '09:05:24.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 25, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1079, '2024-12-17', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 26, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1080, '2024-12-17', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 27, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1081, '2024-12-17', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 28, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1082, '2024-12-17', '08:55:02.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 29, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1083, '2024-12-17', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 30, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1084, '2024-12-17', '09:05:17.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 31, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1085, '2024-12-17', '08:55:00.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 32, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1086, '2024-12-17', '08:55:00.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 33, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1087, '2024-12-17', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 34, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1088, '2024-12-17', '08:55:03.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 35, 3, 1);
INSERT INTO `attendance_attendance` VALUES (1089, '2024-12-17', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 36, 3, 1);
INSERT INTO `attendance_attendance` VALUES (1090, '2024-12-17', '09:05:21.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 37, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1091, '2024-12-17', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 38, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1092, '2024-12-17', '08:55:05.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 39, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1093, '2024-12-17', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 40, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1094, '2024-12-17', '08:55:06.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 41, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1095, '2024-12-17', '09:05:04.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 42, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1096, '2024-12-17', '09:05:26.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 43, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1097, '2024-12-17', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 44, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1098, '2024-12-17', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 45, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1099, '2024-12-17', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 46, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1100, '2024-12-17', '08:55:07.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 47, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1101, '2024-12-17', '08:55:09.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 48, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1102, '2024-12-17', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 49, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1103, '2024-12-17', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 50, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1104, '2024-12-17', '08:55:09.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 51, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1105, '2024-12-17', NULL, '17:45:02.000000', 'early', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 52, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1106, '2024-12-17', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 53, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1107, '2024-12-17', '09:05:19.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 54, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1108, '2024-12-17', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 55, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1109, '2024-12-17', '08:55:01.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 56, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1110, '2024-12-17', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 57, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1111, '2024-12-17', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 58, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1112, '2024-12-17', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 59, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1113, '2024-12-17', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 60, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1114, '2024-12-17', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 61, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1115, '2024-12-17', '08:55:00.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 62, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1116, '2024-12-17', '08:55:01.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 63, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1117, '2024-12-17', '09:05:03.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 64, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1118, '2024-12-17', '08:55:05.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 65, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1119, '2024-12-17', '08:55:07.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 66, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1120, '2024-12-17', '08:55:01.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 67, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1121, '2024-12-17', '08:55:07.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 68, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1122, '2024-12-17', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 69, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1123, '2024-12-17', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 70, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1124, '2024-12-17', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 71, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1125, '2024-12-17', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 72, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1126, '2024-12-17', '08:55:06.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 73, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1127, '2024-12-17', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 74, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1128, '2024-12-17', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 75, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1129, '2024-12-17', '08:55:01.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 76, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1130, '2024-12-17', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 77, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1131, '2024-12-17', '08:55:02.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 78, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1132, '2024-12-17', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 79, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1133, '2024-12-17', '08:55:08.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 80, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1134, '2024-12-17', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 81, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1135, '2024-12-17', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 82, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1136, '2024-12-17', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 83, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1137, '2024-12-17', '09:05:17.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 84, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1138, '2024-12-17', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 85, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1139, '2024-12-17', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 86, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1140, '2024-12-17', '09:05:29.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 87, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1141, '2024-12-17', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 88, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1142, '2024-12-17', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 89, 10, 1);
INSERT INTO `attendance_attendance` VALUES (1143, '2024-12-17', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 90, 10, 1);
INSERT INTO `attendance_attendance` VALUES (1144, '2024-12-17', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 91, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1145, '2024-12-17', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 92, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1146, '2024-12-17', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 93, 3, 1);
INSERT INTO `attendance_attendance` VALUES (1147, '2024-12-17', '09:05:07.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 94, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1148, '2024-12-17', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 95, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1149, '2024-12-17', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 96, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1150, '2024-12-17', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 97, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1151, '2024-12-17', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 98, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1152, '2024-12-17', '08:55:06.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 99, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1153, '2024-12-17', NULL, NULL, 'absent', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 100, 10, 1);
INSERT INTO `attendance_attendance` VALUES (1154, '2024-12-18', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 5, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1155, '2024-12-18', '08:55:04.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1156, '2024-12-18', '08:55:00.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1157, '2024-12-18', '08:55:09.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 8, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1158, '2024-12-18', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 9, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1159, '2024-12-18', '08:55:02.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 10, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1160, '2024-12-18', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 11, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1161, '2024-12-18', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 12, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1162, '2024-12-18', '08:55:09.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 13, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1163, '2024-12-18', '08:55:09.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 14, 1, 4);
INSERT INTO `attendance_attendance` VALUES (1164, '2024-12-18', '08:55:06.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 15, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1165, '2024-12-18', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 16, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1166, '2024-12-18', '08:55:10.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 17, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1167, '2024-12-18', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 18, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1168, '2024-12-18', '08:55:07.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 19, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1169, '2024-12-18', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 20, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1170, '2024-12-18', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 21, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1171, '2024-12-18', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 22, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1172, '2024-12-18', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 23, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1173, '2024-12-18', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 24, 1, 4);
INSERT INTO `attendance_attendance` VALUES (1174, '2024-12-18', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 25, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1175, '2024-12-18', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 26, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1176, '2024-12-18', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 27, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1177, '2024-12-18', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 28, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1178, '2024-12-18', '08:55:09.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 29, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1179, '2024-12-18', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 30, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1180, '2024-12-18', '08:55:10.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 31, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1181, '2024-12-18', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 32, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1182, '2024-12-18', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 33, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1183, '2024-12-18', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 34, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1184, '2024-12-18', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 35, 3, 1);
INSERT INTO `attendance_attendance` VALUES (1185, '2024-12-18', '08:55:10.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 36, 3, 1);
INSERT INTO `attendance_attendance` VALUES (1186, '2024-12-18', '08:55:08.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 37, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1187, '2024-12-18', '08:55:02.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 38, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1188, '2024-12-18', '08:55:05.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 39, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1189, '2024-12-18', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 40, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1190, '2024-12-18', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 41, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1191, '2024-12-18', '08:55:10.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 42, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1192, '2024-12-18', '09:05:19.000000', NULL, 'late', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 43, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1193, '2024-12-18', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 44, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1194, '2024-12-18', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 45, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1195, '2024-12-18', '08:55:04.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 46, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1196, '2024-12-18', '08:55:00.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 47, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1197, '2024-12-18', '08:55:01.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 48, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1198, '2024-12-18', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 49, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1199, '2024-12-18', '08:55:02.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:23.000000', '2026-01-24 16:13:23.000000', 50, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1200, '2024-12-18', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 51, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1201, '2024-12-18', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 52, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1202, '2024-12-18', '09:05:18.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 53, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1203, '2024-12-18', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 54, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1204, '2024-12-18', '08:55:00.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 55, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1205, '2024-12-18', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 56, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1206, '2024-12-18', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 57, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1207, '2024-12-18', '08:55:10.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 58, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1208, '2024-12-18', '08:55:00.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 59, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1209, '2024-12-18', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 60, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1210, '2024-12-18', NULL, '17:45:09.000000', 'early', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 61, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1211, '2024-12-18', '09:05:14.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 62, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1212, '2024-12-18', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 63, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1213, '2024-12-18', '08:55:07.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 64, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1214, '2024-12-18', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 65, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1215, '2024-12-18', '08:55:02.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 66, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1216, '2024-12-18', NULL, '17:45:03.000000', 'early', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 67, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1217, '2024-12-18', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 68, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1218, '2024-12-18', '08:55:08.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 69, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1219, '2024-12-18', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 70, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1220, '2024-12-18', NULL, '17:45:09.000000', 'early', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 71, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1221, '2024-12-18', '09:05:17.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 72, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1222, '2024-12-18', '08:55:02.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 73, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1223, '2024-12-18', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 74, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1224, '2024-12-18', '08:55:09.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 75, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1225, '2024-12-18', '09:05:05.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 76, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1226, '2024-12-18', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 77, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1227, '2024-12-18', '08:55:04.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 78, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1228, '2024-12-18', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 79, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1229, '2024-12-18', '08:55:06.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 80, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1230, '2024-12-18', '08:55:01.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 81, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1231, '2024-12-18', '08:55:08.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 82, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1232, '2024-12-18', '08:55:06.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 83, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1233, '2024-12-18', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 84, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1234, '2024-12-18', '08:55:09.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 85, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1235, '2024-12-18', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 86, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1236, '2024-12-18', '08:55:01.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 87, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1237, '2024-12-18', NULL, '17:45:01.000000', 'early', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 88, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1238, '2024-12-18', '08:55:10.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 89, 10, 1);
INSERT INTO `attendance_attendance` VALUES (1239, '2024-12-18', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 90, 10, 1);
INSERT INTO `attendance_attendance` VALUES (1240, '2024-12-18', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 91, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1241, '2024-12-18', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 92, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1242, '2024-12-18', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 93, 3, 1);
INSERT INTO `attendance_attendance` VALUES (1243, '2024-12-18', '09:05:19.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 94, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1244, '2024-12-18', '08:55:10.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 95, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1245, '2024-12-18', '08:55:00.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 96, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1246, '2024-12-18', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 97, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1247, '2024-12-18', '08:55:02.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 98, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1248, '2024-12-18', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 99, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1249, '2024-12-18', '09:05:14.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 100, 10, 1);
INSERT INTO `attendance_attendance` VALUES (1250, '2024-12-19', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 5, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1251, '2024-12-19', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1252, '2024-12-19', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1253, '2024-12-19', '08:55:07.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 8, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1254, '2024-12-19', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 9, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1255, '2024-12-19', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 10, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1256, '2024-12-19', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 11, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1257, '2024-12-19', '09:05:05.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 12, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1258, '2024-12-19', '08:55:00.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 13, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1259, '2024-12-19', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 14, 1, 4);
INSERT INTO `attendance_attendance` VALUES (1260, '2024-12-19', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 15, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1261, '2024-12-19', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 16, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1262, '2024-12-19', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 17, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1263, '2024-12-19', '09:05:09.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 18, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1264, '2024-12-19', '08:55:10.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 19, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1265, '2024-12-19', '08:55:10.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 20, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1266, '2024-12-19', '09:05:05.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 21, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1267, '2024-12-19', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 22, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1268, '2024-12-19', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 23, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1269, '2024-12-19', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 24, 1, 4);
INSERT INTO `attendance_attendance` VALUES (1270, '2024-12-19', '08:55:08.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 25, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1271, '2024-12-19', '08:55:06.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 26, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1272, '2024-12-19', '09:05:10.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 27, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1273, '2024-12-19', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 28, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1274, '2024-12-19', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 29, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1275, '2024-12-19', NULL, '17:45:01.000000', 'early', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 30, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1276, '2024-12-19', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 31, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1277, '2024-12-19', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 32, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1278, '2024-12-19', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 33, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1279, '2024-12-19', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 34, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1280, '2024-12-19', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 35, 3, 1);
INSERT INTO `attendance_attendance` VALUES (1281, '2024-12-19', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 36, 3, 1);
INSERT INTO `attendance_attendance` VALUES (1282, '2024-12-19', '08:55:02.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 37, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1283, '2024-12-19', '09:05:29.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 38, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1284, '2024-12-19', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 39, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1285, '2024-12-19', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 40, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1286, '2024-12-19', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 41, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1287, '2024-12-19', '08:55:03.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 42, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1288, '2024-12-19', NULL, NULL, 'absent', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 43, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1289, '2024-12-19', '09:05:14.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 44, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1290, '2024-12-19', '08:55:00.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 45, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1291, '2024-12-19', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 46, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1292, '2024-12-19', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 47, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1293, '2024-12-19', '08:55:04.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 48, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1294, '2024-12-19', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 49, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1295, '2024-12-19', '08:55:04.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 50, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1296, '2024-12-19', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 51, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1297, '2024-12-19', '08:55:08.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 52, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1298, '2024-12-19', '08:55:07.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 53, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1299, '2024-12-19', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 54, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1300, '2024-12-19', '08:55:01.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 55, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1301, '2024-12-19', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 56, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1302, '2024-12-19', '08:55:07.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 57, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1303, '2024-12-19', '08:55:03.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 58, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1304, '2024-12-19', '08:55:08.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 59, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1305, '2024-12-19', '08:55:06.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 60, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1306, '2024-12-19', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 61, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1307, '2024-12-19', '08:55:01.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 62, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1308, '2024-12-19', '08:55:06.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 63, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1309, '2024-12-19', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 64, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1310, '2024-12-19', '08:55:03.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 65, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1311, '2024-12-19', '08:55:00.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 66, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1312, '2024-12-19', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 67, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1313, '2024-12-19', '08:55:02.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 68, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1314, '2024-12-19', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 69, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1315, '2024-12-19', '09:05:16.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 70, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1316, '2024-12-19', NULL, NULL, 'absent', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 71, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1317, '2024-12-19', '08:55:08.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 72, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1318, '2024-12-19', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 73, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1319, '2024-12-19', '08:55:03.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 74, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1320, '2024-12-19', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 75, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1321, '2024-12-19', '08:55:10.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 76, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1322, '2024-12-19', '08:55:02.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 77, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1323, '2024-12-19', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 78, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1324, '2024-12-19', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 79, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1325, '2024-12-19', '08:55:02.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 80, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1326, '2024-12-19', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 81, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1327, '2024-12-19', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 82, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1328, '2024-12-19', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 83, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1329, '2024-12-19', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 84, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1330, '2024-12-19', '08:55:07.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 85, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1331, '2024-12-19', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 86, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1332, '2024-12-19', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 87, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1333, '2024-12-19', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 88, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1334, '2024-12-19', '09:05:18.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 89, 10, 1);
INSERT INTO `attendance_attendance` VALUES (1335, '2024-12-19', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 90, 10, 1);
INSERT INTO `attendance_attendance` VALUES (1336, '2024-12-19', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 91, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1337, '2024-12-19', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 92, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1338, '2024-12-19', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 93, 3, 1);
INSERT INTO `attendance_attendance` VALUES (1339, '2024-12-19', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 94, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1340, '2024-12-19', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 95, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1341, '2024-12-19', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 96, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1342, '2024-12-19', '09:05:29.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 97, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1343, '2024-12-19', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 98, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1344, '2024-12-19', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 99, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1345, '2024-12-19', '09:05:28.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 100, 10, 1);
INSERT INTO `attendance_attendance` VALUES (1346, '2024-12-20', '09:05:22.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 5, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1347, '2024-12-20', '09:05:05.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1348, '2024-12-20', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1349, '2024-12-20', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 8, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1350, '2024-12-20', '09:05:11.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 9, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1351, '2024-12-20', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 10, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1352, '2024-12-20', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 11, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1353, '2024-12-20', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 12, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1354, '2024-12-20', '08:55:06.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 13, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1355, '2024-12-20', '09:05:13.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 14, 1, 4);
INSERT INTO `attendance_attendance` VALUES (1356, '2024-12-20', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 15, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1357, '2024-12-20', '08:55:00.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 16, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1358, '2024-12-20', NULL, '17:45:04.000000', 'early', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 17, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1359, '2024-12-20', '08:55:10.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 18, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1360, '2024-12-20', '08:55:01.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 19, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1361, '2024-12-20', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 20, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1362, '2024-12-20', '08:55:10.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 21, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1363, '2024-12-20', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 22, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1364, '2024-12-20', '08:55:00.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 23, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1365, '2024-12-20', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 24, 1, 4);
INSERT INTO `attendance_attendance` VALUES (1366, '2024-12-20', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 25, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1367, '2024-12-20', '08:55:00.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 26, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1368, '2024-12-20', '08:55:09.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 27, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1369, '2024-12-20', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 28, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1370, '2024-12-20', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 29, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1371, '2024-12-20', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 30, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1372, '2024-12-20', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 31, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1373, '2024-12-20', '08:55:05.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 32, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1374, '2024-12-20', '08:55:07.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 33, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1375, '2024-12-20', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 34, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1376, '2024-12-20', NULL, '17:45:01.000000', 'early', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 35, 3, 1);
INSERT INTO `attendance_attendance` VALUES (1377, '2024-12-20', '08:55:00.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 36, 3, 1);
INSERT INTO `attendance_attendance` VALUES (1378, '2024-12-20', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 37, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1379, '2024-12-20', '08:55:01.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 38, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1380, '2024-12-20', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 39, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1381, '2024-12-20', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 40, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1382, '2024-12-20', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 41, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1383, '2024-12-20', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 42, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1384, '2024-12-20', '08:55:10.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 43, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1385, '2024-12-20', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 44, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1386, '2024-12-20', '08:55:03.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 45, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1387, '2024-12-20', '09:05:25.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 46, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1388, '2024-12-20', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 47, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1389, '2024-12-20', '08:55:10.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 48, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1390, '2024-12-20', '09:05:22.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 49, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1391, '2024-12-20', NULL, '17:45:06.000000', 'early', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 50, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1392, '2024-12-20', '08:55:06.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 51, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1393, '2024-12-20', '08:55:05.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 52, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1394, '2024-12-20', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 53, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1395, '2024-12-20', NULL, '17:45:05.000000', 'early', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 54, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1396, '2024-12-20', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 55, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1397, '2024-12-20', '08:55:10.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 56, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1398, '2024-12-20', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 57, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1399, '2024-12-20', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 58, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1400, '2024-12-20', NULL, '17:45:05.000000', 'early', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 59, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1401, '2024-12-20', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 60, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1402, '2024-12-20', '08:55:08.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 61, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1403, '2024-12-20', '09:05:23.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 62, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1404, '2024-12-20', '08:55:10.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 63, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1405, '2024-12-20', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 64, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1406, '2024-12-20', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 65, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1407, '2024-12-20', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 66, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1408, '2024-12-20', '08:55:02.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 67, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1409, '2024-12-20', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 68, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1410, '2024-12-20', '08:55:03.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 69, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1411, '2024-12-20', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 70, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1412, '2024-12-20', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 71, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1413, '2024-12-20', '08:55:10.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 72, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1414, '2024-12-20', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 73, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1415, '2024-12-20', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 74, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1416, '2024-12-20', NULL, '17:45:09.000000', 'early', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 75, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1417, '2024-12-20', '08:55:10.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 76, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1418, '2024-12-20', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 77, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1419, '2024-12-20', '08:55:07.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 78, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1420, '2024-12-20', '08:55:05.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 79, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1421, '2024-12-20', '08:55:06.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 80, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1422, '2024-12-20', '08:55:09.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 81, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1423, '2024-12-20', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 82, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1424, '2024-12-20', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 83, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1425, '2024-12-20', '08:55:04.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 84, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1426, '2024-12-20', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 85, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1427, '2024-12-20', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 86, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1428, '2024-12-20', '08:55:00.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 87, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1429, '2024-12-20', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 88, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1430, '2024-12-20', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 89, 10, 1);
INSERT INTO `attendance_attendance` VALUES (1431, '2024-12-20', NULL, '17:45:03.000000', 'early', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 90, 10, 1);
INSERT INTO `attendance_attendance` VALUES (1432, '2024-12-20', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 91, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1433, '2024-12-20', '08:55:03.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 92, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1434, '2024-12-20', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 93, 3, 1);
INSERT INTO `attendance_attendance` VALUES (1435, '2024-12-20', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 94, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1436, '2024-12-20', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 95, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1437, '2024-12-20', '08:55:10.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 96, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1438, '2024-12-20', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 97, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1439, '2024-12-20', '08:55:07.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 98, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1440, '2024-12-20', '09:05:10.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 99, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1441, '2024-12-20', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 100, 10, 1);
INSERT INTO `attendance_attendance` VALUES (1442, '2024-12-23', '08:55:05.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 5, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1443, '2024-12-23', '08:55:10.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1444, '2024-12-23', '08:55:07.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1445, '2024-12-23', '09:05:16.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 8, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1446, '2024-12-23', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 9, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1447, '2024-12-23', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 10, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1448, '2024-12-23', '08:55:00.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 11, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1449, '2024-12-23', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 12, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1450, '2024-12-23', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 13, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1451, '2024-12-23', '08:55:07.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 14, 1, 4);
INSERT INTO `attendance_attendance` VALUES (1452, '2024-12-23', '09:05:26.000000', NULL, 'late', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 15, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1453, '2024-12-23', '08:55:01.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 16, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1454, '2024-12-23', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 17, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1455, '2024-12-23', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 18, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1456, '2024-12-23', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 19, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1457, '2024-12-23', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 20, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1458, '2024-12-23', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 21, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1459, '2024-12-23', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 22, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1460, '2024-12-23', '08:55:10.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 23, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1461, '2024-12-23', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 24, 1, 4);
INSERT INTO `attendance_attendance` VALUES (1462, '2024-12-23', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 25, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1463, '2024-12-23', '08:55:01.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 26, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1464, '2024-12-23', '08:55:06.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 27, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1465, '2024-12-23', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 28, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1466, '2024-12-23', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 29, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1467, '2024-12-23', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 30, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1468, '2024-12-23', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 31, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1469, '2024-12-23', '08:55:10.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 32, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1470, '2024-12-23', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 33, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1471, '2024-12-23', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:24.000000', '2026-01-24 16:13:24.000000', 34, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1472, '2024-12-23', '08:55:05.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 35, 3, 1);
INSERT INTO `attendance_attendance` VALUES (1473, '2024-12-23', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 36, 3, 1);
INSERT INTO `attendance_attendance` VALUES (1474, '2024-12-23', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 37, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1475, '2024-12-23', '08:55:02.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 38, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1476, '2024-12-23', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 39, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1477, '2024-12-23', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 40, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1478, '2024-12-23', '09:05:30.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 41, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1479, '2024-12-23', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 42, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1480, '2024-12-23', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 43, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1481, '2024-12-23', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 44, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1482, '2024-12-23', '08:55:05.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 45, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1483, '2024-12-23', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 46, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1484, '2024-12-23', '08:55:06.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 47, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1485, '2024-12-23', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 48, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1486, '2024-12-23', '09:05:16.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 49, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1487, '2024-12-23', NULL, NULL, 'absent', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 50, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1488, '2024-12-23', '08:55:08.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 51, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1489, '2024-12-23', '08:55:03.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 52, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1490, '2024-12-23', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 53, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1491, '2024-12-23', '08:55:01.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 54, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1492, '2024-12-23', '08:55:08.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 55, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1493, '2024-12-23', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 56, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1494, '2024-12-23', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 57, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1495, '2024-12-23', '08:55:00.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 58, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1496, '2024-12-23', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 59, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1497, '2024-12-23', '08:55:05.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 60, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1498, '2024-12-23', '08:55:09.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 61, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1499, '2024-12-23', '08:55:08.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 62, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1500, '2024-12-23', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 63, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1501, '2024-12-23', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 64, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1502, '2024-12-23', '08:55:05.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 65, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1503, '2024-12-23', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 66, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1504, '2024-12-23', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 67, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1505, '2024-12-23', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 68, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1506, '2024-12-23', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 69, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1507, '2024-12-23', NULL, NULL, 'absent', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 70, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1508, '2024-12-23', '08:55:04.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 71, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1509, '2024-12-23', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 72, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1510, '2024-12-23', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 73, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1511, '2024-12-23', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 74, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1512, '2024-12-23', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 75, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1513, '2024-12-23', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 76, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1514, '2024-12-23', '09:05:04.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 77, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1515, '2024-12-23', '08:55:10.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 78, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1516, '2024-12-23', '09:05:27.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 79, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1517, '2024-12-23', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 80, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1518, '2024-12-23', '09:05:30.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 81, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1519, '2024-12-23', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 82, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1520, '2024-12-23', '08:55:00.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 83, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1521, '2024-12-23', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 84, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1522, '2024-12-23', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 85, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1523, '2024-12-23', '09:05:11.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 86, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1524, '2024-12-23', '08:55:06.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 87, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1525, '2024-12-23', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 88, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1526, '2024-12-23', '08:55:08.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 89, 10, 1);
INSERT INTO `attendance_attendance` VALUES (1527, '2024-12-23', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 90, 10, 1);
INSERT INTO `attendance_attendance` VALUES (1528, '2024-12-23', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 91, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1529, '2024-12-23', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 92, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1530, '2024-12-23', '08:55:03.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 93, 3, 1);
INSERT INTO `attendance_attendance` VALUES (1531, '2024-12-23', NULL, NULL, 'absent', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 94, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1532, '2024-12-23', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 95, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1533, '2024-12-23', NULL, NULL, 'absent', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 96, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1534, '2024-12-23', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 97, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1535, '2024-12-23', '09:05:10.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 98, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1536, '2024-12-23', '09:05:20.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 99, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1537, '2024-12-23', '08:55:05.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 100, 10, 1);
INSERT INTO `attendance_attendance` VALUES (1538, '2024-12-24', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 5, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1539, '2024-12-24', '08:55:09.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1540, '2024-12-24', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1541, '2024-12-24', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 8, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1542, '2024-12-24', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 9, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1543, '2024-12-24', '09:05:22.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 10, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1544, '2024-12-24', NULL, NULL, 'absent', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 11, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1545, '2024-12-24', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 12, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1546, '2024-12-24', NULL, NULL, 'absent', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 13, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1547, '2024-12-24', '08:55:05.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 14, 1, 4);
INSERT INTO `attendance_attendance` VALUES (1548, '2024-12-24', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 15, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1549, '2024-12-24', '08:55:02.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 16, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1550, '2024-12-24', '08:55:01.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 17, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1551, '2024-12-24', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 18, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1552, '2024-12-24', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 19, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1553, '2024-12-24', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 20, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1554, '2024-12-24', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 21, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1555, '2024-12-24', '09:05:18.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 22, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1556, '2024-12-24', '08:55:01.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 23, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1557, '2024-12-24', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 24, 1, 4);
INSERT INTO `attendance_attendance` VALUES (1558, '2024-12-24', '08:55:00.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 25, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1559, '2024-12-24', '08:55:02.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 26, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1560, '2024-12-24', '08:55:08.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 27, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1561, '2024-12-24', '09:05:20.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 28, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1562, '2024-12-24', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 29, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1563, '2024-12-24', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 30, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1564, '2024-12-24', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 31, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1565, '2024-12-24', '08:55:07.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 32, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1566, '2024-12-24', NULL, '17:45:07.000000', 'early', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 33, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1567, '2024-12-24', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 34, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1568, '2024-12-24', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 35, 3, 1);
INSERT INTO `attendance_attendance` VALUES (1569, '2024-12-24', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 36, 3, 1);
INSERT INTO `attendance_attendance` VALUES (1570, '2024-12-24', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 37, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1571, '2024-12-24', '09:05:13.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 38, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1572, '2024-12-24', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 39, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1573, '2024-12-24', '08:55:05.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 40, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1574, '2024-12-24', '08:55:00.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 41, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1575, '2024-12-24', '08:55:06.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 42, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1576, '2024-12-24', '09:05:05.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 43, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1577, '2024-12-24', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 44, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1578, '2024-12-24', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 45, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1579, '2024-12-24', '08:55:02.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 46, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1580, '2024-12-24', '08:55:03.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 47, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1581, '2024-12-24', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 48, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1582, '2024-12-24', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 49, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1583, '2024-12-24', '08:55:00.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 50, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1584, '2024-12-24', '08:55:00.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 51, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1585, '2024-12-24', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 52, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1586, '2024-12-24', '08:55:00.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 53, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1587, '2024-12-24', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 54, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1588, '2024-12-24', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 55, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1589, '2024-12-24', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 56, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1590, '2024-12-24', '09:05:09.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 57, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1591, '2024-12-24', NULL, NULL, 'absent', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 58, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1592, '2024-12-24', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 59, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1593, '2024-12-24', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 60, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1594, '2024-12-24', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 61, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1595, '2024-12-24', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 62, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1596, '2024-12-24', '08:55:06.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 63, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1597, '2024-12-24', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 64, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1598, '2024-12-24', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 65, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1599, '2024-12-24', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 66, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1600, '2024-12-24', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 67, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1601, '2024-12-24', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 68, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1602, '2024-12-24', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 69, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1603, '2024-12-24', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 70, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1604, '2024-12-24', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 71, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1605, '2024-12-24', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 72, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1606, '2024-12-24', NULL, NULL, 'absent', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 73, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1607, '2024-12-24', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 74, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1608, '2024-12-24', '09:05:09.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 75, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1609, '2024-12-24', '08:55:00.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 76, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1610, '2024-12-24', '08:55:10.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 77, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1611, '2024-12-24', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 78, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1612, '2024-12-24', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 79, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1613, '2024-12-24', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 80, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1614, '2024-12-24', '09:05:25.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 81, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1615, '2024-12-24', '08:55:10.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 82, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1616, '2024-12-24', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 83, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1617, '2024-12-24', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 84, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1618, '2024-12-24', '08:55:09.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 85, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1619, '2024-12-24', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 86, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1620, '2024-12-24', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 87, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1621, '2024-12-24', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 88, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1622, '2024-12-24', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 89, 10, 1);
INSERT INTO `attendance_attendance` VALUES (1623, '2024-12-24', '08:55:10.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 90, 10, 1);
INSERT INTO `attendance_attendance` VALUES (1624, '2024-12-24', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 91, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1625, '2024-12-24', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 92, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1626, '2024-12-24', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 93, 3, 1);
INSERT INTO `attendance_attendance` VALUES (1627, '2024-12-24', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 94, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1628, '2024-12-24', '09:05:22.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 95, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1629, '2024-12-24', '08:55:10.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 96, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1630, '2024-12-24', '09:05:18.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 97, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1631, '2024-12-24', '08:55:02.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 98, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1632, '2024-12-24', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 99, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1633, '2024-12-24', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 100, 10, 1);
INSERT INTO `attendance_attendance` VALUES (1634, '2024-12-25', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 5, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1635, '2024-12-25', '08:55:03.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1636, '2024-12-25', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1637, '2024-12-25', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 8, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1638, '2024-12-25', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 9, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1639, '2024-12-25', '08:55:02.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 10, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1640, '2024-12-25', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 11, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1641, '2024-12-25', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 12, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1642, '2024-12-25', '08:55:07.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 13, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1643, '2024-12-25', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 14, 1, 4);
INSERT INTO `attendance_attendance` VALUES (1644, '2024-12-25', '08:55:08.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 15, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1645, '2024-12-25', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 16, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1646, '2024-12-25', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 17, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1647, '2024-12-25', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 18, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1648, '2024-12-25', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 19, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1649, '2024-12-25', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 20, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1650, '2024-12-25', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 21, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1651, '2024-12-25', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 22, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1652, '2024-12-25', NULL, NULL, 'absent', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 23, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1653, '2024-12-25', '08:55:00.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 24, 1, 4);
INSERT INTO `attendance_attendance` VALUES (1654, '2024-12-25', '09:05:06.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 25, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1655, '2024-12-25', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 26, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1656, '2024-12-25', '08:55:01.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 27, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1657, '2024-12-25', NULL, '17:45:00.000000', 'early', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 28, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1658, '2024-12-25', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 29, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1659, '2024-12-25', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 30, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1660, '2024-12-25', '09:05:14.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 31, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1661, '2024-12-25', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 32, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1662, '2024-12-25', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 33, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1663, '2024-12-25', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 34, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1664, '2024-12-25', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 35, 3, 1);
INSERT INTO `attendance_attendance` VALUES (1665, '2024-12-25', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 36, 3, 1);
INSERT INTO `attendance_attendance` VALUES (1666, '2024-12-25', '08:55:06.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 37, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1667, '2024-12-25', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 38, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1668, '2024-12-25', '08:55:00.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 39, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1669, '2024-12-25', '08:55:07.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 40, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1670, '2024-12-25', '08:55:08.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 41, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1671, '2024-12-25', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 42, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1672, '2024-12-25', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 43, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1673, '2024-12-25', '08:55:08.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 44, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1674, '2024-12-25', '08:55:01.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 45, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1675, '2024-12-25', NULL, NULL, 'absent', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 46, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1676, '2024-12-25', '08:55:06.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 47, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1677, '2024-12-25', '08:55:00.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 48, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1678, '2024-12-25', '08:55:07.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 49, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1679, '2024-12-25', '09:05:21.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 50, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1680, '2024-12-25', '09:05:05.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 51, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1681, '2024-12-25', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 52, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1682, '2024-12-25', '08:55:08.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 53, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1683, '2024-12-25', '08:55:05.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 54, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1684, '2024-12-25', '08:55:04.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 55, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1685, '2024-12-25', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 56, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1686, '2024-12-25', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 57, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1687, '2024-12-25', '08:55:01.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 58, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1688, '2024-12-25', '08:55:01.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 59, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1689, '2024-12-25', '08:55:10.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 60, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1690, '2024-12-25', '08:55:09.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 61, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1691, '2024-12-25', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 62, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1692, '2024-12-25', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 63, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1693, '2024-12-25', '08:55:07.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 64, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1694, '2024-12-25', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 65, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1695, '2024-12-25', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 66, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1696, '2024-12-25', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 67, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1697, '2024-12-25', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 68, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1698, '2024-12-25', '08:55:08.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 69, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1699, '2024-12-25', '09:05:23.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 70, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1700, '2024-12-25', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 71, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1701, '2024-12-25', '08:55:09.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 72, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1702, '2024-12-25', '08:55:00.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 73, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1703, '2024-12-25', NULL, NULL, 'absent', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 74, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1704, '2024-12-25', '08:55:06.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 75, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1705, '2024-12-25', NULL, NULL, 'absent', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 76, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1706, '2024-12-25', '08:55:02.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 77, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1707, '2024-12-25', '08:55:05.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 78, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1708, '2024-12-25', '08:55:02.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 79, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1709, '2024-12-25', '08:55:10.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 80, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1710, '2024-12-25', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 81, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1711, '2024-12-25', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 82, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1712, '2024-12-25', '08:55:09.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 83, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1713, '2024-12-25', '08:55:04.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 84, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1714, '2024-12-25', '08:55:00.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 85, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1715, '2024-12-25', '09:05:16.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 86, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1716, '2024-12-25', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 87, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1717, '2024-12-25', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 88, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1718, '2024-12-25', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 89, 10, 1);
INSERT INTO `attendance_attendance` VALUES (1719, '2024-12-25', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 90, 10, 1);
INSERT INTO `attendance_attendance` VALUES (1720, '2024-12-25', '08:55:08.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 91, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1721, '2024-12-25', '08:55:05.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 92, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1722, '2024-12-25', '09:05:25.000000', NULL, 'late', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 93, 3, 1);
INSERT INTO `attendance_attendance` VALUES (1723, '2024-12-25', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 94, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1724, '2024-12-25', '08:55:06.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 95, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1725, '2024-12-25', '08:55:00.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 96, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1726, '2024-12-25', '08:55:01.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 97, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1727, '2024-12-25', '08:55:00.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 98, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1728, '2024-12-25', '08:55:02.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 99, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1729, '2024-12-25', '08:55:05.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 100, 10, 1);
INSERT INTO `attendance_attendance` VALUES (1730, '2024-12-26', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 5, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1731, '2024-12-26', '08:55:09.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1732, '2024-12-26', '08:55:05.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1733, '2024-12-26', '08:55:01.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 8, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1734, '2024-12-26', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 9, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1735, '2024-12-26', '08:55:01.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 10, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1736, '2024-12-26', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 11, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1737, '2024-12-26', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 12, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1738, '2024-12-26', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 13, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1739, '2024-12-26', '08:55:02.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 14, 1, 4);
INSERT INTO `attendance_attendance` VALUES (1740, '2024-12-26', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 15, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1741, '2024-12-26', '08:55:06.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 16, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1742, '2024-12-26', '08:55:00.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 17, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1743, '2024-12-26', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:25.000000', '2026-01-24 16:13:25.000000', 18, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1744, '2024-12-26', NULL, NULL, 'absent', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 19, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1745, '2024-12-26', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 20, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1746, '2024-12-26', '08:55:00.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 21, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1747, '2024-12-26', '08:55:04.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 22, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1748, '2024-12-26', '08:55:03.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 23, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1749, '2024-12-26', '08:55:04.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 24, 1, 4);
INSERT INTO `attendance_attendance` VALUES (1750, '2024-12-26', '08:55:10.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 25, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1751, '2024-12-26', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 26, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1752, '2024-12-26', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 27, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1753, '2024-12-26', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 28, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1754, '2024-12-26', '08:55:01.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 29, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1755, '2024-12-26', '08:55:10.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 30, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1756, '2024-12-26', '09:05:27.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 31, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1757, '2024-12-26', '08:55:09.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 32, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1758, '2024-12-26', '08:55:04.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 33, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1759, '2024-12-26', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 34, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1760, '2024-12-26', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 35, 3, 1);
INSERT INTO `attendance_attendance` VALUES (1761, '2024-12-26', '08:55:10.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 36, 3, 1);
INSERT INTO `attendance_attendance` VALUES (1762, '2024-12-26', '09:05:09.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 37, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1763, '2024-12-26', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 38, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1764, '2024-12-26', '08:55:02.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 39, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1765, '2024-12-26', NULL, NULL, 'absent', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 40, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1766, '2024-12-26', '08:55:07.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 41, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1767, '2024-12-26', '08:55:06.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 42, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1768, '2024-12-26', NULL, '17:45:03.000000', 'early', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 43, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1769, '2024-12-26', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 44, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1770, '2024-12-26', '08:55:10.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 45, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1771, '2024-12-26', '08:55:10.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 46, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1772, '2024-12-26', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 47, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1773, '2024-12-26', '08:55:01.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 48, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1774, '2024-12-26', '08:55:04.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 49, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1775, '2024-12-26', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 50, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1776, '2024-12-26', '08:55:00.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 51, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1777, '2024-12-26', '08:55:06.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 52, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1778, '2024-12-26', '08:55:10.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 53, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1779, '2024-12-26', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 54, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1780, '2024-12-26', '09:05:03.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 55, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1781, '2024-12-26', '09:05:02.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 56, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1782, '2024-12-26', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 57, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1783, '2024-12-26', NULL, NULL, 'absent', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 58, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1784, '2024-12-26', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 59, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1785, '2024-12-26', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 60, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1786, '2024-12-26', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 61, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1787, '2024-12-26', '08:55:01.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 62, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1788, '2024-12-26', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 63, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1789, '2024-12-26', '08:55:06.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 64, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1790, '2024-12-26', NULL, '17:45:04.000000', 'early', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 65, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1791, '2024-12-26', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 66, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1792, '2024-12-26', '08:55:06.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 67, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1793, '2024-12-26', '08:55:10.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 68, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1794, '2024-12-26', '08:55:00.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 69, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1795, '2024-12-26', '08:55:06.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 70, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1796, '2024-12-26', '08:55:08.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 71, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1797, '2024-12-26', '08:55:03.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 72, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1798, '2024-12-26', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 73, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1799, '2024-12-26', '09:05:22.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 74, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1800, '2024-12-26', '08:55:10.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 75, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1801, '2024-12-26', '09:05:09.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 76, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1802, '2024-12-26', '09:05:18.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 77, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1803, '2024-12-26', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 78, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1804, '2024-12-26', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 79, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1805, '2024-12-26', '08:55:06.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 80, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1806, '2024-12-26', '09:05:03.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 81, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1807, '2024-12-26', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 82, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1808, '2024-12-26', '09:05:14.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 83, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1809, '2024-12-26', '08:55:06.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 84, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1810, '2024-12-26', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 85, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1811, '2024-12-26', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 86, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1812, '2024-12-26', '08:55:07.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 87, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1813, '2024-12-26', '08:55:09.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 88, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1814, '2024-12-26', '08:55:08.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 89, 10, 1);
INSERT INTO `attendance_attendance` VALUES (1815, '2024-12-26', '08:55:10.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 90, 10, 1);
INSERT INTO `attendance_attendance` VALUES (1816, '2024-12-26', '08:55:01.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 91, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1817, '2024-12-26', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 92, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1818, '2024-12-26', '08:55:00.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 93, 3, 1);
INSERT INTO `attendance_attendance` VALUES (1819, '2024-12-26', '09:05:27.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 94, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1820, '2024-12-26', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 95, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1821, '2024-12-26', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 96, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1822, '2024-12-26', '08:55:08.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 97, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1823, '2024-12-26', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 98, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1824, '2024-12-26', '08:55:07.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 99, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1825, '2024-12-26', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 100, 10, 1);
INSERT INTO `attendance_attendance` VALUES (1826, '2024-12-27', '08:55:01.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 5, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1827, '2024-12-27', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1828, '2024-12-27', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1829, '2024-12-27', '08:55:03.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 8, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1830, '2024-12-27', NULL, '17:45:09.000000', 'early', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 9, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1831, '2024-12-27', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 10, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1832, '2024-12-27', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 11, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1833, '2024-12-27', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 12, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1834, '2024-12-27', '08:55:05.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 13, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1835, '2024-12-27', '08:55:00.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 14, 1, 4);
INSERT INTO `attendance_attendance` VALUES (1836, '2024-12-27', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 15, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1837, '2024-12-27', '09:05:02.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 16, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1838, '2024-12-27', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 17, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1839, '2024-12-27', '08:55:03.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 18, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1840, '2024-12-27', '08:55:00.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 19, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1841, '2024-12-27', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 20, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1842, '2024-12-27', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 21, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1843, '2024-12-27', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 22, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1844, '2024-12-27', '08:55:09.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 23, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1845, '2024-12-27', '08:55:03.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 24, 1, 4);
INSERT INTO `attendance_attendance` VALUES (1846, '2024-12-27', '09:05:04.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 25, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1847, '2024-12-27', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 26, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1848, '2024-12-27', '08:55:03.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 27, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1849, '2024-12-27', '08:55:06.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 28, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1850, '2024-12-27', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 29, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1851, '2024-12-27', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 30, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1852, '2024-12-27', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 31, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1853, '2024-12-27', '08:55:05.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 32, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1854, '2024-12-27', '08:55:04.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 33, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1855, '2024-12-27', '08:55:10.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 34, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1856, '2024-12-27', '09:05:17.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 35, 3, 1);
INSERT INTO `attendance_attendance` VALUES (1857, '2024-12-27', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 36, 3, 1);
INSERT INTO `attendance_attendance` VALUES (1858, '2024-12-27', '08:55:02.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 37, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1859, '2024-12-27', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 38, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1860, '2024-12-27', '08:55:01.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 39, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1861, '2024-12-27', '08:55:03.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 40, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1862, '2024-12-27', '08:55:10.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 41, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1863, '2024-12-27', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 42, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1864, '2024-12-27', NULL, '17:45:07.000000', 'early', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 43, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1865, '2024-12-27', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 44, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1866, '2024-12-27', '09:05:01.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 45, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1867, '2024-12-27', '08:55:09.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 46, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1868, '2024-12-27', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 47, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1869, '2024-12-27', '08:55:03.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 48, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1870, '2024-12-27', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 49, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1871, '2024-12-27', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 50, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1872, '2024-12-27', '08:55:03.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 51, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1873, '2024-12-27', NULL, '17:45:05.000000', 'early', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 52, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1874, '2024-12-27', '08:55:01.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 53, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1875, '2024-12-27', '08:55:06.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 54, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1876, '2024-12-27', '09:05:08.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 55, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1877, '2024-12-27', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 56, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1878, '2024-12-27', '08:55:01.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 57, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1879, '2024-12-27', NULL, '17:45:03.000000', 'early', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 58, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1880, '2024-12-27', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 59, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1881, '2024-12-27', NULL, NULL, 'absent', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 60, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1882, '2024-12-27', '08:55:00.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 61, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1883, '2024-12-27', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 62, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1884, '2024-12-27', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 63, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1885, '2024-12-27', '09:05:08.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 64, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1886, '2024-12-27', '08:55:01.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 65, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1887, '2024-12-27', '08:55:08.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 66, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1888, '2024-12-27', NULL, '17:45:02.000000', 'early', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 67, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1889, '2024-12-27', '08:55:08.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 68, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1890, '2024-12-27', '08:55:00.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 69, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1891, '2024-12-27', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 70, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1892, '2024-12-27', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 71, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1893, '2024-12-27', NULL, '17:45:08.000000', 'early', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 72, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1894, '2024-12-27', '08:55:02.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 73, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1895, '2024-12-27', '09:05:28.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 74, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1896, '2024-12-27', NULL, NULL, 'absent', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 75, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1897, '2024-12-27', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 76, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1898, '2024-12-27', '08:55:06.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 77, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1899, '2024-12-27', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 78, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1900, '2024-12-27', '09:05:13.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 79, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1901, '2024-12-27', '08:55:03.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 80, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1902, '2024-12-27', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 81, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1903, '2024-12-27', '08:55:03.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 82, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1904, '2024-12-27', '09:05:07.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 83, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1905, '2024-12-27', '08:55:06.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 84, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1906, '2024-12-27', '08:55:01.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 85, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1907, '2024-12-27', '08:55:07.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 86, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1908, '2024-12-27', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 87, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1909, '2024-12-27', '08:55:08.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 88, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1910, '2024-12-27', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 89, 10, 1);
INSERT INTO `attendance_attendance` VALUES (1911, '2024-12-27', '08:55:06.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 90, 10, 1);
INSERT INTO `attendance_attendance` VALUES (1912, '2024-12-27', '08:55:06.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 91, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1913, '2024-12-27', '09:05:02.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 92, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1914, '2024-12-27', '08:55:09.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 93, 3, 1);
INSERT INTO `attendance_attendance` VALUES (1915, '2024-12-27', '08:55:08.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 94, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1916, '2024-12-27', '09:05:19.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 95, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1917, '2024-12-27', '08:55:07.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 96, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1918, '2024-12-27', '09:05:02.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 97, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1919, '2024-12-27', '08:55:04.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 98, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1920, '2024-12-27', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 99, 9, 1);
INSERT INTO `attendance_attendance` VALUES (1921, '2024-12-27', '08:55:02.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 100, 10, 1);
INSERT INTO `attendance_attendance` VALUES (1922, '2024-12-30', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 5, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1923, '2024-12-30', '09:05:27.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1924, '2024-12-30', '08:55:04.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1925, '2024-12-30', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 8, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1926, '2024-12-30', '08:55:03.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 9, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1927, '2024-12-30', '08:55:00.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 10, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1928, '2024-12-30', '08:55:01.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 11, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1929, '2024-12-30', '08:55:09.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 12, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1930, '2024-12-30', '08:55:07.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 13, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1931, '2024-12-30', '08:55:00.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 14, 1, 4);
INSERT INTO `attendance_attendance` VALUES (1932, '2024-12-30', '08:55:05.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 15, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1933, '2024-12-30', '09:05:03.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 16, 1, 1);
INSERT INTO `attendance_attendance` VALUES (1934, '2024-12-30', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 17, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1935, '2024-12-30', '08:55:02.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 18, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1936, '2024-12-30', '09:05:13.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 19, 1, 2);
INSERT INTO `attendance_attendance` VALUES (1937, '2024-12-30', '08:55:02.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 20, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1938, '2024-12-30', '08:55:06.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 21, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1939, '2024-12-30', '08:55:10.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 22, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1940, '2024-12-30', '08:55:10.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 23, 1, 3);
INSERT INTO `attendance_attendance` VALUES (1941, '2024-12-30', '08:55:08.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 24, 1, 4);
INSERT INTO `attendance_attendance` VALUES (1942, '2024-12-30', '08:55:00.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 25, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1943, '2024-12-30', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 26, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1944, '2024-12-30', '08:55:02.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 27, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1945, '2024-12-30', '08:55:09.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 28, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1946, '2024-12-30', NULL, NULL, 'absent', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 29, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1947, '2024-12-30', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 30, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1948, '2024-12-30', '08:55:09.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 31, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1949, '2024-12-30', '08:55:06.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 32, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1950, '2024-12-30', '08:55:00.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 33, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1951, '2024-12-30', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 34, 2, 5);
INSERT INTO `attendance_attendance` VALUES (1952, '2024-12-30', '08:55:10.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 35, 3, 1);
INSERT INTO `attendance_attendance` VALUES (1953, '2024-12-30', '08:55:08.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 36, 3, 1);
INSERT INTO `attendance_attendance` VALUES (1954, '2024-12-30', '09:05:15.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 37, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1955, '2024-12-30', '08:55:09.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 38, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1956, '2024-12-30', '08:55:08.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 39, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1957, '2024-12-30', '08:55:06.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 40, 3, 2);
INSERT INTO `attendance_attendance` VALUES (1958, '2024-12-30', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 41, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1959, '2024-12-30', '08:55:07.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 42, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1960, '2024-12-30', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 43, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1961, '2024-12-30', '08:55:02.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 44, 3, 3);
INSERT INTO `attendance_attendance` VALUES (1962, '2024-12-30', '08:55:07.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 45, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1963, '2024-12-30', '09:05:09.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 46, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1964, '2024-12-30', '08:55:02.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 47, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1965, '2024-12-30', '08:55:07.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 48, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1966, '2024-12-30', '08:55:01.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 49, 4, 7);
INSERT INTO `attendance_attendance` VALUES (1967, '2024-12-30', '08:55:09.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 50, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1968, '2024-12-30', '08:55:08.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 51, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1969, '2024-12-30', '09:05:05.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 52, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1970, '2024-12-30', '08:55:04.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 53, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1971, '2024-12-30', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 54, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1972, '2024-12-30', '08:55:07.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 55, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1973, '2024-12-30', '08:55:05.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 56, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1974, '2024-12-30', '08:55:04.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 57, 5, 8);
INSERT INTO `attendance_attendance` VALUES (1975, '2024-12-30', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 58, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1976, '2024-12-30', '08:55:03.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 59, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1977, '2024-12-30', '08:55:04.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 60, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1978, '2024-12-30', '08:55:05.000000', '18:05:03.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 61, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1979, '2024-12-30', '08:55:05.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 62, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1980, '2024-12-30', '08:55:02.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 63, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1981, '2024-12-30', '08:55:07.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 64, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1982, '2024-12-30', NULL, '17:45:08.000000', 'early', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 65, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1983, '2024-12-30', NULL, NULL, 'absent', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 66, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1984, '2024-12-30', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 67, 6, 9);
INSERT INTO `attendance_attendance` VALUES (1985, '2024-12-30', '08:55:07.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 68, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1986, '2024-12-30', '08:55:03.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 69, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1987, '2024-12-30', '08:55:00.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 70, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1988, '2024-12-30', '08:55:05.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 71, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1989, '2024-12-30', '08:55:07.000000', '18:05:07.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 72, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1990, '2024-12-30', '08:55:00.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 73, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1991, '2024-12-30', '08:55:02.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 74, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1992, '2024-12-30', '08:55:06.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 75, 7, 6);
INSERT INTO `attendance_attendance` VALUES (1993, '2024-12-30', '08:55:07.000000', '18:05:02.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 76, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1994, '2024-12-30', '08:55:05.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 77, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1995, '2024-12-30', '08:55:03.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 78, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1996, '2024-12-30', '08:55:10.000000', '18:05:00.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 79, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1997, '2024-12-30', '08:55:06.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 80, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1998, '2024-12-30', '08:55:08.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 81, 8, 10);
INSERT INTO `attendance_attendance` VALUES (1999, '2024-12-30', '08:55:10.000000', '18:05:10.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 82, 8, 10);
INSERT INTO `attendance_attendance` VALUES (2000, '2024-12-30', '09:05:13.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 83, 8, 10);
INSERT INTO `attendance_attendance` VALUES (2001, '2024-12-30', '08:55:05.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 84, 9, 1);
INSERT INTO `attendance_attendance` VALUES (2002, '2024-12-30', '08:55:01.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 85, 9, 1);
INSERT INTO `attendance_attendance` VALUES (2003, '2024-12-30', '08:55:10.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 86, 9, 1);
INSERT INTO `attendance_attendance` VALUES (2004, '2024-12-30', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 87, 9, 1);
INSERT INTO `attendance_attendance` VALUES (2005, '2024-12-30', '08:55:08.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 88, 9, 1);
INSERT INTO `attendance_attendance` VALUES (2006, '2024-12-30', '08:55:05.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 89, 10, 1);
INSERT INTO `attendance_attendance` VALUES (2007, '2024-12-30', '08:55:03.000000', '18:05:04.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 90, 10, 1);
INSERT INTO `attendance_attendance` VALUES (2008, '2024-12-30', NULL, NULL, 'absent', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 91, 1, 2);
INSERT INTO `attendance_attendance` VALUES (2009, '2024-12-30', '08:55:10.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 92, 2, 5);
INSERT INTO `attendance_attendance` VALUES (2010, '2024-12-30', '08:55:08.000000', '18:05:05.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 93, 3, 1);
INSERT INTO `attendance_attendance` VALUES (2011, '2024-12-30', '08:55:02.000000', '18:05:09.000000', 'normal', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 94, 6, 9);
INSERT INTO `attendance_attendance` VALUES (2012, '2024-12-30', '09:05:20.000000', NULL, 'late', '2026-01-24 16:13:26.000000', '2026-01-24 16:13:26.000000', 95, 5, 8);
INSERT INTO `attendance_attendance` VALUES (2013, '2024-12-30', '08:55:04.000000', '18:05:08.000000', 'normal', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 96, 8, 10);
INSERT INTO `attendance_attendance` VALUES (2014, '2024-12-30', NULL, '17:45:04.000000', 'early', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 97, 7, 6);
INSERT INTO `attendance_attendance` VALUES (2015, '2024-12-30', '08:55:02.000000', '18:05:06.000000', 'normal', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 98, 4, 7);
INSERT INTO `attendance_attendance` VALUES (2016, '2024-12-30', '08:55:07.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 99, 9, 1);
INSERT INTO `attendance_attendance` VALUES (2017, '2024-12-30', '08:55:10.000000', '18:05:01.000000', 'normal', '2026-01-24 16:13:27.000000', '2026-01-24 16:13:27.000000', 100, 10, 1);
INSERT INTO `attendance_attendance` VALUES (2018, '2026-01-24', '21:14:04.000000', NULL, 'late', '2026-01-24 13:14:04.775791', '2026-01-24 13:14:04.782794', 100, 10, 1);
INSERT INTO `attendance_attendance` VALUES (2019, '2026-01-25', '00:07:06.000000', '19:34:32.000000', 'normal', '2026-01-24 16:07:06.253436', '2026-01-25 11:35:56.470055', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2020, '2025-07-01', '08:55:00.000000', '18:05:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2021, '2025-07-02', '08:52:00.000000', '18:02:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2022, '2025-07-03', '08:58:00.000000', '18:08:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2023, '2025-07-04', '09:15:00.000000', '18:30:00.000000', 'late', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2024, '2025-07-07', '08:50:00.000000', '17:30:00.000000', 'early', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2025, '2025-07-01', '08:55:00.000000', '18:05:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (2026, '2025-07-02', '08:53:00.000000', '18:03:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (2027, '2025-07-03', '09:10:00.000000', '18:10:00.000000', 'late', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (2028, '2025-07-01', '08:56:00.000000', '18:06:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 8, 1, 2);
INSERT INTO `attendance_attendance` VALUES (2029, '2025-07-02', '08:51:00.000000', '18:01:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 8, 1, 2);
INSERT INTO `attendance_attendance` VALUES (2030, '2025-08-01', '08:55:00.000000', '18:05:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2031, '2025-08-04', '09:20:00.000000', '18:20:00.000000', 'late', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2032, '2025-08-05', '08:50:00.000000', '17:45:00.000000', 'early', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2033, '2025-08-06', NULL, NULL, 'absent', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2034, '2025-08-07', '08:52:00.000000', '18:02:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2035, '2025-08-01', '08:57:00.000000', '18:07:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (2036, '2025-08-02', '09:05:00.000000', '18:15:00.000000', 'late', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (2037, '2025-09-01', '08:54:00.000000', '18:04:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2038, '2025-09-02', '08:58:00.000000', '18:08:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2039, '2025-09-03', '09:12:00.000000', '18:18:00.000000', 'late', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2040, '2025-09-04', '08:55:00.000000', '17:55:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2041, '2025-09-05', '08:51:00.000000', '18:01:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2042, '2025-09-08', '09:08:00.000000', '18:08:00.000000', 'late', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2043, '2025-09-01', '08:56:00.000000', '18:06:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (2044, '2025-09-02', '08:53:00.000000', '18:03:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (2045, '2025-10-08', '08:55:00.000000', '18:05:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2046, '2025-10-09', '08:52:00.000000', '18:02:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2047, '2025-10-10', '09:15:00.000000', '18:20:00.000000', 'late', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2048, '2025-10-11', '08:50:00.000000', '17:40:00.000000', 'early', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2049, '2025-10-14', '08:58:00.000000', '18:08:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2050, '2025-10-15', '09:05:00.000000', '18:10:00.000000', 'late', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2051, '2025-10-08', '08:57:00.000000', '18:07:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (2052, '2025-10-09', '08:54:00.000000', '18:04:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (2053, '2025-11-03', '08:55:00.000000', '18:05:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2054, '2025-11-04', '08:51:00.000000', '18:01:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2055, '2025-11-05', '09:10:00.000000', '18:15:00.000000', 'late', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2056, '2025-11-06', '08:53:00.000000', '18:03:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2057, '2025-11-07', '08:56:00.000000', '18:06:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2058, '2025-11-10', '09:18:00.000000', '18:25:00.000000', 'late', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2059, '2025-11-11', '08:50:00.000000', '17:50:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2060, '2025-11-03', '08:58:00.000000', '18:08:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (2061, '2025-11-04', '08:55:00.000000', '18:05:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (2062, '2025-12-01', '08:55:00.000000', '18:05:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2063, '2025-12-02', '08:52:00.000000', '18:02:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2064, '2025-12-03', '09:08:00.000000', '18:12:00.000000', 'late', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2065, '2025-12-04', '08:54:00.000000', '18:04:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2066, '2025-12-05', '08:51:00.000000', '18:01:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2067, '2025-12-08', '09:12:00.000000', '18:18:00.000000', 'late', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2068, '2025-12-09', '08:56:00.000000', '18:06:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2069, '2025-12-10', '08:53:00.000000', '18:03:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2070, '2025-12-11', '09:05:00.000000', '18:10:00.000000', 'late', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2071, '2025-12-12', '08:50:00.000000', '17:55:00.000000', 'early', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2072, '2025-12-01', '08:57:00.000000', '18:07:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (2073, '2025-12-02', '08:55:00.000000', '18:05:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (2074, '2026-01-02', '08:55:00.000000', '18:05:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2075, '2026-01-03', '08:52:00.000000', '18:02:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2076, '2026-01-06', '09:10:00.000000', '18:15:00.000000', 'late', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2077, '2026-01-07', '08:54:00.000000', '18:04:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2078, '2026-01-08', '08:51:00.000000', '18:01:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2079, '2026-01-09', '09:15:00.000000', '18:20:00.000000', 'late', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2080, '2026-01-10', '08:56:00.000000', '18:06:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2081, '2026-01-13', '08:53:00.000000', '18:03:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2082, '2026-01-14', '09:05:00.000000', '18:10:00.000000', 'late', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2083, '2026-01-15', '08:50:00.000000', '17:50:00.000000', 'early', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2084, '2026-01-16', '08:58:00.000000', '18:08:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2085, '2026-01-17', NULL, NULL, 'absent', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2086, '2026-01-20', '08:55:00.000000', '18:05:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2087, '2026-01-21', '08:52:00.000000', '18:02:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2088, '2026-01-22', '09:08:00.000000', '18:12:00.000000', 'late', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2089, '2026-01-23', '08:54:00.000000', '18:04:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2090, '2026-01-24', '08:51:00.000000', '18:01:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 1, 1);
INSERT INTO `attendance_attendance` VALUES (2091, '2026-01-02', '08:57:00.000000', '18:07:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (2092, '2026-01-03', '08:55:00.000000', '18:05:00.000000', 'normal', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 7, 1, 2);
INSERT INTO `attendance_attendance` VALUES (2093, '2026-01-25', '20:55:51.000000', '20:55:53.000000', 'late', '2026-01-25 12:55:51.617266', '2026-01-25 12:55:53.229380', 2, NULL, NULL);

-- ----------------------------
-- Table structure for attendance_exceptionreport
-- ----------------------------
DROP TABLE IF EXISTS `attendance_exceptionreport`;
CREATE TABLE `attendance_exceptionreport`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `exception_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `date` date NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `handler_comment` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `handled_at` datetime(6) NULL DEFAULT NULL,
  `handler_id` bigint NULL DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `attendance_exception_handler_id_9f707d06_fk_accounts_`(`handler_id` ASC) USING BTREE,
  INDEX `attendance_exceptionreport_user_id_74919185_fk_accounts_user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `attendance_exception_handler_id_9f707d06_fk_accounts_` FOREIGN KEY (`handler_id`) REFERENCES `accounts_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `attendance_exceptionreport_user_id_74919185_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of attendance_exceptionreport
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 81 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
INSERT INTO `auth_permission` VALUES (77, 'Can add 异常上报', 20, 'add_exceptionreport');
INSERT INTO `auth_permission` VALUES (78, 'Can change 异常上报', 20, 'change_exceptionreport');
INSERT INTO `auth_permission` VALUES (79, 'Can delete 异常上报', 20, 'delete_exceptionreport');
INSERT INTO `auth_permission` VALUES (80, 'Can view 异常上报', 20, 'view_exceptionreport');

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
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
INSERT INTO `django_content_type` VALUES (20, 'attendance', 'exceptionreport');
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
) ENGINE = InnoDB AUTO_INCREMENT = 41 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
INSERT INTO `django_migrations` VALUES (33, 'attendance', '0002_exceptionreport', '2026-01-26 13:03:50.025386');
INSERT INTO `django_migrations` VALUES (34, 'salary', '0003_salaryexception_exception_date_and_more', '2026-01-26 13:09:16.756794');
INSERT INTO `django_migrations` VALUES (35, 'organization', '0003_add_department_to_post', '2026-01-26 15:35:37.009579');
INSERT INTO `django_migrations` VALUES (36, 'organization', '0004_alter_post_options_post_department', '2026-01-27 02:33:40.701543');
INSERT INTO `django_migrations` VALUES (37, 'attendance', '0002_attendance_checker_attendance_department_and_more', '2026-01-27 02:33:49.979945');
INSERT INTO `django_migrations` VALUES (38, 'attendance', '0003_remove_attendance_checker', '2026-01-27 02:33:50.130846');
INSERT INTO `django_migrations` VALUES (39, 'accounts', '0005_user_address_user_emergency_contact_user_id_card_and_more', '2026-01-27 04:23:38.831460');
INSERT INTO `django_migrations` VALUES (40, 'accounts', '0006_systemconfig_password_storage_mode', '2026-01-27 07:20:24.530956');

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
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 414 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
INSERT INTO `employee_employeeprofile` VALUES (31, 'EMP202401MKT031', '2024-01-25', 7500.00, 'resigned', '2025-08-15', '个人发展原因', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 3, 1, 35);
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
INSERT INTO `employee_employeeprofile` VALUES (45, 'EMP202406HR045', '2024-06-01', 9000.00, 'resigned', '2025-09-30', '家庭原因', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 4, 7, 49);
INSERT INTO `employee_employeeprofile` VALUES (46, 'EMP202401FIN046', '2024-01-10', 7500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 5, 8, 50);
INSERT INTO `employee_employeeprofile` VALUES (47, 'EMP202402FIN047', '2024-02-15', 8000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 5, 8, 51);
INSERT INTO `employee_employeeprofile` VALUES (48, 'EMP202403FIN048', '2024-03-01', 8500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 5, 8, 52);
INSERT INTO `employee_employeeprofile` VALUES (49, 'EMP202403FIN049', '2024-03-20', 8500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 5, 8, 53);
INSERT INTO `employee_employeeprofile` VALUES (50, 'EMP202404FIN050', '2024-04-05', 9000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 5, 8, 54);
INSERT INTO `employee_employeeprofile` VALUES (51, 'EMP202404FIN051', '2024-04-20', 9000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 5, 8, 55);
INSERT INTO `employee_employeeprofile` VALUES (52, 'EMP202405FIN052', '2024-05-05', 9500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 5, 8, 56);
INSERT INTO `employee_employeeprofile` VALUES (53, 'EMP202405FIN053', '2024-05-20', 10000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 5, 8, 57);
INSERT INTO `employee_employeeprofile` VALUES (54, 'EMP202401OPS054', '2024-01-20', 6500.00, 'resigned', '2025-10-20', '薪资不满意', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 6, 9, 58);
INSERT INTO `employee_employeeprofile` VALUES (55, 'EMP202402OPS055', '2024-02-10', 7000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 6, 9, 59);
INSERT INTO `employee_employeeprofile` VALUES (56, 'EMP202402OPS056', '2024-02-28', 7500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 6, 9, 60);
INSERT INTO `employee_employeeprofile` VALUES (57, 'EMP202403OPS057', '2024-03-15', 7500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 6, 9, 61);
INSERT INTO `employee_employeeprofile` VALUES (58, 'EMP202404OPS058', '2024-04-01', 8000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 6, 9, 62);
INSERT INTO `employee_employeeprofile` VALUES (59, 'EMP202404OPS059', '2024-04-15', 8000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 6, 9, 63);
INSERT INTO `employee_employeeprofile` VALUES (60, 'EMP202404OPS060', '2024-04-30', 8500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 6, 9, 64);
INSERT INTO `employee_employeeprofile` VALUES (61, 'EMP202405OPS061', '2024-05-10', 8500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 6, 9, 65);
INSERT INTO `employee_employeeprofile` VALUES (62, 'EMP202405OPS062', '2024-05-25', 9000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 6, 9, 66);
INSERT INTO `employee_employeeprofile` VALUES (63, 'EMP202406OPS063', '2024-06-05', 9000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 6, 9, 67);
INSERT INTO `employee_employeeprofile` VALUES (64, 'EMP202402DES064', '2024-02-01', 8500.00, 'resigned', '2025-11-15', '回老家发展', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 7, 6, 68);
INSERT INTO `employee_employeeprofile` VALUES (65, 'EMP202402DES065', '2024-02-20', 9000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 7, 6, 69);
INSERT INTO `employee_employeeprofile` VALUES (66, 'EMP202403DES066', '2024-03-10', 9500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 7, 6, 70);
INSERT INTO `employee_employeeprofile` VALUES (67, 'EMP202403DES067', '2024-03-25', 10000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 7, 6, 71);
INSERT INTO `employee_employeeprofile` VALUES (68, 'EMP202404DES068', '2024-04-10', 10000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 7, 6, 72);
INSERT INTO `employee_employeeprofile` VALUES (69, 'EMP202404DES069', '2024-04-25', 10500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 7, 6, 73);
INSERT INTO `employee_employeeprofile` VALUES (70, 'EMP202405DES070', '2024-05-05', 10500.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 7, 6, 74);
INSERT INTO `employee_employeeprofile` VALUES (71, 'EMP202405DES071', '2024-05-20', 11000.00, 'active', NULL, '', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 7, 6, 75);
INSERT INTO `employee_employeeprofile` VALUES (72, 'EMP202401CS072', '2024-01-15', 5500.00, 'resigned', '2025-12-31', '合同到期不续签', '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000', 8, 10, 76);
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
INSERT INTO `employee_employeeprofile` VALUES (101, 'EMP202507TECH101', '2025-07-01', 12000.00, 'active', NULL, '', '2026-01-25 19:50:34.000000', '2026-01-25 19:50:34.000000', 1, 3, 101);
INSERT INTO `employee_employeeprofile` VALUES (102, 'EMP202507TECH102', '2025-07-15', 11000.00, 'active', NULL, '', '2026-01-25 19:50:34.000000', '2026-01-25 19:50:34.000000', 1, 2, 102);
INSERT INTO `employee_employeeprofile` VALUES (103, 'EMP202508TECH103', '2025-08-01', 11500.00, 'active', NULL, '', '2026-01-25 19:50:34.000000', '2026-01-25 19:50:34.000000', 1, 3, 103);
INSERT INTO `employee_employeeprofile` VALUES (104, 'EMP202509TECH104', '2025-09-01', 12000.00, 'active', NULL, '', '2026-01-25 19:50:34.000000', '2026-01-25 19:50:34.000000', 1, 3, 104);
INSERT INTO `employee_employeeprofile` VALUES (105, 'EMP202510TECH105', '2025-10-01', 12500.00, 'active', NULL, '', '2026-01-25 19:50:34.000000', '2026-01-25 19:50:34.000000', 1, 3, 105);
INSERT INTO `employee_employeeprofile` VALUES (106, 'EMP202511TECH106', '2025-11-01', 12000.00, 'active', NULL, '', '2026-01-25 19:50:34.000000', '2026-01-25 19:50:34.000000', 1, 3, 106);
INSERT INTO `employee_employeeprofile` VALUES (107, 'EMP202512TECH107', '2025-12-01', 13000.00, 'active', NULL, '', '2026-01-25 19:50:34.000000', '2026-01-25 19:50:34.000000', 1, 4, 107);
INSERT INTO `employee_employeeprofile` VALUES (108, 'EMP202601TECH108', '2026-01-05', 11500.00, 'active', NULL, '', '2026-01-25 19:50:34.000000', '2026-01-25 19:50:34.000000', 1, 2, 108);
INSERT INTO `employee_employeeprofile` VALUES (109, 'EMP202507PRD109', '2025-07-10', 13000.00, 'active', NULL, '', '2026-01-25 19:50:34.000000', '2026-01-25 19:50:34.000000', 2, 5, 109);
INSERT INTO `employee_employeeprofile` VALUES (110, 'EMP202509PRD110', '2025-09-15', 13500.00, 'active', NULL, '', '2026-01-25 19:50:34.000000', '2026-01-25 19:50:34.000000', 2, 5, 110);
INSERT INTO `employee_employeeprofile` VALUES (111, 'EMP202511PRD111', '2025-11-01', 14000.00, 'active', NULL, '', '2026-01-25 19:50:34.000000', '2026-01-25 19:50:34.000000', 2, 5, 111);
INSERT INTO `employee_employeeprofile` VALUES (112, 'EMP202508MKT112', '2025-08-01', 10000.00, 'active', NULL, '', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 3, 1, 112);
INSERT INTO `employee_employeeprofile` VALUES (113, 'EMP202510MKT113', '2025-10-01', 10500.00, 'active', NULL, '', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 3, 2, 113);
INSERT INTO `employee_employeeprofile` VALUES (114, 'EMP202507OPS114', '2025-07-20', 9000.00, 'active', NULL, '', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 9, 114);
INSERT INTO `employee_employeeprofile` VALUES (115, 'EMP202512OPS115', '2025-12-01', 9500.00, 'active', NULL, '', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 6, 9, 115);
INSERT INTO `employee_employeeprofile` VALUES (116, 'EMP202509DES116', '2025-09-01', 11500.00, 'active', NULL, '', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 7, 6, 116);
INSERT INTO `employee_employeeprofile` VALUES (117, 'EMP202508FIN117', '2025-08-15', 10000.00, 'active', NULL, '', '2026-01-25 19:50:35.000000', '2026-01-25 19:50:35.000000', 5, 8, 117);
INSERT INTO `employee_employeeprofile` VALUES (118, 'EMP202601LEG002', '2026-01-18', 11614.72, 'active', NULL, '', '2026-01-13 00:00:00.000000', '2026-01-24 00:00:00.000000', 10, 7, 122);
INSERT INTO `employee_employeeprofile` VALUES (119, 'EMP202601HR002', '2024-01-08', 8590.42, 'active', NULL, '', '2026-01-17 00:00:00.000000', '2026-01-24 02:00:00.000000', 4, 9, 123);
INSERT INTO `employee_employeeprofile` VALUES (120, 'EMP202601TECH001', '2026-01-03', 11933.20, 'active', NULL, '', '2026-01-16 00:00:00.000000', '2026-01-24 05:00:00.000000', 1, 9, 124);
INSERT INTO `employee_employeeprofile` VALUES (121, 'EMP202601HR003', '2020-12-17', 19453.36, 'active', NULL, '', '2026-01-05 00:00:00.000000', '2026-01-23 14:00:00.000000', 4, 5, 125);
INSERT INTO `employee_employeeprofile` VALUES (122, 'EMP202601ADM001', '2026-01-19', 14305.00, 'active', NULL, '', '2026-01-17 00:00:00.000000', '2026-01-23 03:00:00.000000', 9, 5, 126);
INSERT INTO `employee_employeeprofile` VALUES (123, 'EMP202601CS001', '2021-09-28', 7048.12, 'active', NULL, '', '2025-12-26 00:00:00.000000', '2026-01-24 16:00:00.000000', 8, 10, 127);
INSERT INTO `employee_employeeprofile` VALUES (124, 'EMP202601FIN001', '2025-03-01', 36328.09, 'resigned', '2026-01-01', '个人发展', '2026-01-11 00:00:00.000000', '2026-01-23 01:00:00.000000', 5, 4, 128);
INSERT INTO `employee_employeeprofile` VALUES (125, 'EMP202601FIN002', '2023-09-16', 7932.83, 'active', NULL, '', '2026-01-05 00:00:00.000000', '2026-01-24 05:00:00.000000', 5, 10, 129);
INSERT INTO `employee_employeeprofile` VALUES (126, 'EMP202601PRD001', '2026-01-23', 15686.83, 'active', NULL, '', '2026-01-16 00:00:00.000000', '2026-01-23 09:00:00.000000', 2, 3, 130);
INSERT INTO `employee_employeeprofile` VALUES (127, 'EMP202601TECH002', '2025-01-30', 11811.39, 'resigned', '2026-01-23', '工作地点远', '2025-12-30 00:00:00.000000', '2026-01-24 16:00:00.000000', 1, 6, 131);
INSERT INTO `employee_employeeprofile` VALUES (128, 'EMP202601LEG003', '2021-01-18', 8121.25, 'active', NULL, '', '2025-12-29 00:00:00.000000', '2026-01-24 14:00:00.000000', 10, 8, 132);
INSERT INTO `employee_employeeprofile` VALUES (129, 'EMP202601LEG004', '2024-11-01', 16560.65, 'resigned', '2026-01-24', '家庭原因', '2025-12-31 00:00:00.000000', '2026-01-23 21:00:00.000000', 10, 5, 133);
INSERT INTO `employee_employeeprofile` VALUES (130, 'EMP202601HR004', '2024-11-16', 19550.57, 'active', NULL, '', '2026-01-06 00:00:00.000000', '2026-01-23 01:00:00.000000', 4, 3, 134);
INSERT INTO `employee_employeeprofile` VALUES (131, 'EMP202601PRD002', '2026-01-25', 7928.69, 'active', NULL, '', '2026-01-02 00:00:00.000000', '2026-01-23 11:00:00.000000', 2, 9, 135);
INSERT INTO `employee_employeeprofile` VALUES (132, 'EMP202601TECH003', '2025-04-30', 13180.31, 'resigned', '2026-01-08', '家庭原因', '2026-01-11 00:00:00.000000', '2026-01-24 17:00:00.000000', 1, 6, 136);
INSERT INTO `employee_employeeprofile` VALUES (133, 'EMP202601FIN003', '2022-01-02', 16289.44, 'active', NULL, '', '2026-01-07 00:00:00.000000', '2026-01-24 13:00:00.000000', 5, 6, 137);
INSERT INTO `employee_employeeprofile` VALUES (134, 'EMP202601CS002', '2024-09-29', 12212.39, 'active', NULL, '', '2025-12-28 00:00:00.000000', '2026-01-24 09:00:00.000000', 8, 2, 138);
INSERT INTO `employee_employeeprofile` VALUES (135, 'EMP202601TECH004', '2020-09-05', 8699.66, 'active', NULL, '', '2025-12-31 00:00:00.000000', '2026-01-24 04:00:00.000000', 1, 10, 139);
INSERT INTO `employee_employeeprofile` VALUES (136, 'EMP202601HR005', '2021-01-12', 10149.78, 'active', NULL, '', '2026-01-22 00:00:00.000000', '2026-01-23 16:00:00.000000', 4, 8, 140);
INSERT INTO `employee_employeeprofile` VALUES (137, 'EMP202601MKT002', '2022-12-17', 6305.59, 'active', NULL, '', '2026-01-16 00:00:00.000000', '2026-01-24 12:00:00.000000', 3, 1, 141);
INSERT INTO `employee_employeeprofile` VALUES (138, 'EMP202601LEG005', '2022-10-01', 10230.60, 'active', NULL, '', '2026-01-17 00:00:00.000000', '2026-01-24 06:00:00.000000', 10, 9, 142);
INSERT INTO `employee_employeeprofile` VALUES (139, 'EMP202601OPS002', '2024-11-01', 7799.77, 'resigned', '2026-01-03', '其他', '2026-01-25 00:00:00.000000', '2026-01-24 19:00:00.000000', 6, 7, 143);
INSERT INTO `employee_employeeprofile` VALUES (140, 'EMP202601CS003', '2023-11-22', 22225.92, 'active', NULL, '', '2026-01-22 00:00:00.000000', '2026-01-24 22:00:00.000000', 8, 3, 144);
INSERT INTO `employee_employeeprofile` VALUES (141, 'EMP202601CS004', '2023-01-02', 11730.81, 'active', NULL, '', '2025-12-28 00:00:00.000000', '2026-01-24 18:00:00.000000', 8, 9, 145);
INSERT INTO `employee_employeeprofile` VALUES (142, 'EMP202601PRD003', '2026-01-17', 9673.52, 'active', NULL, '', '2026-01-02 00:00:00.000000', '2026-01-23 15:00:00.000000', 2, 9, 146);
INSERT INTO `employee_employeeprofile` VALUES (143, 'EMP202601TECH005', '2026-01-12', 30484.78, 'active', NULL, '', '2026-01-18 00:00:00.000000', '2026-01-23 17:00:00.000000', 1, 4, 147);
INSERT INTO `employee_employeeprofile` VALUES (144, 'EMP202601OPS003', '2020-11-10', 21592.72, 'active', NULL, '', '2026-01-22 00:00:00.000000', '2026-01-23 06:00:00.000000', 6, 3, 148);
INSERT INTO `employee_employeeprofile` VALUES (145, 'EMP202601PRD004', '2024-01-26', 19715.84, 'active', NULL, '', '2026-01-15 00:00:00.000000', '2026-01-24 18:00:00.000000', 2, 3, 149);
INSERT INTO `employee_employeeprofile` VALUES (146, 'EMP202601CS005', '2026-01-20', 12076.33, 'active', NULL, '', '2026-01-21 00:00:00.000000', '2026-01-24 10:00:00.000000', 8, 8, 150);
INSERT INTO `employee_employeeprofile` VALUES (147, 'EMP202601OPS004', '2024-08-03', 14874.39, 'resigned', '2026-01-25', '个人发展', '2026-01-20 00:00:00.000000', '2026-01-23 04:00:00.000000', 6, 2, 151);
INSERT INTO `employee_employeeprofile` VALUES (148, 'EMP202601OPS005', '2026-01-09', 8119.28, 'active', NULL, '', '2026-01-15 00:00:00.000000', '2026-01-23 00:00:00.000000', 6, 10, 152);
INSERT INTO `employee_employeeprofile` VALUES (149, 'EMP202601FIN004', '2026-01-10', 11481.91, 'active', NULL, '', '2026-01-10 00:00:00.000000', '2026-01-24 06:00:00.000000', 5, 2, 153);
INSERT INTO `employee_employeeprofile` VALUES (150, 'EMP202601ADM002', '2024-11-09', 9352.05, 'active', NULL, '', '2026-01-14 00:00:00.000000', '2026-01-23 15:00:00.000000', 9, 9, 154);
INSERT INTO `employee_employeeprofile` VALUES (151, 'EMP202601OPS006', '2020-11-29', 9258.35, 'active', NULL, '', '2026-01-03 00:00:00.000000', '2026-01-24 21:00:00.000000', 6, 7, 155);
INSERT INTO `employee_employeeprofile` VALUES (152, 'EMP202601LEG006', '2021-11-04', 11889.09, 'active', NULL, '', '2026-01-11 00:00:00.000000', '2026-01-23 14:00:00.000000', 10, 8, 156);
INSERT INTO `employee_employeeprofile` VALUES (153, 'EMP202601ADM003', '2023-12-17', 15409.89, 'active', NULL, '', '2026-01-02 00:00:00.000000', '2026-01-24 14:00:00.000000', 9, 5, 157);
INSERT INTO `employee_employeeprofile` VALUES (154, 'EMP202601HR006', '2023-10-21', 7663.29, 'active', NULL, '', '2026-01-08 00:00:00.000000', '2026-01-24 00:00:00.000000', 4, 1, 158);
INSERT INTO `employee_employeeprofile` VALUES (155, 'EMP202601TECH006', '2021-10-08', 23453.58, 'active', NULL, '', '2026-01-17 00:00:00.000000', '2026-01-23 20:00:00.000000', 1, 3, 159);
INSERT INTO `employee_employeeprofile` VALUES (156, 'EMP202601PRD005', '2026-01-14', 7620.90, 'active', NULL, '', '2025-12-27 00:00:00.000000', '2026-01-24 15:00:00.000000', 2, 1, 160);
INSERT INTO `employee_employeeprofile` VALUES (157, 'EMP202601ADM004', '2021-08-12', 20192.54, 'active', NULL, '', '2026-01-13 00:00:00.000000', '2026-01-24 09:00:00.000000', 9, 3, 161);
INSERT INTO `employee_employeeprofile` VALUES (158, 'EMP202601CS006', '2026-01-13', 9655.69, 'active', NULL, '', '2026-01-13 00:00:00.000000', '2026-01-24 21:00:00.000000', 8, 1, 162);
INSERT INTO `employee_employeeprofile` VALUES (159, 'EMP202601LEG007', '2024-12-31', 11896.64, 'resigned', '2026-01-08', '薪资不满意', '2026-01-05 00:00:00.000000', '2026-01-23 06:00:00.000000', 10, 10, 163);
INSERT INTO `employee_employeeprofile` VALUES (160, 'EMP202601ADM005', '2024-10-04', 12270.35, 'active', NULL, '', '2026-01-19 00:00:00.000000', '2026-01-24 15:00:00.000000', 9, 8, 164);
INSERT INTO `employee_employeeprofile` VALUES (161, 'EMP202601CS007', '2024-09-03', 10321.05, 'active', NULL, '', '2025-12-31 00:00:00.000000', '2026-01-24 20:00:00.000000', 8, 7, 165);
INSERT INTO `employee_employeeprofile` VALUES (162, 'EMP202601LEG008', '2021-11-17', 10437.87, 'active', NULL, '', '2026-01-14 00:00:00.000000', '2026-01-23 01:00:00.000000', 10, 8, 166);
INSERT INTO `employee_employeeprofile` VALUES (163, 'EMP202601OPS007', '2026-01-06', 10258.53, 'active', NULL, '', '2026-01-24 00:00:00.000000', '2026-01-23 03:00:00.000000', 6, 8, 167);
INSERT INTO `employee_employeeprofile` VALUES (164, 'EMP202601DES001', '2021-09-01', 13459.77, 'active', NULL, '', '2026-01-20 00:00:00.000000', '2026-01-23 08:00:00.000000', 7, 5, 168);
INSERT INTO `employee_employeeprofile` VALUES (165, 'EMP202601CS008', '2023-08-26', 7705.63, 'active', NULL, '', '2026-01-08 00:00:00.000000', '2026-01-24 09:00:00.000000', 8, 10, 169);
INSERT INTO `employee_employeeprofile` VALUES (166, 'EMP202601TECH007', '2024-08-03', 8107.85, 'resigned', '2026-01-25', '家庭原因', '2026-01-17 00:00:00.000000', '2026-01-24 00:00:00.000000', 1, 10, 170);
INSERT INTO `employee_employeeprofile` VALUES (167, 'EMP202601CS009', '2023-10-18', 8942.28, 'active', NULL, '', '2025-12-26 00:00:00.000000', '2026-01-23 14:00:00.000000', 8, 7, 171);
INSERT INTO `employee_employeeprofile` VALUES (168, 'EMP202601CS010', '2023-12-04', 11423.99, 'active', NULL, '', '2026-01-07 00:00:00.000000', '2026-01-23 00:00:00.000000', 8, 10, 172);
INSERT INTO `employee_employeeprofile` VALUES (169, 'EMP202601ADM006', '2026-01-20', 15280.66, 'active', NULL, '', '2025-12-26 00:00:00.000000', '2026-01-24 14:00:00.000000', 9, 3, 173);
INSERT INTO `employee_employeeprofile` VALUES (170, 'EMP202601LEG009', '2023-10-15', 21182.90, 'active', NULL, '', '2026-01-01 00:00:00.000000', '2026-01-24 18:00:00.000000', 10, 3, 174);
INSERT INTO `employee_employeeprofile` VALUES (171, 'EMP202601OPS008', '2021-09-28', 17866.32, 'active', NULL, '', '2026-01-01 00:00:00.000000', '2026-01-24 22:00:00.000000', 6, 3, 175);
INSERT INTO `employee_employeeprofile` VALUES (172, 'EMP202601HR007', '2024-08-14', 11949.67, 'active', NULL, '', '2025-12-31 00:00:00.000000', '2026-01-23 09:00:00.000000', 4, 8, 176);
INSERT INTO `employee_employeeprofile` VALUES (173, 'EMP202601LEG010', '2026-01-17', 11498.83, 'active', NULL, '', '2026-01-19 00:00:00.000000', '2026-01-23 13:00:00.000000', 10, 6, 177);
INSERT INTO `employee_employeeprofile` VALUES (174, 'EMP202601MKT003', '2024-01-20', 7834.22, 'active', NULL, '', '2026-01-16 00:00:00.000000', '2026-01-23 14:00:00.000000', 3, 7, 178);
INSERT INTO `employee_employeeprofile` VALUES (175, 'EMP202601PRD006', '2026-01-08', 6143.88, 'active', NULL, '', '2026-01-11 00:00:00.000000', '2026-01-23 13:00:00.000000', 2, 9, 179);
INSERT INTO `employee_employeeprofile` VALUES (176, 'EMP202601ADM007', '2022-11-17', 8120.55, 'active', NULL, '', '2025-12-31 00:00:00.000000', '2026-01-23 15:00:00.000000', 9, 7, 180);
INSERT INTO `employee_employeeprofile` VALUES (177, 'EMP202601CS011', '2025-11-26', 13005.09, 'resigned', '2026-01-01', '个人发展', '2026-01-11 00:00:00.000000', '2026-01-23 22:00:00.000000', 8, 2, 181);
INSERT INTO `employee_employeeprofile` VALUES (178, 'EMP202601HR008', '2024-12-20', 30766.44, 'active', NULL, '', '2025-12-28 00:00:00.000000', '2026-01-23 06:00:00.000000', 4, 4, 182);
INSERT INTO `employee_employeeprofile` VALUES (179, 'EMP202601HR009', '2020-09-29', 10143.47, 'active', NULL, '', '2026-01-11 00:00:00.000000', '2026-01-23 21:00:00.000000', 4, 7, 183);
INSERT INTO `employee_employeeprofile` VALUES (180, 'EMP202601DES002', '2023-09-01', 16561.20, 'active', NULL, '', '2026-01-16 00:00:00.000000', '2026-01-23 00:00:00.000000', 7, 3, 184);
INSERT INTO `employee_employeeprofile` VALUES (181, 'EMP202601CS012', '2022-10-22', 15265.12, 'active', NULL, '', '2026-01-03 00:00:00.000000', '2026-01-24 09:00:00.000000', 8, 3, 185);
INSERT INTO `employee_employeeprofile` VALUES (182, 'EMP202601FIN005', '2026-01-24', 7945.00, 'active', NULL, '', '2026-01-10 00:00:00.000000', '2026-01-23 03:00:00.000000', 5, 1, 186);
INSERT INTO `employee_employeeprofile` VALUES (183, 'EMP202601HR010', '2022-08-17', 14697.52, 'active', NULL, '', '2026-01-02 00:00:00.000000', '2026-01-24 00:00:00.000000', 4, 6, 187);
INSERT INTO `employee_employeeprofile` VALUES (184, 'EMP202601TECH008', '2022-12-02', 8139.67, 'active', NULL, '', '2025-12-27 00:00:00.000000', '2026-01-23 22:00:00.000000', 1, 1, 188);
INSERT INTO `employee_employeeprofile` VALUES (185, 'EMP202601LEG011', '2024-10-06', 12825.96, 'active', NULL, '', '2025-12-28 00:00:00.000000', '2026-01-24 09:00:00.000000', 10, 6, 189);
INSERT INTO `employee_employeeprofile` VALUES (186, 'EMP202601ADM008', '2026-01-14', 18264.92, 'active', NULL, '', '2025-12-30 00:00:00.000000', '2026-01-23 17:00:00.000000', 9, 5, 190);
INSERT INTO `employee_employeeprofile` VALUES (187, 'EMP202601OPS009', '2020-10-02', 15689.49, 'active', NULL, '', '2026-01-05 00:00:00.000000', '2026-01-23 04:00:00.000000', 6, 3, 191);
INSERT INTO `employee_employeeprofile` VALUES (188, 'EMP202601FIN006', '2021-09-07', 11401.08, 'active', NULL, '', '2026-01-17 00:00:00.000000', '2026-01-23 13:00:00.000000', 5, 9, 192);
INSERT INTO `employee_employeeprofile` VALUES (189, 'EMP202601TECH009', '2026-01-05', 9031.47, 'active', NULL, '', '2026-01-10 00:00:00.000000', '2026-01-23 06:00:00.000000', 1, 10, 193);
INSERT INTO `employee_employeeprofile` VALUES (190, 'EMP202601DES003', '2021-01-10', 12789.85, 'active', NULL, '', '2026-01-10 00:00:00.000000', '2026-01-24 19:00:00.000000', 7, 2, 194);
INSERT INTO `employee_employeeprofile` VALUES (191, 'EMP202601ADM009', '2026-01-16', 8267.61, 'active', NULL, '', '2026-01-15 00:00:00.000000', '2026-01-23 05:00:00.000000', 9, 8, 195);
INSERT INTO `employee_employeeprofile` VALUES (192, 'EMP202601HR011', '2022-01-13', 6788.89, 'active', NULL, '', '2026-01-25 00:00:00.000000', '2026-01-24 17:00:00.000000', 4, 1, 196);
INSERT INTO `employee_employeeprofile` VALUES (193, 'EMP202601CS013', '2020-11-02', 7739.35, 'active', NULL, '', '2026-01-03 00:00:00.000000', '2026-01-24 17:00:00.000000', 8, 9, 197);
INSERT INTO `employee_employeeprofile` VALUES (194, 'EMP202601FIN007', '2020-11-10', 18386.80, 'active', NULL, '', '2026-01-17 00:00:00.000000', '2026-01-23 02:00:00.000000', 5, 3, 198);
INSERT INTO `employee_employeeprofile` VALUES (195, 'EMP202601DES004', '2025-10-27', 9976.19, 'resigned', '2026-01-10', '工作地点远', '2025-12-26 00:00:00.000000', '2026-01-24 01:00:00.000000', 7, 9, 199);
INSERT INTO `employee_employeeprofile` VALUES (196, 'EMP202601PRD007', '2024-08-21', 9830.29, 'active', NULL, '', '2026-01-17 00:00:00.000000', '2026-01-24 05:00:00.000000', 2, 1, 200);
INSERT INTO `employee_employeeprofile` VALUES (197, 'EMP202601FIN008', '2026-01-20', 10806.37, 'active', NULL, '', '2025-12-29 00:00:00.000000', '2026-01-23 10:00:00.000000', 5, 6, 201);
INSERT INTO `employee_employeeprofile` VALUES (198, 'EMP202601FIN009', '2022-01-15', 9383.93, 'active', NULL, '', '2026-01-02 00:00:00.000000', '2026-01-23 05:00:00.000000', 5, 8, 202);
INSERT INTO `employee_employeeprofile` VALUES (199, 'EMP202601OPS010', '2024-06-04', 40554.59, 'resigned', '2026-01-25', '薪资不满意', '2026-01-09 00:00:00.000000', '2026-01-23 04:00:00.000000', 6, 4, 203);
INSERT INTO `employee_employeeprofile` VALUES (200, 'EMP202601TECH010', '2025-01-30', 8052.20, 'resigned', '2026-01-02', '公司裁员', '2025-12-29 00:00:00.000000', '2026-01-23 06:00:00.000000', 1, 1, 204);
INSERT INTO `employee_employeeprofile` VALUES (201, 'EMP202601ADM010', '2025-04-30', 11358.96, 'resigned', '2026-01-25', '工作地点远', '2026-01-08 00:00:00.000000', '2026-01-24 06:00:00.000000', 9, 6, 205);
INSERT INTO `employee_employeeprofile` VALUES (202, 'EMP202601MKT004', '2025-09-27', 11208.67, 'resigned', '2026-01-25', '公司裁员', '2025-12-28 00:00:00.000000', '2026-01-24 20:00:00.000000', 3, 10, 206);
INSERT INTO `employee_employeeprofile` VALUES (203, 'EMP202601MKT005', '2024-02-05', 17921.12, 'resigned', '2026-01-18', '薪资不满意', '2025-12-29 00:00:00.000000', '2026-01-24 16:00:00.000000', 3, 5, 207);
INSERT INTO `employee_employeeprofile` VALUES (204, 'EMP202601OPS011', '2025-01-25', 11631.69, 'active', NULL, '', '2026-01-11 00:00:00.000000', '2026-01-24 02:00:00.000000', 6, 9, 208);
INSERT INTO `employee_employeeprofile` VALUES (205, 'EMP202601ADM011', '2026-01-19', 9636.16, 'active', NULL, '', '2026-01-03 00:00:00.000000', '2026-01-24 21:00:00.000000', 9, 8, 209);
INSERT INTO `employee_employeeprofile` VALUES (206, 'EMP202601OPS012', '2020-11-01', 8155.41, 'active', NULL, '', '2026-01-07 00:00:00.000000', '2026-01-24 05:00:00.000000', 6, 10, 210);
INSERT INTO `employee_employeeprofile` VALUES (207, 'EMP202601FIN010', '2022-01-07', 11420.93, 'active', NULL, '', '2026-01-23 00:00:00.000000', '2026-01-24 02:00:00.000000', 5, 8, 211);
INSERT INTO `employee_employeeprofile` VALUES (208, 'EMP202601CS014', '2024-07-04', 11428.99, 'resigned', '2026-01-13', '工作地点远', '2026-01-14 00:00:00.000000', '2026-01-24 15:00:00.000000', 8, 10, 212);
INSERT INTO `employee_employeeprofile` VALUES (209, 'EMP202601LEG012', '2021-12-09', 9801.60, 'active', NULL, '', '2025-12-30 00:00:00.000000', '2026-01-23 03:00:00.000000', 10, 1, 213);
INSERT INTO `employee_employeeprofile` VALUES (210, 'EMP202601FIN011', '2020-08-23', 12933.65, 'active', NULL, '', '2026-01-09 00:00:00.000000', '2026-01-24 05:00:00.000000', 5, 2, 214);
INSERT INTO `employee_employeeprofile` VALUES (211, 'EMP202601MKT006', '2021-11-16', 17988.17, 'active', NULL, '', '2026-01-05 00:00:00.000000', '2026-01-24 17:00:00.000000', 3, 6, 215);
INSERT INTO `employee_employeeprofile` VALUES (212, 'EMP202601FIN012', '2024-01-01', 16332.35, 'active', NULL, '', '2026-01-05 00:00:00.000000', '2026-01-24 17:00:00.000000', 5, 5, 216);
INSERT INTO `employee_employeeprofile` VALUES (213, 'EMP202601FIN013', '2026-01-05', 37173.41, 'active', NULL, '', '2026-01-08 00:00:00.000000', '2026-01-24 20:00:00.000000', 5, 4, 217);
INSERT INTO `employee_employeeprofile` VALUES (214, 'EMP202601FIN014', '2024-10-29', 19788.88, 'active', NULL, '', '2025-12-30 00:00:00.000000', '2026-01-24 18:00:00.000000', 5, 3, 218);
INSERT INTO `employee_employeeprofile` VALUES (215, 'EMP202601OPS013', '2024-06-04', 8864.24, 'resigned', '2026-01-04', '个人发展', '2026-01-12 00:00:00.000000', '2026-01-23 14:00:00.000000', 6, 1, 219);
INSERT INTO `employee_employeeprofile` VALUES (216, 'EMP202601ADM012', '2025-05-30', 7646.36, 'resigned', '2026-01-10', '薪资不满意', '2026-01-14 00:00:00.000000', '2026-01-25 00:00:00.000000', 9, 8, 220);
INSERT INTO `employee_employeeprofile` VALUES (217, 'EMP202601PRD008', '2025-01-12', 12691.23, 'active', NULL, '', '2026-01-13 00:00:00.000000', '2026-01-23 00:00:00.000000', 2, 2, 221);
INSERT INTO `employee_employeeprofile` VALUES (218, 'EMP202601TECH011', '2026-01-09', 7961.79, 'active', NULL, '', '2026-01-25 00:00:00.000000', '2026-01-23 08:00:00.000000', 1, 7, 222);
INSERT INTO `employee_employeeprofile` VALUES (219, 'EMP202601FIN015', '2026-01-06', 14488.83, 'active', NULL, '', '2026-01-11 00:00:00.000000', '2026-01-24 13:00:00.000000', 5, 5, 223);
INSERT INTO `employee_employeeprofile` VALUES (220, 'EMP202601CS015', '2026-01-07', 12227.43, 'active', NULL, '', '2025-12-28 00:00:00.000000', '2026-01-23 13:00:00.000000', 8, 5, 224);
INSERT INTO `employee_employeeprofile` VALUES (221, 'EMP202601DES005', '2026-01-01', 9883.79, 'active', NULL, '', '2026-01-02 00:00:00.000000', '2026-01-23 01:00:00.000000', 7, 10, 225);
INSERT INTO `employee_employeeprofile` VALUES (222, 'EMP202601LEG013', '2026-01-04', 10484.41, 'active', NULL, '', '2025-12-29 00:00:00.000000', '2026-01-23 23:00:00.000000', 10, 7, 226);
INSERT INTO `employee_employeeprofile` VALUES (223, 'EMP202601CS016', '2026-01-06', 6210.96, 'active', NULL, '', '2026-01-10 00:00:00.000000', '2026-01-23 01:00:00.000000', 8, 9, 227);
INSERT INTO `employee_employeeprofile` VALUES (224, 'EMP202601LEG014', '2023-01-26', 9895.87, 'active', NULL, '', '2026-01-19 00:00:00.000000', '2026-01-23 05:00:00.000000', 10, 7, 228);
INSERT INTO `employee_employeeprofile` VALUES (225, 'EMP202601DES006', '2026-01-12', 7345.86, 'active', NULL, '', '2025-12-30 00:00:00.000000', '2026-01-23 19:00:00.000000', 7, 8, 229);
INSERT INTO `employee_employeeprofile` VALUES (226, 'EMP202601OPS014', '2024-09-02', 19180.29, 'resigned', '2026-01-25', '公司裁员', '2025-12-30 00:00:00.000000', '2026-01-23 09:00:00.000000', 6, 3, 230);
INSERT INTO `employee_employeeprofile` VALUES (227, 'EMP202601OPS015', '2025-12-26', 11087.90, 'resigned', '2026-01-25', '其他', '2025-12-31 00:00:00.000000', '2026-01-23 21:00:00.000000', 6, 7, 231);
INSERT INTO `employee_employeeprofile` VALUES (228, 'EMP202601ADM013', '2026-01-07', 7314.29, 'active', NULL, '', '2026-01-16 00:00:00.000000', '2026-01-24 04:00:00.000000', 9, 7, 232);
INSERT INTO `employee_employeeprofile` VALUES (229, 'EMP202601MKT007', '2024-01-14', 6144.18, 'active', NULL, '', '2026-01-04 00:00:00.000000', '2026-01-23 01:00:00.000000', 3, 1, 233);
INSERT INTO `employee_employeeprofile` VALUES (230, 'EMP202601DES007', '2020-09-16', 10277.86, 'active', NULL, '', '2026-01-20 00:00:00.000000', '2026-01-23 18:00:00.000000', 7, 7, 234);
INSERT INTO `employee_employeeprofile` VALUES (231, 'EMP202601LEG015', '2026-01-15', 10687.39, 'active', NULL, '', '2026-01-13 00:00:00.000000', '2026-01-24 12:00:00.000000', 10, 8, 235);
INSERT INTO `employee_employeeprofile` VALUES (232, 'EMP202601TECH012', '2026-01-02', 7734.90, 'active', NULL, '', '2026-01-06 00:00:00.000000', '2026-01-23 18:00:00.000000', 1, 9, 236);
INSERT INTO `employee_employeeprofile` VALUES (233, 'EMP202601HR012', '2025-12-26', 11938.49, 'resigned', '2026-01-25', '其他', '2026-01-21 00:00:00.000000', '2026-01-24 08:00:00.000000', 4, 9, 237);
INSERT INTO `employee_employeeprofile` VALUES (234, 'EMP202601TECH013', '2026-01-03', 13642.49, 'active', NULL, '', '2026-01-25 00:00:00.000000', '2026-01-23 18:00:00.000000', 1, 2, 238);
INSERT INTO `employee_employeeprofile` VALUES (235, 'EMP202601CS017', '2024-09-23', 9856.77, 'active', NULL, '', '2026-01-17 00:00:00.000000', '2026-01-24 19:00:00.000000', 8, 10, 239);
INSERT INTO `employee_employeeprofile` VALUES (236, 'EMP202601CS018', '2021-12-05', 10432.31, 'active', NULL, '', '2026-01-22 00:00:00.000000', '2026-01-24 08:00:00.000000', 8, 6, 240);
INSERT INTO `employee_employeeprofile` VALUES (237, 'EMP202601TECH014', '2022-10-29', 7251.50, 'active', NULL, '', '2026-01-20 00:00:00.000000', '2026-01-23 03:00:00.000000', 1, 1, 241);
INSERT INTO `employee_employeeprofile` VALUES (238, 'EMP202601PRD009', '2023-12-10', 49677.44, 'active', NULL, '', '2026-01-07 00:00:00.000000', '2026-01-23 14:00:00.000000', 2, 4, 242);
INSERT INTO `employee_employeeprofile` VALUES (239, 'EMP202601LEG016', '2026-01-04', 16656.84, 'active', NULL, '', '2026-01-22 00:00:00.000000', '2026-01-24 13:00:00.000000', 10, 3, 243);
INSERT INTO `employee_employeeprofile` VALUES (240, 'EMP202601PRD010', '2024-12-01', 16739.39, 'resigned', '2026-01-17', '个人发展', '2026-01-09 00:00:00.000000', '2026-01-23 16:00:00.000000', 2, 3, 244);
INSERT INTO `employee_employeeprofile` VALUES (241, 'EMP202601PRD011', '2026-01-15', 14522.14, 'active', NULL, '', '2026-01-03 00:00:00.000000', '2026-01-23 08:00:00.000000', 2, 5, 245);
INSERT INTO `employee_employeeprofile` VALUES (242, 'EMP202601FIN016', '2024-09-10', 21396.46, 'active', NULL, '', '2026-01-16 00:00:00.000000', '2026-01-24 13:00:00.000000', 5, 3, 246);
INSERT INTO `employee_employeeprofile` VALUES (243, 'EMP202601TECH015', '2022-10-26', 8444.60, 'active', NULL, '', '2026-01-12 00:00:00.000000', '2026-01-23 19:00:00.000000', 1, 9, 247);
INSERT INTO `employee_employeeprofile` VALUES (244, 'EMP202601LEG017', '2021-12-31', 7293.80, 'active', NULL, '', '2026-01-03 00:00:00.000000', '2026-01-23 22:00:00.000000', 10, 1, 248);
INSERT INTO `employee_employeeprofile` VALUES (245, 'EMP202601CS019', '2024-09-02', 12816.18, 'resigned', '2026-01-11', '工作地点远', '2026-01-14 00:00:00.000000', '2026-01-23 13:00:00.000000', 8, 2, 249);
INSERT INTO `employee_employeeprofile` VALUES (246, 'EMP202601HR013', '2020-08-18', 8464.15, 'active', NULL, '', '2026-01-01 00:00:00.000000', '2026-01-23 00:00:00.000000', 4, 9, 250);
INSERT INTO `employee_employeeprofile` VALUES (247, 'EMP202601LEG018', '2025-05-30', 9934.89, 'resigned', '2026-01-19', '薪资不满意', '2025-12-27 00:00:00.000000', '2026-01-23 01:00:00.000000', 10, 7, 251);
INSERT INTO `employee_employeeprofile` VALUES (248, 'EMP202601HR014', '2023-12-30', 6005.24, 'active', NULL, '', '2026-01-08 00:00:00.000000', '2026-01-24 22:00:00.000000', 4, 9, 252);
INSERT INTO `employee_employeeprofile` VALUES (249, 'EMP202601PRD012', '2024-07-04', 9886.52, 'resigned', '2026-01-24', '公司裁员', '2026-01-17 00:00:00.000000', '2026-01-23 07:00:00.000000', 2, 1, 253);
INSERT INTO `employee_employeeprofile` VALUES (250, 'EMP202601CS020', '2020-08-10', 9255.58, 'active', NULL, '', '2026-01-17 00:00:00.000000', '2026-01-23 12:00:00.000000', 8, 1, 254);
INSERT INTO `employee_employeeprofile` VALUES (251, 'EMP202601CS021', '2021-12-13', 12015.21, 'active', NULL, '', '2026-01-21 00:00:00.000000', '2026-01-23 20:00:00.000000', 8, 6, 255);
INSERT INTO `employee_employeeprofile` VALUES (252, 'EMP202601TECH016', '2021-11-21', 44459.10, 'active', NULL, '', '2026-01-13 00:00:00.000000', '2026-01-24 02:00:00.000000', 1, 4, 256);
INSERT INTO `employee_employeeprofile` VALUES (253, 'EMP202601HR015', '2026-01-10', 31663.78, 'active', NULL, '', '2026-01-05 00:00:00.000000', '2026-01-23 17:00:00.000000', 4, 4, 257);
INSERT INTO `employee_employeeprofile` VALUES (254, 'EMP202601ADM014', '2023-11-10', 14016.61, 'active', NULL, '', '2026-01-02 00:00:00.000000', '2026-01-24 21:00:00.000000', 9, 5, 258);
INSERT INTO `employee_employeeprofile` VALUES (255, 'EMP202601OPS016', '2024-02-05', 11096.70, 'resigned', '2026-01-05', '公司裁员', '2026-01-18 00:00:00.000000', '2026-01-23 05:00:00.000000', 6, 2, 259);
INSERT INTO `employee_employeeprofile` VALUES (256, 'EMP202601HR016', '2023-09-14', 12119.11, 'active', NULL, '', '2025-12-30 00:00:00.000000', '2026-01-24 00:00:00.000000', 4, 2, 260);
INSERT INTO `employee_employeeprofile` VALUES (257, 'EMP202601PRD013', '2026-01-17', 11295.25, 'active', NULL, '', '2026-01-20 00:00:00.000000', '2026-01-24 00:00:00.000000', 2, 2, 261);
INSERT INTO `employee_employeeprofile` VALUES (258, 'EMP202601FIN017', '2022-01-20', 36831.70, 'active', NULL, '', '2026-01-20 00:00:00.000000', '2026-01-24 19:00:00.000000', 5, 4, 262);
INSERT INTO `employee_employeeprofile` VALUES (259, 'EMP202601OPS017', '2020-12-08', 9111.29, 'active', NULL, '', '2026-01-23 00:00:00.000000', '2026-01-23 03:00:00.000000', 6, 8, 263);
INSERT INTO `employee_employeeprofile` VALUES (260, 'EMP202601LEG019', '2026-01-22', 11696.83, 'active', NULL, '', '2026-01-03 00:00:00.000000', '2026-01-23 23:00:00.000000', 10, 8, 264);
INSERT INTO `employee_employeeprofile` VALUES (261, 'EMP202601CS022', '2023-08-24', 8060.07, 'active', NULL, '', '2026-01-03 00:00:00.000000', '2026-01-24 07:00:00.000000', 8, 10, 265);
INSERT INTO `employee_employeeprofile` VALUES (262, 'EMP202601PRD014', '2022-01-11', 10241.45, 'active', NULL, '', '2025-12-28 00:00:00.000000', '2026-01-24 05:00:00.000000', 2, 10, 266);
INSERT INTO `employee_employeeprofile` VALUES (263, 'EMP202601ADM015', '2024-06-04', 47318.51, 'resigned', '2026-01-25', '公司裁员', '2026-01-03 00:00:00.000000', '2026-01-24 18:00:00.000000', 9, 4, 267);
INSERT INTO `employee_employeeprofile` VALUES (264, 'EMP202601MKT008', '2021-11-04', 22413.48, 'active', NULL, '', '2026-01-22 00:00:00.000000', '2026-01-24 09:00:00.000000', 3, 3, 268);
INSERT INTO `employee_employeeprofile` VALUES (265, 'EMP202601MKT009', '2023-09-17', 13050.73, 'active', NULL, '', '2025-12-27 00:00:00.000000', '2026-01-23 19:00:00.000000', 3, 2, 269);
INSERT INTO `employee_employeeprofile` VALUES (266, 'EMP202601CS023', '2025-07-29', 9697.79, 'resigned', '2026-01-13', '薪资不满意', '2025-12-29 00:00:00.000000', '2026-01-23 21:00:00.000000', 8, 10, 270);
INSERT INTO `employee_employeeprofile` VALUES (267, 'EMP202601CS024', '2021-12-17', 10042.75, 'active', NULL, '', '2026-01-19 00:00:00.000000', '2026-01-24 18:00:00.000000', 8, 2, 271);
INSERT INTO `employee_employeeprofile` VALUES (268, 'EMP202601OPS018', '2020-09-20', 17710.44, 'active', NULL, '', '2026-01-01 00:00:00.000000', '2026-01-23 09:00:00.000000', 6, 6, 272);
INSERT INTO `employee_employeeprofile` VALUES (269, 'EMP202601FIN018', '2025-01-22', 8558.31, 'active', NULL, '', '2025-12-26 00:00:00.000000', '2026-01-24 03:00:00.000000', 5, 1, 273);
INSERT INTO `employee_employeeprofile` VALUES (270, 'EMP202601TECH017', '2022-11-19', 18028.26, 'active', NULL, '', '2026-01-15 00:00:00.000000', '2026-01-23 02:00:00.000000', 1, 5, 274);
INSERT INTO `employee_employeeprofile` VALUES (271, 'EMP202601FIN019', '2026-01-25', 10962.81, 'active', NULL, '', '2026-01-07 00:00:00.000000', '2026-01-23 20:00:00.000000', 5, 9, 275);
INSERT INTO `employee_employeeprofile` VALUES (272, 'EMP202601FIN020', '2025-10-27', 11566.86, 'resigned', '2026-01-25', '其他', '2026-01-08 00:00:00.000000', '2026-01-24 06:00:00.000000', 5, 7, 276);
INSERT INTO `employee_employeeprofile` VALUES (273, 'EMP202601TECH018', '2023-10-29', 10029.99, 'active', NULL, '', '2026-01-18 00:00:00.000000', '2026-01-24 20:00:00.000000', 1, 8, 277);
INSERT INTO `employee_employeeprofile` VALUES (274, 'EMP202601OPS019', '2021-12-07', 7794.69, 'active', NULL, '', '2026-01-19 00:00:00.000000', '2026-01-24 02:00:00.000000', 6, 9, 278);
INSERT INTO `employee_employeeprofile` VALUES (275, 'EMP202601TECH019', '2023-08-02', 8274.21, 'active', NULL, '', '2026-01-03 00:00:00.000000', '2026-01-24 04:00:00.000000', 1, 7, 279);
INSERT INTO `employee_employeeprofile` VALUES (276, 'EMP202601DES008', '2026-01-25', 7623.65, 'active', NULL, '', '2026-01-23 00:00:00.000000', '2026-01-24 16:00:00.000000', 7, 1, 280);
INSERT INTO `employee_employeeprofile` VALUES (277, 'EMP202601FIN021', '2021-11-21', 7454.84, 'active', NULL, '', '2026-01-15 00:00:00.000000', '2026-01-24 22:00:00.000000', 5, 8, 281);
INSERT INTO `employee_employeeprofile` VALUES (278, 'EMP202601DES009', '2022-01-01', 13368.41, 'active', NULL, '', '2026-01-01 00:00:00.000000', '2026-01-23 04:00:00.000000', 7, 2, 282);
INSERT INTO `employee_employeeprofile` VALUES (279, 'EMP202601TECH020', '2025-12-26', 12307.39, 'resigned', '2026-01-02', '公司裁员', '2026-01-20 00:00:00.000000', '2026-01-23 23:00:00.000000', 1, 5, 283);
INSERT INTO `employee_employeeprofile` VALUES (280, 'EMP202601FIN022', '2024-04-05', 11272.17, 'resigned', '2026-01-05', '工作地点远', '2026-01-24 00:00:00.000000', '2026-01-23 11:00:00.000000', 5, 6, 284);
INSERT INTO `employee_employeeprofile` VALUES (281, 'EMP202601FIN023', '2024-02-05', 8257.69, 'resigned', '2026-01-25', '工作地点远', '2026-01-10 00:00:00.000000', '2026-01-23 03:00:00.000000', 5, 1, 285);
INSERT INTO `employee_employeeprofile` VALUES (282, 'EMP202601PRD015', '2024-12-01', 11822.00, 'resigned', '2026-01-25', '薪资不满意', '2026-01-07 00:00:00.000000', '2026-01-24 20:00:00.000000', 2, 6, 286);
INSERT INTO `employee_employeeprofile` VALUES (283, 'EMP202601HR017', '2021-12-11', 13650.51, 'active', NULL, '', '2026-01-03 00:00:00.000000', '2026-01-23 13:00:00.000000', 4, 2, 287);
INSERT INTO `employee_employeeprofile` VALUES (284, 'EMP202601OPS020', '2025-01-06', 30195.28, 'active', NULL, '', '2026-01-17 00:00:00.000000', '2026-01-23 09:00:00.000000', 6, 4, 288);
INSERT INTO `employee_employeeprofile` VALUES (285, 'EMP202601ADM016', '2023-01-17', 9052.05, 'active', NULL, '', '2026-01-11 00:00:00.000000', '2026-01-24 13:00:00.000000', 9, 1, 289);
INSERT INTO `employee_employeeprofile` VALUES (286, 'EMP202601PRD016', '2022-09-23', 6561.69, 'active', NULL, '', '2026-01-12 00:00:00.000000', '2026-01-23 20:00:00.000000', 2, 7, 290);
INSERT INTO `employee_employeeprofile` VALUES (287, 'EMP202601LEG020', '2021-11-11', 10621.65, 'active', NULL, '', '2026-01-04 00:00:00.000000', '2026-01-24 19:00:00.000000', 10, 10, 291);
INSERT INTO `employee_employeeprofile` VALUES (288, 'EMP202601FIN024', '2022-08-22', 18947.80, 'active', NULL, '', '2026-01-11 00:00:00.000000', '2026-01-23 18:00:00.000000', 5, 5, 292);
INSERT INTO `employee_employeeprofile` VALUES (289, 'EMP202601OPS021', '2023-10-19', 19006.61, 'active', NULL, '', '2026-01-08 00:00:00.000000', '2026-01-23 17:00:00.000000', 6, 3, 293);
INSERT INTO `employee_employeeprofile` VALUES (290, 'EMP202601HR018', '2025-11-26', 8948.22, 'resigned', '2026-01-25', '工作地点远', '2026-01-12 00:00:00.000000', '2026-01-25 00:00:00.000000', 4, 9, 294);
INSERT INTO `employee_employeeprofile` VALUES (291, 'EMP202601PRD017', '2024-12-05', 16447.99, 'active', NULL, '', '2026-01-06 00:00:00.000000', '2026-01-24 10:00:00.000000', 2, 6, 295);
INSERT INTO `employee_employeeprofile` VALUES (292, 'EMP202601TECH021', '2026-01-19', 8060.52, 'active', NULL, '', '2026-01-06 00:00:00.000000', '2026-01-23 12:00:00.000000', 1, 9, 296);
INSERT INTO `employee_employeeprofile` VALUES (293, 'EMP202601DES010', '2024-11-24', 6296.16, 'active', NULL, '', '2025-12-30 00:00:00.000000', '2026-01-23 05:00:00.000000', 7, 1, 297);
INSERT INTO `employee_employeeprofile` VALUES (294, 'EMP202601OPS022', '2023-09-29', 13650.13, 'active', NULL, '', '2025-12-29 00:00:00.000000', '2026-01-23 18:00:00.000000', 6, 5, 298);
INSERT INTO `employee_employeeprofile` VALUES (295, 'EMP202601LEG021', '2026-01-10', 15167.66, 'active', NULL, '', '2026-01-17 00:00:00.000000', '2026-01-23 23:00:00.000000', 10, 5, 299);
INSERT INTO `employee_employeeprofile` VALUES (296, 'EMP202601HR019', '2021-01-15', 8689.59, 'active', NULL, '', '2026-01-01 00:00:00.000000', '2026-01-24 08:00:00.000000', 4, 7, 300);
INSERT INTO `employee_employeeprofile` VALUES (297, 'EMP202601TECH022', '2024-12-01', 10567.68, 'resigned', '2026-01-07', '薪资不满意', '2026-01-04 00:00:00.000000', '2026-01-23 02:00:00.000000', 1, 2, 301);
INSERT INTO `employee_employeeprofile` VALUES (298, 'EMP202601ADM017', '2024-10-15', 37874.69, 'active', NULL, '', '2026-01-07 00:00:00.000000', '2026-01-23 15:00:00.000000', 9, 4, 302);
INSERT INTO `employee_employeeprofile` VALUES (299, 'EMP202601DES011', '2020-12-03', 7267.01, 'active', NULL, '', '2025-12-28 00:00:00.000000', '2026-01-24 03:00:00.000000', 7, 9, 303);
INSERT INTO `employee_employeeprofile` VALUES (300, 'EMP202601MKT010', '2020-12-16', 9740.43, 'active', NULL, '', '2025-12-28 00:00:00.000000', '2026-01-24 03:00:00.000000', 3, 8, 304);
INSERT INTO `employee_employeeprofile` VALUES (301, 'EMP202601OPS023', '2025-10-27', 8700.69, 'resigned', '2026-01-10', '公司裁员', '2026-01-19 00:00:00.000000', '2026-01-23 05:00:00.000000', 6, 9, 305);
INSERT INTO `employee_employeeprofile` VALUES (302, 'EMP202601CS025', '2021-12-11', 8935.56, 'active', NULL, '', '2025-12-26 00:00:00.000000', '2026-01-23 01:00:00.000000', 8, 10, 306);
INSERT INTO `employee_employeeprofile` VALUES (303, 'EMP202601OPS024', '2024-08-09', 11036.16, 'active', NULL, '', '2025-12-30 00:00:00.000000', '2026-01-24 07:00:00.000000', 6, 2, 307);
INSERT INTO `employee_employeeprofile` VALUES (304, 'EMP202601LEG022', '2022-01-20', 19702.94, 'active', NULL, '', '2025-12-28 00:00:00.000000', '2026-01-23 18:00:00.000000', 10, 5, 308);
INSERT INTO `employee_employeeprofile` VALUES (305, 'EMP202601ADM018', '2025-08-28', 12340.43, 'resigned', '2026-01-24', '工作地点远', '2026-01-01 00:00:00.000000', '2026-01-23 19:00:00.000000', 9, 8, 309);
INSERT INTO `employee_employeeprofile` VALUES (306, 'EMP202601HR020', '2020-11-11', 22875.94, 'active', NULL, '', '2026-01-11 00:00:00.000000', '2026-01-24 20:00:00.000000', 4, 3, 310);
INSERT INTO `employee_employeeprofile` VALUES (307, 'EMP202601HR021', '2026-01-18', 10012.57, 'active', NULL, '', '2026-01-12 00:00:00.000000', '2026-01-24 09:00:00.000000', 4, 9, 311);
INSERT INTO `employee_employeeprofile` VALUES (308, 'EMP202601HR022', '2024-09-03', 13077.95, 'active', NULL, '', '2025-12-31 00:00:00.000000', '2026-01-23 01:00:00.000000', 4, 2, 312);
INSERT INTO `employee_employeeprofile` VALUES (309, 'EMP202601HR023', '2021-11-10', 18634.10, 'active', NULL, '', '2026-01-04 00:00:00.000000', '2026-01-24 04:00:00.000000', 4, 5, 313);
INSERT INTO `employee_employeeprofile` VALUES (310, 'EMP202601TECH023', '2024-09-16', 19749.28, 'active', NULL, '', '2026-01-07 00:00:00.000000', '2026-01-23 21:00:00.000000', 1, 5, 314);
INSERT INTO `employee_employeeprofile` VALUES (311, 'EMP202601FIN025', '2026-01-09', 15534.29, 'active', NULL, '', '2026-01-12 00:00:00.000000', '2026-01-24 04:00:00.000000', 5, 3, 315);
INSERT INTO `employee_employeeprofile` VALUES (312, 'EMP202601CS026', '2023-10-27', 12188.99, 'active', NULL, '', '2026-01-08 00:00:00.000000', '2026-01-23 06:00:00.000000', 8, 2, 316);
INSERT INTO `employee_employeeprofile` VALUES (313, 'EMP202601HR024', '2026-01-12', 7806.88, 'active', NULL, '', '2025-12-30 00:00:00.000000', '2026-01-24 03:00:00.000000', 4, 10, 317);
INSERT INTO `employee_employeeprofile` VALUES (314, 'EMP202601HR025', '2022-10-18', 19959.64, 'active', NULL, '', '2025-12-29 00:00:00.000000', '2026-01-23 04:00:00.000000', 4, 3, 318);
INSERT INTO `employee_employeeprofile` VALUES (315, 'EMP202601MKT011', '2025-01-14', 12214.03, 'active', NULL, '', '2026-01-12 00:00:00.000000', '2026-01-23 07:00:00.000000', 3, 6, 319);
INSERT INTO `employee_employeeprofile` VALUES (316, 'EMP202601CS027', '2021-10-19', 13348.58, 'active', NULL, '', '2026-01-25 00:00:00.000000', '2026-01-24 11:00:00.000000', 8, 2, 320);
INSERT INTO `employee_employeeprofile` VALUES (317, 'EMP202601TECH024', '2026-01-12', 11493.79, 'active', NULL, '', '2025-12-30 00:00:00.000000', '2026-01-24 17:00:00.000000', 1, 9, 321);
INSERT INTO `employee_employeeprofile` VALUES (318, 'EMP202601OPS025', '2024-12-01', 7116.79, 'resigned', '2026-01-02', '工作地点远', '2026-01-19 00:00:00.000000', '2026-01-24 00:00:00.000000', 6, 8, 322);
INSERT INTO `employee_employeeprofile` VALUES (319, 'EMP202601MKT012', '2025-05-30', 24855.06, 'resigned', '2026-01-25', '其他', '2026-01-06 00:00:00.000000', '2026-01-23 13:00:00.000000', 3, 3, 323);
INSERT INTO `employee_employeeprofile` VALUES (320, 'EMP202601DES012', '2022-09-03', 9634.42, 'active', NULL, '', '2026-01-17 00:00:00.000000', '2026-01-23 09:00:00.000000', 7, 9, 324);
INSERT INTO `employee_employeeprofile` VALUES (321, 'EMP202601CS028', '2026-01-18', 6440.22, 'active', NULL, '', '2026-01-11 00:00:00.000000', '2026-01-24 05:00:00.000000', 8, 10, 325);
INSERT INTO `employee_employeeprofile` VALUES (322, 'EMP202601OPS026', '2022-08-13', 7940.50, 'active', NULL, '', '2026-01-02 00:00:00.000000', '2026-01-24 14:00:00.000000', 6, 7, 326);
INSERT INTO `employee_employeeprofile` VALUES (323, 'EMP202601ADM019', '2024-10-02', 22509.22, 'resigned', '2026-01-13', '家庭原因', '2026-01-10 00:00:00.000000', '2026-01-23 12:00:00.000000', 9, 3, 327);
INSERT INTO `employee_employeeprofile` VALUES (324, 'EMP202601TECH025', '2024-12-18', 8822.15, 'active', NULL, '', '2025-12-28 00:00:00.000000', '2026-01-24 04:00:00.000000', 1, 7, 328);
INSERT INTO `employee_employeeprofile` VALUES (325, 'EMP202601CS029', '2022-09-23', 34292.64, 'active', NULL, '', '2026-01-25 00:00:00.000000', '2026-01-23 11:00:00.000000', 8, 4, 329);
INSERT INTO `employee_employeeprofile` VALUES (326, 'EMP202601HR026', '2025-01-12', 7108.80, 'active', NULL, '', '2026-01-20 00:00:00.000000', '2026-01-24 22:00:00.000000', 4, 7, 330);
INSERT INTO `employee_employeeprofile` VALUES (327, 'EMP202601CS030', '2021-01-04', 11495.74, 'active', NULL, '', '2026-01-20 00:00:00.000000', '2026-01-23 22:00:00.000000', 8, 10, 331);
INSERT INTO `employee_employeeprofile` VALUES (328, 'EMP202601CS031', '2024-08-02', 42893.24, 'active', NULL, '', '2026-01-19 00:00:00.000000', '2026-01-24 21:00:00.000000', 8, 4, 332);
INSERT INTO `employee_employeeprofile` VALUES (329, 'EMP202601FIN026', '2024-12-15', 12651.26, 'active', NULL, '', '2026-01-02 00:00:00.000000', '2026-01-24 02:00:00.000000', 5, 2, 333);
INSERT INTO `employee_employeeprofile` VALUES (330, 'EMP202601LEG023', '2020-12-26', 45516.25, 'active', NULL, '', '2025-12-27 00:00:00.000000', '2026-01-23 21:00:00.000000', 10, 4, 334);
INSERT INTO `employee_employeeprofile` VALUES (331, 'EMP202601FIN027', '2026-01-15', 19661.60, 'active', NULL, '', '2026-01-03 00:00:00.000000', '2026-01-24 10:00:00.000000', 5, 3, 335);
INSERT INTO `employee_employeeprofile` VALUES (332, 'EMP202601OPS027', '2023-12-03', 11433.67, 'active', NULL, '', '2026-01-14 00:00:00.000000', '2026-01-23 18:00:00.000000', 6, 10, 336);
INSERT INTO `employee_employeeprofile` VALUES (333, 'EMP202601LEG024', '2024-12-01', 15199.60, 'resigned', '2026-01-25', '薪资不满意', '2026-01-07 00:00:00.000000', '2026-01-23 22:00:00.000000', 10, 6, 337);
INSERT INTO `employee_employeeprofile` VALUES (334, 'EMP202601PRD018', '2026-01-16', 8221.18, 'active', NULL, '', '2025-12-30 00:00:00.000000', '2026-01-23 19:00:00.000000', 2, 9, 338);
INSERT INTO `employee_employeeprofile` VALUES (335, 'EMP202601CS032', '2020-10-12', 12796.74, 'active', NULL, '', '2025-12-31 00:00:00.000000', '2026-01-24 03:00:00.000000', 8, 8, 339);
INSERT INTO `employee_employeeprofile` VALUES (336, 'EMP202601FIN028', '2023-10-31', 9700.57, 'active', NULL, '', '2025-12-28 00:00:00.000000', '2026-01-24 10:00:00.000000', 5, 1, 340);
INSERT INTO `employee_employeeprofile` VALUES (337, 'EMP202601PRD019', '2022-09-11', 9162.07, 'active', NULL, '', '2026-01-07 00:00:00.000000', '2026-01-24 19:00:00.000000', 2, 9, 341);
INSERT INTO `employee_employeeprofile` VALUES (338, 'EMP202601CS033', '2024-08-16', 10681.28, 'active', NULL, '', '2026-01-04 00:00:00.000000', '2026-01-24 20:00:00.000000', 8, 6, 342);
INSERT INTO `employee_employeeprofile` VALUES (339, 'EMP202601MKT013', '2020-11-19', 17818.97, 'active', NULL, '', '2025-12-29 00:00:00.000000', '2026-01-24 18:00:00.000000', 3, 3, 343);
INSERT INTO `employee_employeeprofile` VALUES (340, 'EMP202601LEG025', '2026-01-20', 9597.43, 'active', NULL, '', '2026-01-05 00:00:00.000000', '2026-01-23 09:00:00.000000', 10, 8, 344);
INSERT INTO `employee_employeeprofile` VALUES (341, 'EMP202601LEG026', '2024-02-05', 10369.76, 'resigned', '2026-01-22', '薪资不满意', '2026-01-17 00:00:00.000000', '2026-01-23 03:00:00.000000', 10, 10, 345);
INSERT INTO `employee_employeeprofile` VALUES (342, 'EMP202601FIN029', '2025-06-29', 21091.74, 'resigned', '2026-01-19', '个人发展', '2026-01-04 00:00:00.000000', '2026-01-24 16:00:00.000000', 5, 3, 346);
INSERT INTO `employee_employeeprofile` VALUES (343, 'EMP202601OPS028', '2024-08-08', 7038.20, 'active', NULL, '', '2025-12-27 00:00:00.000000', '2026-01-23 23:00:00.000000', 6, 1, 347);
INSERT INTO `employee_employeeprofile` VALUES (344, 'EMP202601CS034', '2023-12-26', 9292.56, 'active', NULL, '', '2025-12-30 00:00:00.000000', '2026-01-24 00:00:00.000000', 8, 1, 348);
INSERT INTO `employee_employeeprofile` VALUES (345, 'EMP202601ADM020', '2026-01-13', 9231.69, 'active', NULL, '', '2026-01-01 00:00:00.000000', '2026-01-24 12:00:00.000000', 9, 7, 349);
INSERT INTO `employee_employeeprofile` VALUES (346, 'EMP202601HR027', '2020-08-06', 11868.22, 'active', NULL, '', '2026-01-07 00:00:00.000000', '2026-01-23 07:00:00.000000', 4, 2, 350);
INSERT INTO `employee_employeeprofile` VALUES (347, 'EMP202601HR028', '2020-11-03', 8219.17, 'active', NULL, '', '2026-01-09 00:00:00.000000', '2026-01-23 23:00:00.000000', 4, 7, 351);
INSERT INTO `employee_employeeprofile` VALUES (348, 'EMP202601FIN030', '2024-12-01', 7488.94, 'resigned', '2026-01-21', '公司裁员', '2026-01-21 00:00:00.000000', '2026-01-24 16:00:00.000000', 5, 1, 352);
INSERT INTO `employee_employeeprofile` VALUES (349, 'EMP202601DES013', '2021-11-03', 8853.57, 'active', NULL, '', '2025-12-28 00:00:00.000000', '2026-01-23 15:00:00.000000', 7, 10, 353);
INSERT INTO `employee_employeeprofile` VALUES (350, 'EMP202601HR029', '2025-01-22', 13751.59, 'active', NULL, '', '2026-01-09 00:00:00.000000', '2026-01-23 06:00:00.000000', 4, 2, 354);
INSERT INTO `employee_employeeprofile` VALUES (351, 'EMP202601FIN031', '2020-11-10', 10075.81, 'active', NULL, '', '2026-01-24 00:00:00.000000', '2026-01-24 16:00:00.000000', 5, 2, 355);
INSERT INTO `employee_employeeprofile` VALUES (352, 'EMP202601PRD020', '2026-01-24', 6748.25, 'active', NULL, '', '2026-01-19 00:00:00.000000', '2026-01-24 08:00:00.000000', 2, 10, 356);
INSERT INTO `employee_employeeprofile` VALUES (353, 'EMP202601PRD021', '2026-01-19', 11644.02, 'active', NULL, '', '2025-12-28 00:00:00.000000', '2026-01-23 03:00:00.000000', 2, 7, 357);
INSERT INTO `employee_employeeprofile` VALUES (354, 'EMP202601LEG027', '2023-12-14', 7227.77, 'active', NULL, '', '2026-01-01 00:00:00.000000', '2026-01-24 23:00:00.000000', 10, 10, 358);
INSERT INTO `employee_employeeprofile` VALUES (355, 'EMP202601ADM021', '2026-01-19', 6620.21, 'active', NULL, '', '2026-01-15 00:00:00.000000', '2026-01-23 15:00:00.000000', 9, 1, 359);
INSERT INTO `employee_employeeprofile` VALUES (356, 'EMP202601CS035', '2023-01-11', 8660.24, 'active', NULL, '', '2026-01-13 00:00:00.000000', '2026-01-24 14:00:00.000000', 8, 9, 360);
INSERT INTO `employee_employeeprofile` VALUES (357, 'EMP202601CS036', '2023-12-30', 11252.11, 'active', NULL, '', '2026-01-13 00:00:00.000000', '2026-01-24 10:00:00.000000', 8, 9, 361);
INSERT INTO `employee_employeeprofile` VALUES (358, 'EMP202601MKT014', '2023-12-14', 10232.61, 'active', NULL, '', '2025-12-29 00:00:00.000000', '2026-01-24 03:00:00.000000', 3, 6, 362);
INSERT INTO `employee_employeeprofile` VALUES (359, 'EMP202601CS037', '2026-01-20', 44519.66, 'active', NULL, '', '2026-01-24 00:00:00.000000', '2026-01-23 01:00:00.000000', 8, 4, 363);
INSERT INTO `employee_employeeprofile` VALUES (360, 'EMP202601CS038', '2025-10-27', 7482.41, 'resigned', '2026-01-08', '薪资不满意', '2026-01-06 00:00:00.000000', '2026-01-24 14:00:00.000000', 8, 7, 364);
INSERT INTO `employee_employeeprofile` VALUES (361, 'EMP202601ADM022', '2024-12-28', 17533.41, 'active', NULL, '', '2026-01-21 00:00:00.000000', '2026-01-23 13:00:00.000000', 9, 5, 365);
INSERT INTO `employee_employeeprofile` VALUES (362, 'EMP202601LEG028', '2021-01-06', 6623.90, 'active', NULL, '', '2025-12-26 00:00:00.000000', '2026-01-24 22:00:00.000000', 10, 1, 366);
INSERT INTO `employee_employeeprofile` VALUES (363, 'EMP202601OPS029', '2022-11-19', 14537.32, 'active', NULL, '', '2026-01-21 00:00:00.000000', '2026-01-24 22:00:00.000000', 6, 2, 367);
INSERT INTO `employee_employeeprofile` VALUES (364, 'EMP202601HR030', '2022-01-08', 7775.46, 'active', NULL, '', '2026-01-09 00:00:00.000000', '2026-01-24 07:00:00.000000', 4, 1, 368);
INSERT INTO `employee_employeeprofile` VALUES (365, 'EMP202601PRD022', '2024-01-18', 18450.04, 'active', NULL, '', '2026-01-14 00:00:00.000000', '2026-01-23 03:00:00.000000', 2, 3, 369);
INSERT INTO `employee_employeeprofile` VALUES (366, 'EMP202601PRD023', '2023-01-10', 11238.50, 'active', NULL, '', '2026-01-14 00:00:00.000000', '2026-01-24 12:00:00.000000', 2, 10, 370);
INSERT INTO `employee_employeeprofile` VALUES (367, 'EMP202601FIN032', '2021-09-01', 7249.39, 'active', NULL, '', '2025-12-30 00:00:00.000000', '2026-01-24 12:00:00.000000', 5, 1, 371);
INSERT INTO `employee_employeeprofile` VALUES (368, 'EMP202601FIN033', '2025-10-27', 47743.50, 'resigned', '2026-01-15', '薪资不满意', '2026-01-02 00:00:00.000000', '2026-01-23 19:00:00.000000', 5, 4, 372);
INSERT INTO `employee_employeeprofile` VALUES (369, 'EMP202601OPS030', '2026-01-20', 7039.41, 'active', NULL, '', '2026-01-09 00:00:00.000000', '2026-01-24 04:00:00.000000', 6, 10, 373);
INSERT INTO `employee_employeeprofile` VALUES (370, 'EMP202601HR031', '2021-08-22', 16539.02, 'active', NULL, '', '2025-12-27 00:00:00.000000', '2026-01-25 00:00:00.000000', 4, 5, 374);
INSERT INTO `employee_employeeprofile` VALUES (371, 'EMP202601PRD024', '2026-01-24', 6123.21, 'active', NULL, '', '2026-01-10 00:00:00.000000', '2026-01-24 05:00:00.000000', 2, 9, 375);
INSERT INTO `employee_employeeprofile` VALUES (372, 'EMP202601CS039', '2026-01-17', 13594.85, 'active', NULL, '', '2026-01-14 00:00:00.000000', '2026-01-23 09:00:00.000000', 8, 2, 376);
INSERT INTO `employee_employeeprofile` VALUES (373, 'EMP202601MKT015', '2020-08-01', 10260.02, 'active', NULL, '', '2026-01-11 00:00:00.000000', '2026-01-24 04:00:00.000000', 3, 8, 377);
INSERT INTO `employee_employeeprofile` VALUES (374, 'EMP202601ADM023', '2026-01-12', 16557.61, 'active', NULL, '', '2026-01-03 00:00:00.000000', '2026-01-23 02:00:00.000000', 9, 5, 378);
INSERT INTO `employee_employeeprofile` VALUES (375, 'EMP202601HR032', '2024-12-01', 7363.20, 'resigned', '2026-01-25', '家庭原因', '2026-01-15 00:00:00.000000', '2026-01-24 16:00:00.000000', 4, 1, 379);
INSERT INTO `employee_employeeprofile` VALUES (376, 'EMP202601FIN034', '2026-01-01', 20086.27, 'active', NULL, '', '2026-01-06 00:00:00.000000', '2026-01-23 09:00:00.000000', 5, 3, 380);
INSERT INTO `employee_employeeprofile` VALUES (377, 'EMP202601LEG029', '2023-10-18', 9564.38, 'active', NULL, '', '2026-01-08 00:00:00.000000', '2026-01-24 20:00:00.000000', 10, 7, 381);
INSERT INTO `employee_employeeprofile` VALUES (378, 'EMP202601FIN035', '2026-01-23', 9173.74, 'active', NULL, '', '2026-01-21 00:00:00.000000', '2026-01-23 08:00:00.000000', 5, 7, 382);
INSERT INTO `employee_employeeprofile` VALUES (379, 'EMP202601TECH026', '2022-01-11', 17176.97, 'active', NULL, '', '2026-01-03 00:00:00.000000', '2026-01-23 16:00:00.000000', 1, 5, 383);
INSERT INTO `employee_employeeprofile` VALUES (380, 'EMP202601CS040', '2026-01-07', 43130.14, 'active', NULL, '', '2026-01-22 00:00:00.000000', '2026-01-24 17:00:00.000000', 8, 4, 384);
INSERT INTO `employee_employeeprofile` VALUES (381, 'EMP202601ADM024', '2024-09-13', 36767.50, 'active', NULL, '', '2026-01-05 00:00:00.000000', '2026-01-24 15:00:00.000000', 9, 4, 385);
INSERT INTO `employee_employeeprofile` VALUES (382, 'EMP202601TECH027', '2022-08-18', 7357.54, 'active', NULL, '', '2026-01-11 00:00:00.000000', '2026-01-25 00:00:00.000000', 1, 9, 386);
INSERT INTO `employee_employeeprofile` VALUES (383, 'EMP202601LEG030', '2026-01-16', 10301.53, 'active', NULL, '', '2025-12-30 00:00:00.000000', '2026-01-24 13:00:00.000000', 10, 10, 387);
INSERT INTO `employee_employeeprofile` VALUES (384, 'EMP202601OPS031', '2020-10-29', 7863.88, 'active', NULL, '', '2026-01-17 00:00:00.000000', '2026-01-23 03:00:00.000000', 6, 9, 388);
INSERT INTO `employee_employeeprofile` VALUES (385, 'EMP202601HR033', '2024-05-05', 14159.11, 'resigned', '2026-01-25', '家庭原因', '2026-01-24 00:00:00.000000', '2026-01-24 20:00:00.000000', 4, 6, 389);
INSERT INTO `employee_employeeprofile` VALUES (386, 'EMP202601OPS032', '2024-05-05', 8591.10, 'resigned', '2026-01-13', '公司裁员', '2026-01-16 00:00:00.000000', '2026-01-23 21:00:00.000000', 6, 1, 390);
INSERT INTO `employee_employeeprofile` VALUES (387, 'EMP202601ADM025', '2025-09-27', 32846.96, 'resigned', '2026-01-25', '家庭原因', '2026-01-10 00:00:00.000000', '2026-01-25 00:00:00.000000', 9, 4, 391);
INSERT INTO `employee_employeeprofile` VALUES (388, 'EMP202601HR034', '2021-11-03', 16838.44, 'active', NULL, '', '2026-01-22 00:00:00.000000', '2026-01-24 09:00:00.000000', 4, 6, 392);
INSERT INTO `employee_employeeprofile` VALUES (389, 'EMP202601HR035', '2020-11-14', 6329.49, 'active', NULL, '', '2026-01-06 00:00:00.000000', '2026-01-24 14:00:00.000000', 4, 10, 393);
INSERT INTO `employee_employeeprofile` VALUES (390, 'EMP202601FIN036', '2024-08-03', 37211.55, 'resigned', '2026-01-25', '其他', '2026-01-23 00:00:00.000000', '2026-01-24 12:00:00.000000', 5, 4, 394);
INSERT INTO `employee_employeeprofile` VALUES (391, 'EMP202601CS041', '2024-01-03', 7026.72, 'active', NULL, '', '2026-01-01 00:00:00.000000', '2026-01-23 05:00:00.000000', 8, 7, 395);
INSERT INTO `employee_employeeprofile` VALUES (392, 'EMP202601PRD025', '2023-10-27', 33065.81, 'active', NULL, '', '2025-12-31 00:00:00.000000', '2026-01-24 14:00:00.000000', 2, 4, 396);
INSERT INTO `employee_employeeprofile` VALUES (393, 'EMP202601HR036', '2023-01-11', 11772.75, 'active', NULL, '', '2026-01-02 00:00:00.000000', '2026-01-23 16:00:00.000000', 4, 2, 397);
INSERT INTO `employee_employeeprofile` VALUES (394, 'EMP202601TECH028', '2023-01-25', 17877.73, 'active', NULL, '', '2026-01-07 00:00:00.000000', '2026-01-23 06:00:00.000000', 1, 3, 398);
INSERT INTO `employee_employeeprofile` VALUES (395, 'EMP202601OPS033', '2026-01-11', 17515.04, 'active', NULL, '', '2026-01-10 00:00:00.000000', '2026-01-23 17:00:00.000000', 6, 5, 399);
INSERT INTO `employee_employeeprofile` VALUES (396, 'EMP202601DES014', '2020-09-12', 43883.20, 'active', NULL, '', '2025-12-30 00:00:00.000000', '2026-01-24 23:00:00.000000', 7, 4, 400);
INSERT INTO `employee_employeeprofile` VALUES (397, 'EMP202601CS042', '2026-01-19', 8029.90, 'active', NULL, '', '2026-01-02 00:00:00.000000', '2026-01-23 17:00:00.000000', 8, 7, 401);
INSERT INTO `employee_employeeprofile` VALUES (398, 'EMP202601CS043', '2021-09-26', 7620.97, 'active', NULL, '', '2025-12-31 00:00:00.000000', '2026-01-24 17:00:00.000000', 8, 10, 402);
INSERT INTO `employee_employeeprofile` VALUES (399, 'EMP202601FIN037', '2024-12-01', 36445.76, 'resigned', '2026-01-06', '工作地点远', '2026-01-16 00:00:00.000000', '2026-01-23 17:00:00.000000', 5, 4, 403);
INSERT INTO `employee_employeeprofile` VALUES (400, 'EMP202601FIN038', '2026-01-04', 9259.12, 'active', NULL, '', '2026-01-25 00:00:00.000000', '2026-01-23 18:00:00.000000', 5, 8, 404);
INSERT INTO `employee_employeeprofile` VALUES (401, 'EMP202601PRD026', '2024-09-26', 11660.24, 'active', NULL, '', '2026-01-04 00:00:00.000000', '2026-01-24 14:00:00.000000', 2, 10, 405);
INSERT INTO `employee_employeeprofile` VALUES (402, 'EMP202601FIN039', '2026-01-03', 11552.59, 'active', NULL, '', '2025-12-29 00:00:00.000000', '2026-01-24 09:00:00.000000', 5, 10, 406);
INSERT INTO `employee_employeeprofile` VALUES (403, 'EMP202601CS044', '2026-01-18', 14959.01, 'active', NULL, '', '2026-01-12 00:00:00.000000', '2026-01-24 11:00:00.000000', 8, 5, 407);
INSERT INTO `employee_employeeprofile` VALUES (404, 'EMP202601DES015', '2024-09-18', 8435.40, 'active', NULL, '', '2026-01-25 00:00:00.000000', '2026-01-23 13:00:00.000000', 7, 10, 408);
INSERT INTO `employee_employeeprofile` VALUES (405, 'EMP202601FIN040', '2024-12-01', 48041.75, 'resigned', '2026-01-08', '个人发展', '2026-01-18 00:00:00.000000', '2026-01-23 11:00:00.000000', 5, 4, 409);
INSERT INTO `employee_employeeprofile` VALUES (406, 'EMP202601MKT016', '2026-01-18', 11208.41, 'active', NULL, '', '2026-01-24 00:00:00.000000', '2026-01-23 13:00:00.000000', 3, 8, 410);
INSERT INTO `employee_employeeprofile` VALUES (407, 'EMP202601OPS034', '2026-01-07', 11857.74, 'active', NULL, '', '2026-01-18 00:00:00.000000', '2026-01-24 20:00:00.000000', 6, 6, 411);
INSERT INTO `employee_employeeprofile` VALUES (408, 'EMP202601HR037', '2021-08-31', 11134.03, 'active', NULL, '', '2026-01-14 00:00:00.000000', '2026-01-24 22:00:00.000000', 4, 9, 412);
INSERT INTO `employee_employeeprofile` VALUES (409, 'EMP202601OPS035', '2021-12-07', 7370.07, 'active', NULL, '', '2025-12-29 00:00:00.000000', '2026-01-23 22:00:00.000000', 6, 1, 413);
INSERT INTO `employee_employeeprofile` VALUES (410, 'EMP202601MKT017', '2023-08-18', 12452.56, 'active', NULL, '', '2026-01-22 00:00:00.000000', '2026-01-24 18:00:00.000000', 3, 8, 414);
INSERT INTO `employee_employeeprofile` VALUES (411, 'EMP202601OPS036', '2023-12-21', 8913.21, 'active', NULL, '', '2026-01-24 00:00:00.000000', '2026-01-24 05:00:00.000000', 6, 7, 415);
INSERT INTO `employee_employeeprofile` VALUES (412, 'EMP202601OPS037', '2021-08-06', 13389.85, 'active', NULL, '', '2026-01-15 00:00:00.000000', '2026-01-24 18:00:00.000000', 6, 2, 416);
INSERT INTO `employee_employeeprofile` VALUES (413, 'EMP202601ADM026', '2025-12-26', 10092.31, 'resigned', '2026-01-16', '家庭原因', '2026-01-24 00:00:00.000000', '2026-01-24 14:00:00.000000', 9, 10, 417);

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
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of notice_notice
-- ----------------------------
INSERT INTO `notice_notice` VALUES (1, '测试公告', '123213', 1, 1, '2026-01-24 13:59:07.065629', '2026-01-24 13:58:57.875888', '2026-01-24 14:07:28.461323', 1);
INSERT INTO `notice_notice` VALUES (2, '2025年第三季度全员大会通知', '全体员工请注意，2025年第三季度全员大会将于7月15日下午2点在公司大会议室召开，请准时参加。会议议程包括：Q2工作总结、Q3工作计划、优秀员工表彰等。', 1, 1, '2025-07-01 09:00:00.000000', '2026-01-25 19:53:50.000000', '2026-01-25 19:53:50.000000', 2);
INSERT INTO `notice_notice` VALUES (3, '关于调整作息时间的通知', '为进一步提升工作效率，公司决定从2025年8月1日起调整工作时间。新的作息时间为：上午9:00-12:00，下午13:30-18:00。请各位同事知悉并相互转告。', 0, 1, '2025-07-20 10:00:00.000000', '2026-01-25 19:53:50.000000', '2026-01-25 19:53:50.000000', 2);
INSERT INTO `notice_notice` VALUES (4, '2025年中秋节放假安排', '根据国家法定节假日规定，2025年中秋节放假时间为9月15日至9月17日，共3天。9月14日（周日）正常上班。请各位同事提前安排好工作。', 1, 1, '2025-09-01 08:00:00.000000', '2026-01-25 19:53:50.000000', '2026-01-25 19:53:50.000000', 2);
INSERT INTO `notice_notice` VALUES (5, '关于开展2025年度员工体检的通知', '为保障员工身体健康，公司将于10月15日至10月30日组织年度体检。具体时间安排和注意事项将通过邮件发送，请留意查收。', 0, 1, '2025-09-25 14:00:00.000000', '2026-01-25 19:53:50.000000', '2026-01-25 19:53:50.000000', 2);
INSERT INTO `notice_notice` VALUES (6, '2025年国庆节放假通知', '国庆节放假时间为10月1日至10月7日，共7天。9月28日（周日）和10月11日（周六）正常上班。祝大家节日快乐！', 1, 1, '2025-09-28 09:00:00.000000', '2026-01-25 19:53:50.000000', '2026-01-25 19:53:50.000000', 2);
INSERT INTO `notice_notice` VALUES (7, '关于年终绩效考核的通知', '2025年度年终绩效考核将于12月1日正式启动，请各位员工提前准备年度工作总结和下年度工作计划。具体安排详见OA系统。', 0, 1, '2025-11-15 10:00:00.000000', '2026-01-25 19:53:50.000000', '2026-01-25 19:53:50.000000', 2);
INSERT INTO `notice_notice` VALUES (8, '2026年元旦放假通知', '2026年元旦放假时间为1月1日（周三）放假1天。12月31日（周二）下午可提前下班。请合理安排出行。', 1, 1, '2025-12-20 09:00:00.000000', '2026-01-25 19:53:50.000000', '2026-01-25 19:53:50.000000', 2);
INSERT INTO `notice_notice` VALUES (9, '关于春节假期安排的通知', '2026年春节放假时间为1月28日至2月6日，共10天。1月25日（周日）和2月8日（周日）正常上班。祝大家新年快乐！', 0, 1, '2025-12-25 14:00:00.000000', '2026-01-25 19:53:50.000000', '2026-01-25 19:53:50.000000', 2);
INSERT INTO `notice_notice` VALUES (10, '公司年度盛典邀请函', '诚邀各位同事参加2026年1月20日举办的年度盛典，届时将颁发优秀员工奖、最佳团队奖等多项大奖，并设有抽奖环节。请着正装出席。', 0, 1, '2026-01-05 16:00:00.000000', '2026-01-25 19:53:50.000000', '2026-01-25 19:53:50.000000', 2);

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
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
  `department_id` bigint NULL DEFAULT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `sort_order` int NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `code`(`code` ASC) USING BTREE,
  INDEX `idx_department_id`(`department_id` ASC) USING BTREE,
  CONSTRAINT `fk_post_department` FOREIGN KEY (`department_id`) REFERENCES `organization_department` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of organization_post
-- ----------------------------
INSERT INTO `organization_post` VALUES (1, '初级开发工程师', 'JDEV', 1, '负责基础开发工作，使用公司技术栈完成功能开发', 1, 1, '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000');
INSERT INTO `organization_post` VALUES (2, '中级开发工程师', 'MDEV', 1, '承担核心模块开发，指导初级工程师', 2, 1, '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000');
INSERT INTO `organization_post` VALUES (3, '高级开发工程师', 'SDEV', 1, '负责技术架构设计，攻克技术难题', 3, 1, '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000');
INSERT INTO `organization_post` VALUES (4, '技术总监', 'TD', 1, '技术团队管理，技术战略规划', 4, 1, '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000');
INSERT INTO `organization_post` VALUES (5, '产品经理', 'PM', 2, '产品规划，需求分析，项目管理', 5, 1, '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000');
INSERT INTO `organization_post` VALUES (6, 'UI/UX设计师', 'UI', 7, '界面设计，用户体验优化', 6, 1, '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000');
INSERT INTO `organization_post` VALUES (7, '人事专员', 'HRSP', 4, '招聘，员工关系，薪酬福利', 7, 1, '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000');
INSERT INTO `organization_post` VALUES (8, '财务专员', 'FASP', 5, '账务处理，财务报表，税务申报', 8, 1, '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000');
INSERT INTO `organization_post` VALUES (9, '运营专员', 'OPSP', 6, '日常运营，数据分析，活动策划', 9, 1, '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000');
INSERT INTO `organization_post` VALUES (10, '客户成功经理', 'CSM', 8, '客户服务，客户满意度维护', 10, 1, '2026-01-24 16:10:19.000000', '2026-01-24 16:10:19.000000');

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
) ENGINE = InnoDB AUTO_INCREMENT = 14 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of performance_performancereview
-- ----------------------------
INSERT INTO `performance_performancereview` VALUES (1, '2025-Q1', 5.0, '好', '好', '好', 'draft', '2026-01-24 15:32:48.447836', '2026-01-24 15:32:48.447836', 2, 1);
INSERT INTO `performance_performancereview` VALUES (2, '2025-Q1', 5.0, '优秀', '优秀', '优秀', 'draft', '2026-01-24 15:40:22.393695', '2026-01-24 15:40:22.393695', 3, 1);
INSERT INTO `performance_performancereview` VALUES (3, '2025-Q3', 5.0, '优秀', '优秀', '优秀', 'draft', '2026-01-24 15:41:22.623888', '2026-01-24 15:41:22.623888', 2, 1);
INSERT INTO `performance_performancereview` VALUES (4, '2025-01', 5.0, '优秀', '优秀', '优秀', 'draft', '2026-01-24 15:41:58.331549', '2026-01-24 15:41:58.331549', 2, 1);
INSERT INTO `performance_performancereview` VALUES (5, '2025-Q1', 5.0, '优秀', '优秀', '优秀', 'published', '2026-01-24 15:51:36.824303', '2026-01-24 16:00:14.381128', 6, 1);
INSERT INTO `performance_performancereview` VALUES (6, '2025-Q3', 4.5, '工作认真负责，技术能力提升明显，能够独立完成分配的任务。积极主动参与团队协作。', '建议加强跨部门沟通能力，提高文档输出质量。', '继续深化技术学习，争取独立负责项目。', 'published', '2026-01-25 19:53:50.000000', '2026-01-25 19:53:50.000000', 6, 2);
INSERT INTO `performance_performancereview` VALUES (7, '2025-Q3', 4.0, '工作态度积极，团队协作良好，能够按时完成工作任务。', '工作效率有待提升，需要加强时间管理。', '提高工作效率，优化工作方法。', 'published', '2026-01-25 19:53:50.000000', '2026-01-25 19:53:50.000000', 7, 2);
INSERT INTO `performance_performancereview` VALUES (8, '2025-Q3', 4.8, '表现出色，超额完成季度目标，创新能力强，获得客户好评。', '注意劳逸结合，适当休息。', '带领团队完成更多高质量项目。', 'published', '2026-01-25 19:53:50.000000', '2026-01-25 19:53:50.000000', 8, 2);
INSERT INTO `performance_performancereview` VALUES (9, '2025-Q4', 4.2, 'Q4表现稳定，在项目攻坚阶段表现出色，技术问题处理及时。', '代码规范性和文档输出需要加强。', '提升代码质量意识。', 'published', '2026-01-25 19:53:50.000000', '2026-01-25 19:53:50.000000', 6, 2);
INSERT INTO `performance_performancereview` VALUES (10, '2025-Q4', 4.5, 'Q4工作表现优秀，积极主动解决技术难题，为团队做出重要贡献。', '继续保持，多分享经验给新同事。', '成为技术骨干，指导新人。', 'published', '2026-01-25 19:53:50.000000', '2026-01-25 19:53:50.000000', 7, 2);
INSERT INTO `performance_performancereview` VALUES (11, '2025-Q4', 4.0, '按时完成工作任务，与同事相处融洽。', '需要提高主动性，多承担挑战性工作。', '设定更高的工作目标。', 'published', '2026-01-25 19:53:50.000000', '2026-01-25 19:53:50.000000', 8, 2);
INSERT INTO `performance_performancereview` VALUES (12, '2025-年度', 4.3, '全年表现良好，工作稳定，技术能力持续提升。团队协作意识强。', '跨部门沟通能力有待加强，演讲表达能力需提升。', '争取明年成为技术负责人。', 'published', '2026-01-25 19:53:50.000000', '2026-01-25 19:53:50.000000', 6, 2);
INSERT INTO `performance_performancereview` VALUES (13, '2025-年度', 4.1, '全年工作态度端正，遵守公司制度，与同事相处良好。', '专业技能深度有待加强。', '深入学习专业知识，提升竞争力。', 'draft', '2026-01-25 19:53:50.000000', '2026-01-25 19:53:50.000000', 7, 2);

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
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
  `salary_record_id` bigint NULL DEFAULT NULL,
  `exception_date` date NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `salary_exception_assigned_to_id_b493e5eb_fk_accounts_user_id`(`assigned_to_id` ASC) USING BTREE,
  INDEX `salary_exception_reported_by_id_3e6df770_fk_accounts_user_id`(`reported_by_id` ASC) USING BTREE,
  INDEX `salary_exception_salary_record_id_5c158ee5_fk_salary_sa`(`salary_record_id` ASC) USING BTREE,
  CONSTRAINT `salary_exception_assigned_to_id_b493e5eb_fk_accounts_user_id` FOREIGN KEY (`assigned_to_id`) REFERENCES `accounts_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `salary_exception_reported_by_id_3e6df770_fk_accounts_user_id` FOREIGN KEY (`reported_by_id`) REFERENCES `accounts_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `salary_exception_salary_record_id_5c158ee5_fk_salary_sa` FOREIGN KEY (`salary_record_id`) REFERENCES `salary_salaryrecord` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of salary_exception
-- ----------------------------
INSERT INTO `salary_exception` VALUES (1, 'salary_error', 'ces', 'resolved', '测试', 400.00, '2026-01-25 09:25:37.331122', '2026-01-25 09:25:13.323380', '2026-01-25 09:25:37.331122', 1, 1, 286, NULL);
INSERT INTO `salary_exception` VALUES (2, 'attendance_error', '123123', 'pending', '', 0.00, NULL, '2026-01-26 12:06:47.511195', '2026-01-26 12:06:47.511195', NULL, 2, 327, NULL);

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
) ENGINE = InnoDB AUTO_INCREMENT = 336 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
INSERT INTO `salary_salaryrecord` VALUES (289, '2025-07', 9500.00, 6.0, 300.00, 2, 0, 100.00, 9700.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 4);
INSERT INTO `salary_salaryrecord` VALUES (290, '2025-07', 10000.00, 10.0, 500.00, 0, 0, 0.00, 10500.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 6);
INSERT INTO `salary_salaryrecord` VALUES (291, '2025-07', 11000.00, 15.0, 750.00, 0, 1, 50.00, 11700.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 10);
INSERT INTO `salary_salaryrecord` VALUES (292, '2025-07', 9000.00, 8.0, 400.00, 1, 0, 50.00, 9350.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 7);
INSERT INTO `salary_salaryrecord` VALUES (293, '2025-07', 9500.00, 6.0, 300.00, 0, 0, 0.00, 9800.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 8);
INSERT INTO `salary_salaryrecord` VALUES (294, '2025-08', 8500.00, 6.0, 300.00, 0, 0, 100.00, 8700.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 2);
INSERT INTO `salary_salaryrecord` VALUES (295, '2025-08', 9000.00, 10.0, 500.00, 1, 0, 50.00, 9450.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 3);
INSERT INTO `salary_salaryrecord` VALUES (296, '2025-08', 9500.00, 8.0, 400.00, 0, 0, 0.00, 9900.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 4);
INSERT INTO `salary_salaryrecord` VALUES (297, '2025-08', 10000.00, 12.0, 600.00, 0, 0, 0.00, 10600.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 6);
INSERT INTO `salary_salaryrecord` VALUES (298, '2025-08', 11000.00, 10.0, 500.00, 2, 0, 100.00, 11400.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 10);
INSERT INTO `salary_salaryrecord` VALUES (299, '2025-08', 9000.00, 14.0, 700.00, 0, 0, 0.00, 9700.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 7);
INSERT INTO `salary_salaryrecord` VALUES (300, '2025-08', 9500.00, 8.0, 400.00, 1, 0, 50.00, 9850.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 8);
INSERT INTO `salary_salaryrecord` VALUES (301, '2025-09', 8500.00, 10.0, 500.00, 1, 0, 50.00, 8950.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 2);
INSERT INTO `salary_salaryrecord` VALUES (302, '2025-09', 9000.00, 8.0, 400.00, 0, 0, 0.00, 9400.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 3);
INSERT INTO `salary_salaryrecord` VALUES (303, '2025-09', 9500.00, 6.0, 300.00, 0, 0, 0.00, 9800.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 4);
INSERT INTO `salary_salaryrecord` VALUES (304, '2025-09', 10000.00, 12.0, 600.00, 0, 0, 0.00, 10600.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 6);
INSERT INTO `salary_salaryrecord` VALUES (305, '2025-09', 11000.00, 14.0, 700.00, 0, 0, 0.00, 11700.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 10);
INSERT INTO `salary_salaryrecord` VALUES (306, '2025-09', 9000.00, 6.0, 300.00, 2, 0, 100.00, 9200.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 7);
INSERT INTO `salary_salaryrecord` VALUES (307, '2025-09', 9500.00, 10.0, 500.00, 0, 1, 50.00, 9950.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 8);
INSERT INTO `salary_salaryrecord` VALUES (308, '2025-10', 8500.00, 15.0, 750.00, 0, 0, 0.00, 9250.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 2);
INSERT INTO `salary_salaryrecord` VALUES (309, '2025-10', 9000.00, 10.0, 500.00, 1, 0, 50.00, 9450.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 3);
INSERT INTO `salary_salaryrecord` VALUES (310, '2025-10', 9500.00, 8.0, 400.00, 0, 1, 50.00, 9850.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 4);
INSERT INTO `salary_salaryrecord` VALUES (311, '2025-10', 10000.00, 18.0, 900.00, 0, 0, 0.00, 10900.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 6);
INSERT INTO `salary_salaryrecord` VALUES (312, '2025-10', 11000.00, 12.0, 600.00, 0, 0, 0.00, 11600.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 10);
INSERT INTO `salary_salaryrecord` VALUES (313, '2025-10', 9000.00, 8.0, 400.00, 1, 0, 50.00, 9350.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 7);
INSERT INTO `salary_salaryrecord` VALUES (314, '2025-10', 9500.00, 12.0, 600.00, 0, 0, 0.00, 10100.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 8);
INSERT INTO `salary_salaryrecord` VALUES (315, '2025-11', 8500.00, 8.0, 400.00, 0, 0, 0.00, 8900.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 2);
INSERT INTO `salary_salaryrecord` VALUES (316, '2025-11', 9000.00, 14.0, 700.00, 0, 0, 0.00, 9700.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 3);
INSERT INTO `salary_salaryrecord` VALUES (317, '2025-11', 9500.00, 10.0, 500.00, 1, 0, 50.00, 9950.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 4);
INSERT INTO `salary_salaryrecord` VALUES (318, '2025-11', 10000.00, 8.0, 400.00, 0, 0, 0.00, 10400.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 6);
INSERT INTO `salary_salaryrecord` VALUES (319, '2025-11', 11000.00, 15.0, 750.00, 0, 0, 0.00, 11750.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 10);
INSERT INTO `salary_salaryrecord` VALUES (320, '2025-11', 9000.00, 6.0, 300.00, 2, 0, 100.00, 9200.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 7);
INSERT INTO `salary_salaryrecord` VALUES (321, '2025-11', 9500.00, 8.0, 400.00, 0, 0, 0.00, 9900.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 8);
INSERT INTO `salary_salaryrecord` VALUES (322, '2025-12', 8500.00, 12.0, 600.00, 1, 0, 50.00, 9050.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 2);
INSERT INTO `salary_salaryrecord` VALUES (323, '2025-12', 9000.00, 15.0, 750.00, 0, 0, 0.00, 9750.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 3);
INSERT INTO `salary_salaryrecord` VALUES (324, '2025-12', 9500.00, 14.0, 700.00, 0, 0, 0.00, 10200.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 4);
INSERT INTO `salary_salaryrecord` VALUES (325, '2025-12', 10000.00, 20.0, 1000.00, 0, 0, 0.00, 11000.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 6);
INSERT INTO `salary_salaryrecord` VALUES (326, '2025-12', 11000.00, 18.0, 900.00, 0, 1, 50.00, 11850.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 10);
INSERT INTO `salary_salaryrecord` VALUES (327, '2025-12', 9000.00, 10.0, 500.00, 0, 0, 0.00, 9500.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 7);
INSERT INTO `salary_salaryrecord` VALUES (328, '2025-12', 9500.00, 12.0, 600.00, 1, 0, 50.00, 10050.00, 'published', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 8);
INSERT INTO `salary_salaryrecord` VALUES (329, '2026-01', 8500.00, 8.0, 400.00, 0, 0, 0.00, 8900.00, 'draft', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 2);
INSERT INTO `salary_salaryrecord` VALUES (330, '2026-01', 9000.00, 10.0, 500.00, 1, 0, 50.00, 9450.00, 'draft', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 3);
INSERT INTO `salary_salaryrecord` VALUES (331, '2026-01', 9500.00, 8.0, 400.00, 0, 0, 0.00, 9900.00, 'draft', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 4);
INSERT INTO `salary_salaryrecord` VALUES (332, '2026-01', 10000.00, 12.0, 600.00, 2, 0, 100.00, 10500.00, 'draft', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 6);
INSERT INTO `salary_salaryrecord` VALUES (333, '2026-01', 11000.00, 14.0, 700.00, 0, 0, 0.00, 11700.00, 'draft', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 10);
INSERT INTO `salary_salaryrecord` VALUES (334, '2026-01', 9000.00, 6.0, 300.00, 1, 0, 50.00, 9250.00, 'draft', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 7);
INSERT INTO `salary_salaryrecord` VALUES (335, '2026-01', 9500.00, 10.0, 500.00, 0, 1, 50.00, 9950.00, 'draft', '2026-01-25 19:57:15.000000', '2026-01-25 19:57:15.000000', 8);

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
-- Procedure structure for generate_attendance_data
-- ----------------------------
DROP PROCEDURE IF EXISTS `generate_attendance_data`;
delimiter ;;
CREATE PROCEDURE `generate_attendance_data`(IN start_user_id INT, IN end_user_id INT, IN start_date DATE, IN end_date DATE)
BEGIN
    DECLARE curr_date DATE;
    DECLARE curr_user INT;
    DECLARE check_in TIME;
    DECLARE check_out TIME;
    DECLARE v_status VARCHAR(20);
    DECLARE is_weekend INT;
    DECLARE random_val INT;

    SET curr_date = start_date;
    WHILE curr_date <= end_date DO
        SET curr_user = start_user_id;
        WHILE curr_user <= end_user_id DO
            -- 跳过周末
            SET is_weekend = DAYOFWEEK(curr_date) IN (1, 7);

            IF is_weekend = 0 THEN
                -- 随机生成考勤状态 (80%正常, 10%迟到, 5%早退, 5%请假/缺勤)
                SET random_val = FLOOR(RAND() * 100);

                IF random_val < 80 THEN
                    -- 正常: 08:50-09:05签到, 18:00-18:10签退
                    SET check_in = TIME(CONCAT('0', FLOOR(8 + RAND()*0.2), ':', LPAD(FLOOR(RAND()*60), 2, '0'), ':00'));
                    SET check_out = TIME(CONCAT('18:', LPAD(FLOOR(RAND()*10), 2, '0'), ':00'));
                    SET v_status = 'normal';
                ELSEIF random_val < 90 THEN
                    -- 迟到: 09:05-09:30签到
                    SET check_in = TIME(CONCAT('09:', LPAD(FLOOR(RAND()*25)+5, 2, '0'), ':00'));
                    SET check_out = TIME(CONCAT('18:', LPAD(FLOOR(RAND()*10), 2, '0'), ':00'));
                    SET v_status = 'late';
                ELSEIF random_val < 95 THEN
                    -- 早退: 正常签到, 17:30-17:59签退
                    SET check_in = TIME(CONCAT('0', FLOOR(8 + RAND()*0.2), ':', LPAD(FLOOR(RAND()*60), 2, '0'), ':00'));
                    SET check_out = TIME(CONCAT('17:', LPAD(FLOOR(RAND()*30), 2, '0'), ':00'));
                    SET v_status = 'early';
                ELSE
                    -- 缺勤/请假
                    SET check_in = NULL;
                    SET check_out = NULL;
                    SET v_status = 'absent';
                END IF;

                -- 插入考勤记录 (使用REPLACE避免重复)
                REPLACE INTO attendance_attendance (date, check_in_time, check_out_time, status, created_at, updated_at, user_id)
                VALUES (curr_date, check_in, check_out, v_status, NOW(), NOW(), curr_user);
            END IF;

            SET curr_user = curr_user + 1;
        END WHILE;
        SET curr_date = DATE_ADD(curr_date, INTERVAL 1 DAY);
    END WHILE;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for generate_mock_employees
-- ----------------------------
DROP PROCEDURE IF EXISTS `generate_mock_employees`;
delimiter ;;
CREATE PROCEDURE `generate_mock_employees`()
BEGIN
    DECLARE i INT DEFAULT 101; -- 从 ID 101 开始
    DECLARE max_id INT DEFAULT 400; -- 生成到 400 (共300人)
    
    -- 变量定义
    DECLARE v_username VARCHAR(150);
    DECLARE v_realname VARCHAR(50);
    DECLARE v_phone VARCHAR(11);
    DECLARE v_email VARCHAR(254);
    DECLARE v_is_active TINYINT(1);
    DECLARE v_date_joined DATETIME;
    DECLARE v_role VARCHAR(20) DEFAULT 'employee';
    
    -- 档案变量
    DECLARE v_emp_no VARCHAR(20);
    DECLARE v_hire_date DATE;
    DECLARE v_status VARCHAR(20);
    DECLARE v_resigned_date DATE;
    DECLARE v_resigned_reason LONGTEXT;
    DECLARE v_salary DECIMAL(10,2);
    DECLARE v_dept_id BIGINT;
    DECLARE v_post_id BIGINT;
    
    -- 密码 (使用原有数据的 hash: pbkdf2_sha256...)
    DECLARE v_password VARCHAR(128) DEFAULT 'pbkdf2_sha256$1000000$lOIncR9jA2MJEekyudOSDO$7lK14sVM4WrLkfuuT+1RQCRMzA02fO3YLKKTzV11MZ0=';

    -- 循环插入
    WHILE i <= max_id DO
        
        -- ----------------------------
        -- 数据生成逻辑
        -- ----------------------------
        SET v_dept_id = FLOOR(1 + (RAND() * 10)); -- 随机部门 1-10
        SET v_post_id = FLOOR(1 + (RAND() * 10)); -- 随机岗位 1-10
        SET v_salary = 6000 + FLOOR(RAND() * 10000); -- 薪资 6000-16000
        
        -- 生成基础信息
        SET v_username = CONCAT('emp', LPAD(i, 4, '0')); -- 如 emp0101
        SET v_realname = CONCAT('员工', i); 
        SET v_phone = CONCAT('139', LPAD(i, 8, '0')); -- 确保唯一手机号
        SET v_email = CONCAT('emp', i, '@hrms.com');
        
        -- 初始化离职信息为空
        SET v_resigned_date = NULL;
        SET v_resigned_reason = '';

        -- ----------------------------
        -- 场景分支逻辑 (2026年1月 context)
        -- ----------------------------
        
        -- 场景A: 本月离职 (最后20个ID)
        IF i > 380 THEN
            SET v_is_active = 0;
            SET v_status = 'resigned';
            SET v_hire_date = DATE_ADD('2024-01-01', INTERVAL FLOOR(RAND() * 365) DAY); -- 24年入职
            SET v_resigned_date = DATE_ADD('2026-01-01', INTERVAL FLOOR(RAND() * 25) DAY); -- 本月离职
            SET v_resigned_reason = '个人原因发展，计划回老家发展。';
            SET v_date_joined = v_hire_date;
            SET v_emp_no = CONCAT('EMP', DATE_FORMAT(v_hire_date, '%Y%m'), 'RES', i);

        -- 场景B: 本月新入职 (351-380号)
        ELSEIF i > 350 THEN
            SET v_is_active = 1;
            SET v_status = 'probation'; -- 试用期
            SET v_hire_date = DATE_ADD('2026-01-01', INTERVAL FLOOR(RAND() * 25) DAY); -- 本月入职
            SET v_date_joined = v_hire_date;
            SET v_emp_no = CONCAT('EMP', '202601', 'NEW', i);

        -- 场景C: 普通老员工 (其余)
        ELSE
            SET v_is_active = 1;
            SET v_status = 'active';
            -- 入职时间随机分布在 2023-2025年
            SET v_hire_date = DATE_ADD('2023-01-01', INTERVAL FLOOR(RAND() * 1000) DAY);
            -- 确保入职日期不超过 2025-12-31
            IF v_hire_date > '2025-12-31' THEN 
                SET v_hire_date = '2025-12-01'; 
            END IF;
            SET v_date_joined = v_hire_date;
            SET v_emp_no = CONCAT('EMP', DATE_FORMAT(v_hire_date, '%Y%m'), 'NRM', i);
        END IF;

        -- ----------------------------
        -- 1. 插入 accounts_user
        -- ----------------------------
        INSERT INTO `accounts_user` (
            `password`, `last_login`, `is_superuser`, `username`, 
            `first_name`, `last_name`, `is_staff`, `is_active`, 
            `date_joined`, `phone`, `role`, `real_name`, `email`
        ) VALUES (
            v_password, 
            NULL, 
            0, -- 非超级用户
            v_username, 
            '', '', -- Django first/last name 留空
            0, -- 非 staff
            v_is_active, 
            v_date_joined, 
            v_phone, 
            v_role, 
            v_realname, 
            v_email
        );

        -- ----------------------------
        -- 2. 插入 employee_employeeprofile
        -- 注意：这里利用 LAST_INSERT_ID() 或者是循环变量 i (如果是全新库)
        -- 但为了安全，我们用刚插入的 user_id
        -- ----------------------------
        INSERT INTO `employee_employeeprofile` (
            `employee_no`, `hire_date`, `salary_base`, `status`, 
            `resigned_date`, `resigned_reason`, `created_at`, `updated_at`, 
            `department_id`, `post_id`, `user_id`
        ) VALUES (
            v_emp_no, 
            v_hire_date, 
            v_salary, 
            v_status, 
            v_resigned_date, 
            v_resigned_reason, 
            NOW(), 
            NOW(), 
            v_dept_id, 
            v_post_id, 
            (SELECT id FROM accounts_user WHERE username = v_username)
        );

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
