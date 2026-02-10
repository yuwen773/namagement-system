/*
 Navicat Premium Dump SQL

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80027 (8.0.27)
 Source Host           : localhost:3306
 Source Schema         : car_parts

 Target Server Type    : MySQL
 Target Server Version : 80027 (8.0.27)
 File Encoding         : 65001

 Date: 04/02/2026 18:07:04
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

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
) ENGINE = InnoDB AUTO_INCREMENT = 109 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 3, 'add_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 3, 'change_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 3, 'delete_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 3, 'view_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 2, 'add_group');
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 2, 'change_group');
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 2, 'delete_group');
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 2, 'view_group');
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
INSERT INTO `auth_permission` VALUES (25, 'Can add 收货地址', 7, 'add_useraddress');
INSERT INTO `auth_permission` VALUES (26, 'Can change 收货地址', 7, 'change_useraddress');
INSERT INTO `auth_permission` VALUES (27, 'Can delete 收货地址', 7, 'delete_useraddress');
INSERT INTO `auth_permission` VALUES (28, 'Can view 收货地址', 7, 'view_useraddress');
INSERT INTO `auth_permission` VALUES (29, 'Can add 商品属性', 11, 'add_productattribute');
INSERT INTO `auth_permission` VALUES (30, 'Can change 商品属性', 11, 'change_productattribute');
INSERT INTO `auth_permission` VALUES (31, 'Can delete 商品属性', 11, 'delete_productattribute');
INSERT INTO `auth_permission` VALUES (32, 'Can view 商品属性', 11, 'view_productattribute');
INSERT INTO `auth_permission` VALUES (33, 'Can add 商品', 10, 'add_product');
INSERT INTO `auth_permission` VALUES (34, 'Can change 商品', 10, 'change_product');
INSERT INTO `auth_permission` VALUES (35, 'Can delete 商品', 10, 'delete_product');
INSERT INTO `auth_permission` VALUES (36, 'Can view 商品', 10, 'view_product');
INSERT INTO `auth_permission` VALUES (37, 'Can add 商品分类', 8, 'add_category');
INSERT INTO `auth_permission` VALUES (38, 'Can change 商品分类', 8, 'change_category');
INSERT INTO `auth_permission` VALUES (39, 'Can delete 商品分类', 8, 'delete_category');
INSERT INTO `auth_permission` VALUES (40, 'Can view 商品分类', 8, 'view_category');
INSERT INTO `auth_permission` VALUES (41, 'Can add historical 商品', 9, 'add_historicalproduct');
INSERT INTO `auth_permission` VALUES (42, 'Can change historical 商品', 9, 'change_historicalproduct');
INSERT INTO `auth_permission` VALUES (43, 'Can delete historical 商品', 9, 'delete_historicalproduct');
INSERT INTO `auth_permission` VALUES (44, 'Can view historical 商品', 9, 'view_historicalproduct');
INSERT INTO `auth_permission` VALUES (45, 'Can add 商品图片', 12, 'add_productimage');
INSERT INTO `auth_permission` VALUES (46, 'Can change 商品图片', 12, 'change_productimage');
INSERT INTO `auth_permission` VALUES (47, 'Can delete 商品图片', 12, 'delete_productimage');
INSERT INTO `auth_permission` VALUES (48, 'Can view 商品图片', 12, 'view_productimage');
INSERT INTO `auth_permission` VALUES (49, 'Can add 订单', 13, 'add_order');
INSERT INTO `auth_permission` VALUES (50, 'Can change 订单', 13, 'change_order');
INSERT INTO `auth_permission` VALUES (51, 'Can delete 订单', 13, 'delete_order');
INSERT INTO `auth_permission` VALUES (52, 'Can view 订单', 13, 'view_order');
INSERT INTO `auth_permission` VALUES (53, 'Can add 订单商品', 14, 'add_orderitem');
INSERT INTO `auth_permission` VALUES (54, 'Can change 订单商品', 14, 'change_orderitem');
INSERT INTO `auth_permission` VALUES (55, 'Can delete 订单商品', 14, 'delete_orderitem');
INSERT INTO `auth_permission` VALUES (56, 'Can view 订单商品', 14, 'view_orderitem');
INSERT INTO `auth_permission` VALUES (57, 'Can add 退换货申请', 15, 'add_returnrequest');
INSERT INTO `auth_permission` VALUES (58, 'Can change 退换货申请', 15, 'change_returnrequest');
INSERT INTO `auth_permission` VALUES (59, 'Can delete 退换货申请', 15, 'delete_returnrequest');
INSERT INTO `auth_permission` VALUES (60, 'Can view 退换货申请', 15, 'view_returnrequest');
INSERT INTO `auth_permission` VALUES (61, 'Can add 优惠券', 16, 'add_coupon');
INSERT INTO `auth_permission` VALUES (62, 'Can change 优惠券', 16, 'change_coupon');
INSERT INTO `auth_permission` VALUES (63, 'Can delete 优惠券', 16, 'delete_coupon');
INSERT INTO `auth_permission` VALUES (64, 'Can view 优惠券', 16, 'view_coupon');
INSERT INTO `auth_permission` VALUES (65, 'Can add 用户优惠券', 17, 'add_usercoupon');
INSERT INTO `auth_permission` VALUES (66, 'Can change 用户优惠券', 17, 'change_usercoupon');
INSERT INTO `auth_permission` VALUES (67, 'Can delete 用户优惠券', 17, 'delete_usercoupon');
INSERT INTO `auth_permission` VALUES (68, 'Can view 用户优惠券', 17, 'view_usercoupon');
INSERT INTO `auth_permission` VALUES (69, 'Can add 推荐商品', 19, 'add_recommendedproduct');
INSERT INTO `auth_permission` VALUES (70, 'Can change 推荐商品', 19, 'change_recommendedproduct');
INSERT INTO `auth_permission` VALUES (71, 'Can delete 推荐商品', 19, 'delete_recommendedproduct');
INSERT INTO `auth_permission` VALUES (72, 'Can view 推荐商品', 19, 'view_recommendedproduct');
INSERT INTO `auth_permission` VALUES (73, 'Can add 推荐规则', 18, 'add_recommendationrule');
INSERT INTO `auth_permission` VALUES (74, 'Can change 推荐规则', 18, 'change_recommendationrule');
INSERT INTO `auth_permission` VALUES (75, 'Can delete 推荐规则', 18, 'delete_recommendationrule');
INSERT INTO `auth_permission` VALUES (76, 'Can view 推荐规则', 18, 'view_recommendationrule');
INSERT INTO `auth_permission` VALUES (77, 'Can add 常见问题', 20, 'add_faq');
INSERT INTO `auth_permission` VALUES (78, 'Can change 常见问题', 20, 'change_faq');
INSERT INTO `auth_permission` VALUES (79, 'Can delete 常见问题', 20, 'delete_faq');
INSERT INTO `auth_permission` VALUES (80, 'Can view 常见问题', 20, 'view_faq');
INSERT INTO `auth_permission` VALUES (81, 'Can add 改装案例', 21, 'add_modificationcase');
INSERT INTO `auth_permission` VALUES (82, 'Can change 改装案例', 21, 'change_modificationcase');
INSERT INTO `auth_permission` VALUES (83, 'Can delete 改装案例', 21, 'delete_modificationcase');
INSERT INTO `auth_permission` VALUES (84, 'Can view 改装案例', 21, 'view_modificationcase');
INSERT INTO `auth_permission` VALUES (85, 'Can add 系统配置', 24, 'add_systemconfig');
INSERT INTO `auth_permission` VALUES (86, 'Can change 系统配置', 24, 'change_systemconfig');
INSERT INTO `auth_permission` VALUES (87, 'Can delete 系统配置', 24, 'delete_systemconfig');
INSERT INTO `auth_permission` VALUES (88, 'Can view 系统配置', 24, 'view_systemconfig');
INSERT INTO `auth_permission` VALUES (89, 'Can add 站内消息', 22, 'add_message');
INSERT INTO `auth_permission` VALUES (90, 'Can change 站内消息', 22, 'change_message');
INSERT INTO `auth_permission` VALUES (91, 'Can delete 站内消息', 22, 'delete_message');
INSERT INTO `auth_permission` VALUES (92, 'Can view 站内消息', 22, 'view_message');
INSERT INTO `auth_permission` VALUES (93, 'Can add 操作日志', 23, 'add_operationlog');
INSERT INTO `auth_permission` VALUES (94, 'Can change 操作日志', 23, 'change_operationlog');
INSERT INTO `auth_permission` VALUES (95, 'Can delete 操作日志', 23, 'delete_operationlog');
INSERT INTO `auth_permission` VALUES (96, 'Can view 操作日志', 23, 'view_operationlog');
INSERT INTO `auth_permission` VALUES (97, 'Can add 商品评价', 25, 'add_review');
INSERT INTO `auth_permission` VALUES (98, 'Can change 商品评价', 25, 'change_review');
INSERT INTO `auth_permission` VALUES (99, 'Can delete 商品评价', 25, 'delete_review');
INSERT INTO `auth_permission` VALUES (100, 'Can view 商品评价', 25, 'view_review');
INSERT INTO `auth_permission` VALUES (101, 'Can add 购物车', 26, 'add_cart');
INSERT INTO `auth_permission` VALUES (102, 'Can change 购物车', 26, 'change_cart');
INSERT INTO `auth_permission` VALUES (103, 'Can delete 购物车', 26, 'delete_cart');
INSERT INTO `auth_permission` VALUES (104, 'Can view 购物车', 26, 'view_cart');
INSERT INTO `auth_permission` VALUES (105, 'Can add 购物车商品', 27, 'add_cartitem');
INSERT INTO `auth_permission` VALUES (106, 'Can change 购物车商品', 27, 'change_cartitem');
INSERT INTO `auth_permission` VALUES (107, 'Can delete 购物车商品', 27, 'delete_cartitem');
INSERT INTO `auth_permission` VALUES (108, 'Can view 购物车商品', 27, 'view_cartitem');

-- ----------------------------
-- Table structure for cart_items
-- ----------------------------
DROP TABLE IF EXISTS `cart_items`;
CREATE TABLE `cart_items`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `product_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `product_image` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` decimal(10, 2) NOT NULL,
  `quantity` int UNSIGNED NOT NULL,
  `subtotal` decimal(10, 2) NOT NULL,
  `added_at` datetime(6) NOT NULL,
  `cart_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `cart_items_cart_id_product_id_a57569aa_uniq`(`cart_id` ASC, `product_id` ASC) USING BTREE,
  INDEX `cart_items_product_id_9398bb89_fk_products_id`(`product_id` ASC) USING BTREE,
  CONSTRAINT `cart_items_cart_id_54d2714b_fk_carts_id` FOREIGN KEY (`cart_id`) REFERENCES `carts` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `cart_items_product_id_9398bb89_fk_products_id` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `cart_items_chk_1` CHECK (`quantity` >= 0)
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of cart_items
-- ----------------------------

-- ----------------------------
-- Table structure for carts
-- ----------------------------
DROP TABLE IF EXISTS `carts`;
CREATE TABLE `carts`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `total_items` int UNSIGNED NOT NULL,
  `total_price` decimal(10, 2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `carts_user_id_3a9d1785_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `carts_chk_1` CHECK (`total_items` >= 0)
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of carts
-- ----------------------------

-- ----------------------------
-- Table structure for categories
-- ----------------------------
DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `sort_order` int NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `parent_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `categories_parent_id_fc02df82_fk_categories_id`(`parent_id` ASC) USING BTREE,
  CONSTRAINT `categories_parent_id_fc02df82_fk_categories_id` FOREIGN KEY (`parent_id`) REFERENCES `categories` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of categories
-- ----------------------------
INSERT INTO `categories` VALUES (1, '发动机改装', 1, 1, '2026-02-04 06:13:22.346727', '2026-02-04 06:13:22.349863', NULL);
INSERT INTO `categories` VALUES (2, '悬挂系统', 2, 1, '2026-02-04 06:13:24.436335', '2026-02-04 06:13:24.437349', NULL);
INSERT INTO `categories` VALUES (3, '发动机改装', 1, 1, '2026-02-04 06:14:22.751807', '2026-02-04 06:14:22.751807', NULL);
INSERT INTO `categories` VALUES (4, '悬挂系统', 2, 1, '2026-02-04 06:14:24.802216', '2026-02-04 06:14:24.802216', NULL);
INSERT INTO `categories` VALUES (5, '发动机改装', 10, 1, '2026-02-04 06:15:02.115561', '2026-02-04 06:15:12.403894', NULL);

-- ----------------------------
-- Table structure for coupons
-- ----------------------------
DROP TABLE IF EXISTS `coupons`;
CREATE TABLE `coupons`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `discount_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `min_amount` decimal(10, 2) NOT NULL,
  `discount_amount` decimal(10, 2) NOT NULL,
  `discount_rate` decimal(5, 2) NULL DEFAULT NULL,
  `valid_from` datetime(6) NOT NULL,
  `valid_until` datetime(6) NOT NULL,
  `total_quantity` int NOT NULL,
  `per_user_limit` int NOT NULL,
  `issued_quantity` int NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `coupons_is_active_c4b38671`(`is_active` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of coupons
-- ----------------------------
INSERT INTO `coupons` VALUES (1, '测试优惠券', '', 'full_reduction', 100.00, 10.00, NULL, '2026-02-04 09:14:24.303758', '2026-03-06 09:14:24.303758', 0, 1, 0, 1, '2026-02-04 09:14:24.303758', '2026-02-04 09:14:24.305361');

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
  INDEX `django_admin_log_user_id_c564eba6_fk_users_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
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
) ENGINE = InnoDB AUTO_INCREMENT = 28 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (20, 'content', 'faq');
INSERT INTO `django_content_type` VALUES (21, 'content', 'modificationcase');
INSERT INTO `django_content_type` VALUES (4, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (16, 'marketing', 'coupon');
INSERT INTO `django_content_type` VALUES (17, 'marketing', 'usercoupon');
INSERT INTO `django_content_type` VALUES (26, 'orders', 'cart');
INSERT INTO `django_content_type` VALUES (27, 'orders', 'cartitem');
INSERT INTO `django_content_type` VALUES (13, 'orders', 'order');
INSERT INTO `django_content_type` VALUES (14, 'orders', 'orderitem');
INSERT INTO `django_content_type` VALUES (15, 'orders', 'returnrequest');
INSERT INTO `django_content_type` VALUES (8, 'products', 'category');
INSERT INTO `django_content_type` VALUES (9, 'products', 'historicalproduct');
INSERT INTO `django_content_type` VALUES (10, 'products', 'product');
INSERT INTO `django_content_type` VALUES (11, 'products', 'productattribute');
INSERT INTO `django_content_type` VALUES (12, 'products', 'productimage');
INSERT INTO `django_content_type` VALUES (25, 'products', 'review');
INSERT INTO `django_content_type` VALUES (18, 'recommendations', 'recommendationrule');
INSERT INTO `django_content_type` VALUES (19, 'recommendations', 'recommendedproduct');
INSERT INTO `django_content_type` VALUES (5, 'sessions', 'session');
INSERT INTO `django_content_type` VALUES (22, 'system', 'message');
INSERT INTO `django_content_type` VALUES (23, 'system', 'operationlog');
INSERT INTO `django_content_type` VALUES (24, 'system', 'systemconfig');
INSERT INTO `django_content_type` VALUES (6, 'users', 'user');
INSERT INTO `django_content_type` VALUES (7, 'users', 'useraddress');

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
) ENGINE = InnoDB AUTO_INCREMENT = 31 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2026-02-04 04:28:38.463669');
INSERT INTO `django_migrations` VALUES (2, 'contenttypes', '0002_remove_content_type_name', '2026-02-04 04:28:38.541737');
INSERT INTO `django_migrations` VALUES (3, 'auth', '0001_initial', '2026-02-04 04:28:38.760815');
INSERT INTO `django_migrations` VALUES (4, 'auth', '0002_alter_permission_name_max_length', '2026-02-04 04:28:38.809255');
INSERT INTO `django_migrations` VALUES (5, 'auth', '0003_alter_user_email_max_length', '2026-02-04 04:28:38.813934');
INSERT INTO `django_migrations` VALUES (6, 'auth', '0004_alter_user_username_opts', '2026-02-04 04:28:38.817068');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0005_alter_user_last_login_null', '2026-02-04 04:28:38.820437');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0006_require_contenttypes_0002', '2026-02-04 04:28:38.823529');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0007_alter_validators_add_error_messages', '2026-02-04 04:28:38.826295');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0008_alter_user_username_max_length', '2026-02-04 04:28:38.830997');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0009_alter_user_last_name_max_length', '2026-02-04 04:28:38.835628');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0010_alter_group_name_max_length', '2026-02-04 04:28:38.845248');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0011_update_proxy_permissions', '2026-02-04 04:28:38.849036');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0012_alter_user_first_name_max_length', '2026-02-04 04:28:38.853896');
INSERT INTO `django_migrations` VALUES (15, 'users', '0001_initial', '2026-02-04 04:28:39.115427');
INSERT INTO `django_migrations` VALUES (16, 'admin', '0001_initial', '2026-02-04 04:28:39.197227');
INSERT INTO `django_migrations` VALUES (17, 'admin', '0002_logentry_remove_auto_add', '2026-02-04 04:28:39.203504');
INSERT INTO `django_migrations` VALUES (18, 'admin', '0003_logentry_add_action_flag_choices', '2026-02-04 04:28:39.208113');
INSERT INTO `django_migrations` VALUES (19, 'sessions', '0001_initial', '2026-02-04 04:28:39.229976');
INSERT INTO `django_migrations` VALUES (20, 'users', '0002_user_nickname', '2026-02-04 04:29:55.125010');
INSERT INTO `django_migrations` VALUES (21, 'products', '0001_initial', '2026-02-04 05:53:33.188842');
INSERT INTO `django_migrations` VALUES (22, 'marketing', '0001_initial', '2026-02-04 06:30:45.404569');
INSERT INTO `django_migrations` VALUES (23, 'orders', '0001_initial', '2026-02-04 06:30:45.949836');
INSERT INTO `django_migrations` VALUES (24, 'marketing', '0002_initial', '2026-02-04 06:30:46.142188');
INSERT INTO `django_migrations` VALUES (25, 'products', '0002_delete_historicalproduct', '2026-02-04 06:55:20.542348');
INSERT INTO `django_migrations` VALUES (26, 'recommendations', '0001_initial', '2026-02-04 06:55:20.822119');
INSERT INTO `django_migrations` VALUES (27, 'content', '0001_initial', '2026-02-04 07:17:52.683085');
INSERT INTO `django_migrations` VALUES (28, 'system', '0001_initial', '2026-02-04 07:44:51.068296');
INSERT INTO `django_migrations` VALUES (29, 'products', '0003_review', '2026-02-04 09:25:53.835208');
INSERT INTO `django_migrations` VALUES (30, 'orders', '0002_cart_cartitem', '2026-02-04 10:00:41.814099');

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
INSERT INTO `django_session` VALUES ('2vlislilj8h058ct0o4lmrf4vxz5rdr9', '.eJxVjEEOwiAQRe_C2hBgcACX7nsGAsxUqoYmpV0Z765NutDtf-_9l4hpW2vcOi9xInER2ojT75hTeXDbCd1Tu82yzG1dpix3RR60y2Emfl4P9--gpl6_tcveMiprE7FDa_S5aAblRh8UZETrCzIGMIgjm8CmIDkCE7SGQADi_QHmHDb6:1vnYJz:X-0KCugJpKFdm2WlC_XDYwCLNNLIz5T3mYWSEs2z0Eo', '2026-02-18 08:33:11.890966');
INSERT INTO `django_session` VALUES ('3af9dl8drx62sc2cotsthuy6tdtkn1mo', '.eJxVjEEOwiAQRe_C2hBgcACX7nsGAsxUqoYmpV0Z765NutDtf-_9l4hpW2vcOi9xInER2ojT75hTeXDbCd1Tu82yzG1dpix3RR60y2Emfl4P9--gpl6_tcveMiprE7FDa_S5aAblRh8UZETrCzIGMIgjm8CmIDkCE7SGQADi_QHmHDb6:1vnYN8:X-2vtz22n929GX9ClDR_63dra9gJfF6t9duG38e9im8', '2026-02-18 08:36:26.807010');
INSERT INTO `django_session` VALUES ('l44bkq9cfek70lbdti5edmdpvmck7n2o', '.eJxVjEEOwiAQRe_C2hBgcACX7nsGAsxUqoYmpV0Z765NutDtf-_9l4hpW2vcOi9xInER2ojT75hTeXDbCd1Tu82yzG1dpix3RR60y2Emfl4P9--gpl6_tcveMiprE7FDa_S5aAblRh8UZETrCzIGMIgjm8CmIDkCE7SGQADi_QHmHDb6:1vnYLT:GyPnJO7HCpPX0-q3VRykOG7J8b4ymQIdTPl1ADkKq30', '2026-02-18 08:34:43.980973');
INSERT INTO `django_session` VALUES ('te17ipvets1yt2tvhs9vk9gsup9syjes', '.eJxVjEEOwiAQRe_C2hBgcACX7nsGAsxUqoYmpV0Z765NutDtf-_9l4hpW2vcOi9xInER2ojT75hTeXDbCd1Tu82yzG1dpix3RR60y2Emfl4P9--gpl6_tcveMiprE7FDa_S5aAblRh8UZETrCzIGMIgjm8CmIDkCE7SGQADi_QHmHDb6:1vnYIw:qZij_uOMkAuHK-sb5J4gDWYSm268HgyqDReEZnJI6wE', '2026-02-18 08:32:06.106770');
INSERT INTO `django_session` VALUES ('z7og2vvqh7g0u9cgxck65b12n3w98ekz', '.eJxVjEEOwiAQRe_C2hBgcACX7nsGAsxUqoYmpV0Z765NutDtf-_9l4hpW2vcOi9xInER2ojT75hTeXDbCd1Tu82yzG1dpix3RR60y2Emfl4P9--gpl6_tcveMiprE7FDa_S5aAblRh8UZETrCzIGMIgjm8CmIDkCE7SGQADi_QHmHDb6:1vnYNt:uU-IUNF07e2JfXTslDRfLo0xE7WWAd-lFs-XXfz85vg', '2026-02-18 08:37:13.126031');

-- ----------------------------
-- Table structure for faqs
-- ----------------------------
DROP TABLE IF EXISTS `faqs`;
CREATE TABLE `faqs`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `question` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `answer` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `category` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `sort_order` int NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `faqs_category_c955e843`(`category` ASC) USING BTREE,
  INDEX `faqs_is_active_cea6fb3d`(`is_active` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of faqs
-- ----------------------------
INSERT INTO `faqs` VALUES (2, '测试问题？', '这是测试答案', 'order', 1, 1, '2026-02-04 08:36:26.974164', '2026-02-04 08:36:26.974164');
INSERT INTO `faqs` VALUES (4, '测试问题？', '这是测试答案', 'order', 1, 1, '2026-02-04 08:37:13.302036', '2026-02-04 08:37:13.302036');

-- ----------------------------
-- Table structure for messages
-- ----------------------------
DROP TABLE IF EXISTS `messages`;
CREATE TABLE `messages`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `message_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `sent_at` datetime(6) NULL DEFAULT NULL,
  `read_at` datetime(6) NULL DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `recipient_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `messages_recipient_id_6dcabc5c_fk_users_id`(`recipient_id` ASC) USING BTREE,
  INDEX `messages_message_type_503315d4`(`message_type` ASC) USING BTREE,
  INDEX `messages_status_80880da1`(`status` ASC) USING BTREE,
  CONSTRAINT `messages_recipient_id_6dcabc5c_fk_users_id` FOREIGN KEY (`recipient_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of messages
-- ----------------------------
INSERT INTO `messages` VALUES (3, '测试公告', '这是测试公告内容', 'announcement', 'sent', '2026-02-04 08:36:27.022173', NULL, '2026-02-04 08:36:27.019578', NULL);
INSERT INTO `messages` VALUES (5, '测试公告', '这是测试公告内容', 'announcement', 'sent', '2026-02-04 08:37:13.363695', NULL, '2026-02-04 08:37:13.362128', NULL);

-- ----------------------------
-- Table structure for modification_cases
-- ----------------------------
DROP TABLE IF EXISTS `modification_cases`;
CREATE TABLE `modification_cases`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `summary` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `cover_image` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `author` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `view_count` int NOT NULL,
  `sort_order` int NOT NULL,
  `published_at` datetime(6) NULL DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `modification_cases_status_c0d0229b`(`status` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of modification_cases
-- ----------------------------
INSERT INTO `modification_cases` VALUES (2, '测试改装案例', '测试摘要', '测试内容', '', '', 'published', 0, 0, NULL, '2026-02-04 08:36:26.941167', '2026-02-04 08:36:26.941167');
INSERT INTO `modification_cases` VALUES (4, '测试改装案例', '测试摘要', '测试内容', '', '', 'published', 0, 0, NULL, '2026-02-04 08:37:13.258824', '2026-02-04 08:37:13.259354');

-- ----------------------------
-- Table structure for operation_logs
-- ----------------------------
DROP TABLE IF EXISTS `operation_logs`;
CREATE TABLE `operation_logs`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `action_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `object_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `object_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `detail` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `ip_address` char(39) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `user_agent` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `error_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `operator_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `operation_logs_operator_id_d13ee887_fk_users_id`(`operator_id` ASC) USING BTREE,
  INDEX `operation_logs_action_type_dccf7423`(`action_type` ASC) USING BTREE,
  INDEX `operation_logs_status_dde406a7`(`status` ASC) USING BTREE,
  INDEX `operation_logs_created_at_a9935f2e`(`created_at` ASC) USING BTREE,
  CONSTRAINT `operation_logs_operator_id_d13ee887_fk_users_id` FOREIGN KEY (`operator_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of operation_logs
-- ----------------------------

-- ----------------------------
-- Table structure for order_items
-- ----------------------------
DROP TABLE IF EXISTS `order_items`;
CREATE TABLE `order_items`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `product_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `product_image` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `product_price` decimal(10, 2) NOT NULL,
  `quantity` int UNSIGNED NOT NULL,
  `subtotal` decimal(10, 2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `order_id` bigint NOT NULL,
  `product_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `order_items_order_id_412ad78b_fk_orders_id`(`order_id` ASC) USING BTREE,
  INDEX `order_items_product_id_dd557d5a_fk_products_id`(`product_id` ASC) USING BTREE,
  CONSTRAINT `order_items_order_id_412ad78b_fk_orders_id` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `order_items_product_id_dd557d5a_fk_products_id` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `order_items_chk_1` CHECK (`quantity` >= 0)
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of order_items
-- ----------------------------
INSERT INTO `order_items` VALUES (1, '管理员创建的商品', '', 199.00, 1, 199.00, '2026-02-04 09:17:39.741646', 2, 5);

-- ----------------------------
-- Table structure for orders
-- ----------------------------
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_no` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `recipient_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `recipient_phone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `recipient_province` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `recipient_city` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `recipient_district` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `recipient_address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `total_amount` decimal(10, 2) NOT NULL,
  `discount_amount` decimal(10, 2) NOT NULL,
  `shipping_fee` decimal(10, 2) NOT NULL,
  `pay_amount` decimal(10, 2) NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `express_company` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `tracking_number` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `remark` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `paid_at` datetime(6) NULL DEFAULT NULL,
  `shipped_at` datetime(6) NULL DEFAULT NULL,
  `completed_at` datetime(6) NULL DEFAULT NULL,
  `coupon_id` bigint NULL DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `order_no`(`order_no` ASC) USING BTREE,
  INDEX `orders_coupon_id_a782d700_fk_user_coupons_id`(`coupon_id` ASC) USING BTREE,
  INDEX `orders_user_id_7e2523fb_fk_users_id`(`user_id` ASC) USING BTREE,
  INDEX `orders_status_17b834eb`(`status` ASC) USING BTREE,
  INDEX `orders_created_at_91ec19d2`(`created_at` ASC) USING BTREE,
  CONSTRAINT `orders_coupon_id_a782d700_fk_user_coupons_id` FOREIGN KEY (`coupon_id`) REFERENCES `user_coupons` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `orders_user_id_7e2523fb_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of orders
-- ----------------------------
INSERT INTO `orders` VALUES (1, '20260204171724344831', '测试收货人', '13800138000', '广东省', '深圳市', '南山区', '科技园路1号', 199.00, 0.00, 0.00, 199.00, 'pending_payment', '', '', '', '2026-02-04 09:17:24.948669', '2026-02-04 09:17:24.949301', NULL, NULL, NULL, NULL, 12);
INSERT INTO `orders` VALUES (2, '20260204171739904334', '测试收货人', '13800138000', '广东省', '深圳市', '南山区', '科技园路1号', 199.00, 0.00, 0.00, 199.00, 'pending_payment', '', '', '', '2026-02-04 09:17:39.738559', '2026-02-04 09:17:39.738559', NULL, NULL, NULL, NULL, 12);

-- ----------------------------
-- Table structure for product_attributes
-- ----------------------------
DROP TABLE IF EXISTS `product_attributes`;
CREATE TABLE `product_attributes`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `attr_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `attr_value` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `sort_order` int NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `product_attributes_product_id_78966835_fk_products_id`(`product_id` ASC) USING BTREE,
  CONSTRAINT `product_attributes_product_id_78966835_fk_products_id` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of product_attributes
-- ----------------------------

-- ----------------------------
-- Table structure for product_images
-- ----------------------------
DROP TABLE IF EXISTS `product_images`;
CREATE TABLE `product_images`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `sort_order` int NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `product_images_product_id_28ebf5f0_fk_products_id`(`product_id` ASC) USING BTREE,
  CONSTRAINT `product_images_product_id_28ebf5f0_fk_products_id` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of product_images
-- ----------------------------

-- ----------------------------
-- Table structure for products
-- ----------------------------
DROP TABLE IF EXISTS `products`;
CREATE TABLE `products`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` decimal(10, 2) NOT NULL,
  `original_price` decimal(10, 2) NOT NULL,
  `stock_quantity` int NOT NULL,
  `main_image` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `sales_count` int NOT NULL,
  `view_count` int NOT NULL,
  `is_featured` tinyint(1) NOT NULL,
  `is_new` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `category_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `products_category_id_a7a3a156_fk_categories_id`(`category_id` ASC) USING BTREE,
  CONSTRAINT `products_category_id_a7a3a156_fk_categories_id` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of products
-- ----------------------------
INSERT INTO `products` VALUES (2, '运动弹簧', '', 888.00, 0.00, 0, '', 'archived', 0, 0, 0, 0, '2026-02-04 06:15:18.616609', '2026-02-04 06:15:47.520625', 5);
INSERT INTO `products` VALUES (4, '测试商品', '', 100.00, 0.00, 0, '', 'draft', 0, 0, 0, 0, '2026-02-04 06:15:53.767155', '2026-02-04 06:15:53.767155', 5);
INSERT INTO `products` VALUES (5, '管理员创建的商品', '', 199.00, 0.00, 0, '', 'published', 0, 0, 0, 0, '2026-02-04 08:56:37.701422', '2026-02-04 08:56:37.708099', 1);

-- ----------------------------
-- Table structure for recommendation_rules
-- ----------------------------
DROP TABLE IF EXISTS `recommendation_rules`;
CREATE TABLE `recommendation_rules`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `rule_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `config` json NOT NULL,
  `priority` int NOT NULL,
  `limit` int NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `recommendation_rules_priority_dfb35ce9`(`priority` ASC) USING BTREE,
  INDEX `recommendation_rules_is_active_482b6a9a`(`is_active` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of recommendation_rules
-- ----------------------------

-- ----------------------------
-- Table structure for recommended_products
-- ----------------------------
DROP TABLE IF EXISTS `recommended_products`;
CREATE TABLE `recommended_products`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `sort_order` int NOT NULL,
  `remark` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `product_id` bigint NOT NULL,
  `rule_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `recommended_products_rule_id_product_id_98659122_uniq`(`rule_id` ASC, `product_id` ASC) USING BTREE,
  INDEX `recommended_products_product_id_f34a220d_fk_products_id`(`product_id` ASC) USING BTREE,
  CONSTRAINT `recommended_products_product_id_f34a220d_fk_products_id` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `recommended_products_rule_id_7f5b0bd5_fk_recommendation_rules_id` FOREIGN KEY (`rule_id`) REFERENCES `recommendation_rules` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of recommended_products
-- ----------------------------

-- ----------------------------
-- Table structure for return_requests
-- ----------------------------
DROP TABLE IF EXISTS `return_requests`;
CREATE TABLE `return_requests`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `request_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `reason` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `evidence_images` json NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `admin_note` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `processed_at` datetime(6) NULL DEFAULT NULL,
  `order_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `return_requests_order_id_627407af_fk_orders_id`(`order_id` ASC) USING BTREE,
  INDEX `return_requests_status_e3b84f6e`(`status` ASC) USING BTREE,
  INDEX `return_requests_created_at_9acd347b`(`created_at` ASC) USING BTREE,
  CONSTRAINT `return_requests_order_id_627407af_fk_orders_id` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of return_requests
-- ----------------------------

-- ----------------------------
-- Table structure for reviews
-- ----------------------------
DROP TABLE IF EXISTS `reviews`;
CREATE TABLE `reviews`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `order_item_id` int NULL DEFAULT NULL,
  `rating` smallint UNSIGNED NOT NULL,
  `comment` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `images` json NOT NULL,
  `is_anonymous` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `reviews_product_id_order_item_id_9ce69f2c_uniq`(`product_id` ASC, `order_item_id` ASC) USING BTREE,
  INDEX `reviews_user_id_c23b0903`(`user_id` ASC) USING BTREE,
  INDEX `reviews_order_item_id_78ca69ec`(`order_item_id` ASC) USING BTREE,
  CONSTRAINT `reviews_product_id_d4b78cfe_fk_products_id` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `reviews_chk_1` CHECK (`rating` >= 0)
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of reviews
-- ----------------------------

-- ----------------------------
-- Table structure for system_configs
-- ----------------------------
DROP TABLE IF EXISTS `system_configs`;
CREATE TABLE `system_configs`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `key` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `value` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `category` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_editable` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `key`(`key` ASC) USING BTREE,
  INDEX `system_configs_category_dcf9cbe0`(`category` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of system_configs
-- ----------------------------

-- ----------------------------
-- Table structure for user_addresses
-- ----------------------------
DROP TABLE IF EXISTS `user_addresses`;
CREATE TABLE `user_addresses`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `recipient_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `province` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `city` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `district` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_default` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_addresses_user_id_c7113441_fk_users_id`(`user_id` ASC) USING BTREE,
  INDEX `user_addresses_is_default_5a272cfe`(`is_default` ASC) USING BTREE,
  CONSTRAINT `user_addresses_user_id_c7113441_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_addresses
-- ----------------------------

-- ----------------------------
-- Table structure for user_coupons
-- ----------------------------
DROP TABLE IF EXISTS `user_coupons`;
CREATE TABLE `user_coupons`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `obtained_at` datetime(6) NOT NULL,
  `used_at` datetime(6) NULL DEFAULT NULL,
  `coupon_id` bigint NOT NULL,
  `used_order_id` bigint NULL DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_coupons_coupon_id_1ca6b254_fk_coupons_id`(`coupon_id` ASC) USING BTREE,
  INDEX `user_coupons_status_d188bc8d`(`status` ASC) USING BTREE,
  INDEX `user_coupons_used_order_id_30a754d2_fk_orders_id`(`used_order_id` ASC) USING BTREE,
  INDEX `user_coupons_user_id_353d52a0_fk_users_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `user_coupons_coupon_id_1ca6b254_fk_coupons_id` FOREIGN KEY (`coupon_id`) REFERENCES `coupons` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `user_coupons_used_order_id_30a754d2_fk_orders_id` FOREIGN KEY (`used_order_id`) REFERENCES `orders` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `user_coupons_user_id_353d52a0_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_coupons
-- ----------------------------
INSERT INTO `user_coupons` VALUES (1, 'unused', '2026-02-04 09:17:24.919653', NULL, 1, NULL, 12);

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `phone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `avatar` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `points` int NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `nickname` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `phone`(`phone` ASC) USING BTREE,
  INDEX `users_status_e50cb8ed`(`status` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (3, 'pbkdf2_sha256$1200000$Ah3AM0WTDWqUMxBxPBF3om$ruoesVCeTMXUpIHSYxjodihsqFp4t2lgzRUyyXA84FU=', NULL, 0, '', '', '', 0, 1, '2026-02-04 04:42:06.913730', '13800138010', '', 0, 'active', '2026-02-04 04:42:06.915340', '2026-02-04 04:42:07.811144', 'LoginTestUser');
INSERT INTO `users` VALUES (4, 'pbkdf2_sha256$1200000$XWWIkD6PzlQ471J0BuGb4p$FFgUYddSh0MN0hJNiV9SQRg1ESAc6AsawRK3gFVE6wk=', NULL, 0, '', '', '', 0, 1, '2026-02-04 04:42:18.636659', '13800138020', '', 0, 'active', '2026-02-04 04:42:18.636659', '2026-02-04 04:42:19.514967', 'MeTestUser');
INSERT INTO `users` VALUES (5, 'pbkdf2_sha256$1200000$5sdcIXKyqD127YLY03vGil$OmfpsX8QSuGa9wcQKlCqzs1RuAbIXhUj0rjyE/KWjJs=', NULL, 0, '', '', '', 0, 1, '2026-02-04 04:43:14.379924', '13800138011', '', 0, 'active', '2026-02-04 04:43:14.379924', '2026-02-04 04:43:14.791305', 'DirectTest');
INSERT INTO `users` VALUES (6, 'pbkdf2_sha256$1200000$dRmVXAeRh0oOeFcs8mHSzb$LmCUBvUpGSWSqxsJJhwAlu63SiJcLFeR/IzuyVMQFSg=', NULL, 0, '', '', 'test99@example.com', 0, 1, '2026-02-04 04:45:46.518317', '13800138099', '', 0, 'active', '2026-02-04 04:45:46.518317', '2026-02-04 04:45:46.928330', 'Test99');
INSERT INTO `users` VALUES (7, 'pbkdf2_sha256$1200000$0CYEiX0TXCzk4aQbmrEX6H$MxFOKqgt9nsI2JL/3jmO1uabyS/VdMzohV36ydgsxio=', NULL, 0, '', '', '', 0, 1, '2026-02-04 04:46:22.773807', '13800138100', '', 0, 'active', '2026-02-04 04:46:22.773807', '2026-02-04 04:46:23.260067', 'LoginTest');
INSERT INTO `users` VALUES (8, 'pbkdf2_sha256$1200000$6Ql3f4KsfMfV24YBEsl1qh$qiMkem0wuFhagibeArKUM0v6Mi/EYCyWgOT/6AzzFaw=', NULL, 0, '', '', '', 0, 1, '2026-02-04 04:49:33.630029', '13800138004', '', 0, 'active', '2026-02-04 04:49:33.630029', '2026-02-04 04:49:34.835292', '');
INSERT INTO `users` VALUES (9, 'pbkdf2_sha256$1200000$T57q5BrUf1IQE6IUBhoyhZ$yaJycsc9ysS0tg4FIR5AXS1gcAmp5SJZafCG73CCqZw=', NULL, 0, '', '', 'test1@example.com', 0, 1, '2026-02-04 04:50:35.844120', '13900139001', '', 0, 'active', '2026-02-04 04:50:35.844120', '2026-02-04 04:50:37.141960', 'TestUser1');
INSERT INTO `users` VALUES (12, 'pbkdf2_sha256$1200000$HrSdCgVJoGqZgtxrSlH01y$06zyd8HMSjc5t3acMZ3xUgXty6eMWCy9FOYswp6kJo0=', '2026-02-04 08:37:13.122899', 1, '', '', 'admin@test.com', 1, 1, '2026-02-04 04:55:27.203425', '13800138888', '', 0, 'active', '2026-02-04 04:55:27.203425', '2026-02-04 04:55:27.631485', 'AdminUser');
INSERT INTO `users` VALUES (13, 'pbkdf2_sha256$1200000$hoWtjDAu1RrqawN0nB5Avl$laKTAM1fCS9qjEwdFjjOrO0ersAWWCsQbisSK/gdTuU=', NULL, 0, '', '', '', 0, 1, '2026-02-04 05:04:34.608897', '13800138103', '', 0, 'active', '2026-02-04 05:04:34.608897', '2026-02-04 05:04:35.502031', '');
INSERT INTO `users` VALUES (14, 'pbkdf2_sha256$1200000$QX6r1qRg0QmpIHemhUYCm7$mR5qnq4CGkDX1Gh27vmfLW+dD3Ssn1Z4mxP+JV7pxbk=', NULL, 0, '', '', 'new@example.com', 0, 1, '2026-02-04 05:05:44.939753', '13900139002', '', 0, 'active', '2026-02-04 05:05:44.940316', '2026-02-04 05:05:45.789012', 'NewUser');
INSERT INTO `users` VALUES (15, 'pbkdf2_sha256$1200000$49c4Q8TMSYjuaGaEJajkhI$rlyBDNUkPOpLz3v0bZ1tAZ4CAAPsi/37Kn5WY4/zp8o=', NULL, 0, '', '', '', 0, 1, '2026-02-04 05:08:52.550346', '12345678901', '', 0, 'active', '2026-02-04 05:08:52.550346', '2026-02-04 05:08:53.403724', '');
INSERT INTO `users` VALUES (17, 'pbkdf2_sha256$1200000$FJFOHBvySjoInw3gqays3p$eJnAVDm26AMrQNVsw9nCXw9vpZD8o9gmuP7zVq8ukwY=', NULL, 1, '', '', '', 1, 1, '2026-02-04 08:57:47.176269', '13800138001', '', 0, 'active', '2026-02-04 08:57:47.176269', '2026-02-04 08:57:47.595273', '管理员测试');
INSERT INTO `users` VALUES (18, 'pbkdf2_sha256$1200000$ZzGlKk2pavovcnQQiJhXpK$xgRqvPLaTfzwXCQ0ALcRbRDFUhrD8jceyHDRDz2/QZ0=', NULL, 0, '', '', '', 0, 1, '2026-02-04 08:57:47.609901', '13800138002', '', 0, 'active', '2026-02-04 08:57:47.609901', '2026-02-04 08:57:48.037183', '普通用户测试');

-- ----------------------------
-- Table structure for users_groups
-- ----------------------------
DROP TABLE IF EXISTS `users_groups`;
CREATE TABLE `users_groups`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `users_groups_user_id_group_id_fc7788e8_uniq`(`user_id` ASC, `group_id` ASC) USING BTREE,
  INDEX `users_groups_group_id_2f3517aa_fk_auth_group_id`(`group_id` ASC) USING BTREE,
  CONSTRAINT `users_groups_group_id_2f3517aa_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `users_groups_user_id_f500bee5_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users_groups
-- ----------------------------

-- ----------------------------
-- Table structure for users_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `users_user_permissions`;
CREATE TABLE `users_user_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `users_user_permissions_user_id_permission_id_3b86cbdf_uniq`(`user_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `users_user_permissio_permission_id_6d08dcd2_fk_auth_perm`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `users_user_permissio_permission_id_6d08dcd2_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `users_user_permissions_user_id_92473840_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users_user_permissions
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
