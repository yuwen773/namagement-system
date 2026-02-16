CREATE DATABASE IF NOT EXISTS `energy_monitoring`
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;

USE `energy_monitoring`;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `em_energy_data`;
DROP TABLE IF EXISTS `em_energy_statistics`;
DROP TABLE IF EXISTS `em_alarms`;
DROP TABLE IF EXISTS `em_alarm_rules`;
DROP TABLE IF EXISTS `em_bills`;
DROP TABLE IF EXISTS `em_recharge_records`;
DROP TABLE IF EXISTS `em_notices`;
DROP TABLE IF EXISTS `em_operation_logs`;
DROP TABLE IF EXISTS `em_energy_forecasts`;
DROP TABLE IF EXISTS `em_devices`;
DROP TABLE IF EXISTS `em_rooms`;
DROP TABLE IF EXISTS `em_floors`;
DROP TABLE IF EXISTS `em_buildings`;
DROP TABLE IF EXISTS `em_campuses`;
DROP TABLE IF EXISTS `em_energy_types`;
DROP TABLE IF EXISTS `em_users`;
DROP TABLE IF EXISTS `em_roles`;

SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE `em_roles` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `code` VARCHAR(32) NOT NULL,
  `name` VARCHAR(64) NOT NULL,
  `description` VARCHAR(255) DEFAULT NULL,
  `is_active` TINYINT(1) NOT NULL DEFAULT 1,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_em_roles_code` (`code`),
  UNIQUE KEY `uk_em_roles_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `em_users` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(64) NOT NULL,
  `password` VARCHAR(128) NOT NULL,
  `email` VARCHAR(254) DEFAULT NULL,
  `real_name` VARCHAR(64) DEFAULT NULL,
  `phone` VARCHAR(32) DEFAULT NULL,
  `avatar` VARCHAR(255) DEFAULT NULL,
  `role_id` BIGINT UNSIGNED NOT NULL,
  `is_active` TINYINT(1) NOT NULL DEFAULT 1,
  `last_login_at` DATETIME(6) DEFAULT NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_em_users_username` (`username`),
  UNIQUE KEY `uk_em_users_email` (`email`),
  KEY `idx_em_users_role_id` (`role_id`),
  CONSTRAINT `fk_em_users_role_id` FOREIGN KEY (`role_id`) REFERENCES `em_roles` (`id`)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `em_campuses` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) NOT NULL,
  `code` VARCHAR(64) NOT NULL,
  `capacity` INT UNSIGNED DEFAULT NULL,
  `description` VARCHAR(255) DEFAULT NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_em_campuses_code` (`code`),
  UNIQUE KEY `uk_em_campuses_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `em_buildings` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `campus_id` BIGINT UNSIGNED NOT NULL,
  `name` VARCHAR(128) NOT NULL,
  `code` VARCHAR(64) NOT NULL,
  `area_type` ENUM('TEACHING', 'LIVING', 'OFFICE', 'MIXED', 'OTHER') NOT NULL DEFAULT 'OTHER',
  `address` VARCHAR(255) DEFAULT NULL,
  `floors_count` INT UNSIGNED NOT NULL DEFAULT 0,
  `built_year` SMALLINT UNSIGNED DEFAULT NULL,
  `gross_floor_area` DECIMAL(14, 2) DEFAULT NULL,
  `room_area` DECIMAL(14, 2) DEFAULT NULL,
  `capacity` INT UNSIGNED DEFAULT NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_em_buildings_code` (`code`),
  UNIQUE KEY `uk_em_buildings_campus_name` (`campus_id`, `name`),
  KEY `idx_em_buildings_campus_id` (`campus_id`),
  CONSTRAINT `fk_em_buildings_campus_id` FOREIGN KEY (`campus_id`) REFERENCES `em_campuses` (`id`)
    ON UPDATE CASCADE
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `em_floors` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `building_id` BIGINT UNSIGNED NOT NULL,
  `floor_number` INT NOT NULL,
  `name` VARCHAR(64) NOT NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_em_floors_building_floor_number` (`building_id`, `floor_number`),
  KEY `idx_em_floors_building_id` (`building_id`),
  CONSTRAINT `fk_em_floors_building_id` FOREIGN KEY (`building_id`) REFERENCES `em_buildings` (`id`)
    ON UPDATE CASCADE
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `em_rooms` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `floor_id` BIGINT UNSIGNED NOT NULL,
  `room_number` VARCHAR(32) NOT NULL,
  `room_type` ENUM('DORMITORY', 'OFFICE', 'CLASSROOM', 'LAB', 'PUBLIC', 'OTHER') NOT NULL DEFAULT 'OTHER',
  `area` DECIMAL(10, 2) DEFAULT NULL,
  `department` VARCHAR(128) DEFAULT NULL,
  `capacity` INT UNSIGNED DEFAULT NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_em_rooms_floor_room_number` (`floor_id`, `room_number`),
  KEY `idx_em_rooms_floor_id` (`floor_id`),
  CONSTRAINT `fk_em_rooms_floor_id` FOREIGN KEY (`floor_id`) REFERENCES `em_floors` (`id`)
    ON UPDATE CASCADE
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `em_energy_types` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(64) NOT NULL,
  `code` VARCHAR(32) NOT NULL,
  `unit` VARCHAR(32) NOT NULL,
  `icon` VARCHAR(128) DEFAULT NULL,
  `description` VARCHAR(255) DEFAULT NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_em_energy_types_code` (`code`),
  UNIQUE KEY `uk_em_energy_types_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `em_devices` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `device_id` VARCHAR(64) NOT NULL,
  `name` VARCHAR(128) NOT NULL,
  `energy_type_id` BIGINT UNSIGNED NOT NULL,
  `room_id` BIGINT UNSIGNED DEFAULT NULL,
  `model` VARCHAR(64) DEFAULT NULL,
  `status` ENUM('ONLINE', 'OFFLINE', 'FAULT') NOT NULL DEFAULT 'OFFLINE',
  `protocol` ENUM('MODBUS', 'BACNET', 'OTHER') NOT NULL DEFAULT 'OTHER',
  `gateway_mode` ENUM('GATEWAY_FORWARD', 'DIRECT_METER', 'OTHER') NOT NULL DEFAULT 'OTHER',
  `last_data_time` DATETIME(6) DEFAULT NULL,
  `installed_at` DATETIME(6) DEFAULT NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_em_devices_device_id` (`device_id`),
  KEY `idx_em_devices_energy_type_id` (`energy_type_id`),
  KEY `idx_em_devices_room_id` (`room_id`),
  KEY `idx_em_devices_status` (`status`),
  CONSTRAINT `fk_em_devices_energy_type_id` FOREIGN KEY (`energy_type_id`) REFERENCES `em_energy_types` (`id`)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,
  CONSTRAINT `fk_em_devices_room_id` FOREIGN KEY (`room_id`) REFERENCES `em_rooms` (`id`)
    ON UPDATE CASCADE
    ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `em_energy_data` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `device_id` BIGINT UNSIGNED NOT NULL,
  `energy_type_id` BIGINT UNSIGNED NOT NULL,
  `timestamp` DATETIME(6) NOT NULL,
  `value` DECIMAL(18, 6) NOT NULL,
  `voltage` DECIMAL(10, 3) DEFAULT NULL,
  `current` DECIMAL(10, 3) DEFAULT NULL,
  `power` DECIMAL(12, 3) DEFAULT NULL,
  `flow_rate` DECIMAL(12, 3) DEFAULT NULL,
  `source_type` ENUM('IMPORT', 'PROTOCOL', 'MANUAL') NOT NULL DEFAULT 'IMPORT',
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_em_energy_data_device_energy_time` (`device_id`, `energy_type_id`, `timestamp`),
  KEY `idx_em_energy_data_timestamp` (`timestamp`),
  KEY `idx_em_energy_data_device_timestamp` (`device_id`, `timestamp`),
  KEY `idx_em_energy_data_energy_type_timestamp` (`energy_type_id`, `timestamp`),
  CONSTRAINT `fk_em_energy_data_device_id` FOREIGN KEY (`device_id`) REFERENCES `em_devices` (`id`)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  CONSTRAINT `fk_em_energy_data_energy_type_id` FOREIGN KEY (`energy_type_id`) REFERENCES `em_energy_types` (`id`)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `em_energy_statistics` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `device_id` BIGINT UNSIGNED NOT NULL,
  `energy_type_id` BIGINT UNSIGNED NOT NULL,
  `period_type` ENUM('DAY', 'MONTH', 'YEAR') NOT NULL,
  `period_date` DATE NOT NULL,
  `total_value` DECIMAL(18, 6) NOT NULL DEFAULT 0,
  `peak_value` DECIMAL(18, 6) DEFAULT NULL,
  `peak_time` DATETIME(6) DEFAULT NULL,
  `avg_value` DECIMAL(18, 6) DEFAULT NULL,
  `cost` DECIMAL(14, 2) DEFAULT NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_em_energy_statistics_unique_period` (`device_id`, `energy_type_id`, `period_type`, `period_date`),
  KEY `idx_em_energy_statistics_period_date` (`period_date`),
  KEY `idx_em_energy_statistics_period_type_date` (`period_type`, `period_date`),
  CONSTRAINT `fk_em_energy_statistics_device_id` FOREIGN KEY (`device_id`) REFERENCES `em_devices` (`id`)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  CONSTRAINT `fk_em_energy_statistics_energy_type_id` FOREIGN KEY (`energy_type_id`) REFERENCES `em_energy_types` (`id`)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `em_alarm_rules` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) NOT NULL,
  `energy_type_id` BIGINT UNSIGNED NOT NULL,
  `condition_type` ENUM('THRESHOLD', 'MUTATION') NOT NULL,
  `threshold_value` DECIMAL(18, 6) NOT NULL,
  `comparison_operator` ENUM('GT', 'GTE', 'LT', 'LTE') NOT NULL DEFAULT 'GT',
  `is_active` TINYINT(1) NOT NULL DEFAULT 1,
  `description` VARCHAR(255) DEFAULT NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  KEY `idx_em_alarm_rules_energy_type_id` (`energy_type_id`),
  KEY `idx_em_alarm_rules_is_active` (`is_active`),
  CONSTRAINT `fk_em_alarm_rules_energy_type_id` FOREIGN KEY (`energy_type_id`) REFERENCES `em_energy_types` (`id`)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `em_alarms` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `device_id` BIGINT UNSIGNED NOT NULL,
  `rule_id` BIGINT UNSIGNED DEFAULT NULL,
  `alarm_type` ENUM('THRESHOLD', 'MUTATION', 'OFFLINE') NOT NULL,
  `alarm_value` DECIMAL(18, 6) DEFAULT NULL,
  `alarm_time` DATETIME(6) NOT NULL,
  `status` ENUM('PENDING', 'PROCESSED', 'IGNORED') NOT NULL DEFAULT 'PENDING',
  `handler_user_id` BIGINT UNSIGNED DEFAULT NULL,
  `handle_time` DATETIME(6) DEFAULT NULL,
  `remark` VARCHAR(500) DEFAULT NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  KEY `idx_em_alarms_device_id` (`device_id`),
  KEY `idx_em_alarms_rule_id` (`rule_id`),
  KEY `idx_em_alarms_alarm_time` (`alarm_time`),
  KEY `idx_em_alarms_status` (`status`),
  CONSTRAINT `fk_em_alarms_device_id` FOREIGN KEY (`device_id`) REFERENCES `em_devices` (`id`)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  CONSTRAINT `fk_em_alarms_rule_id` FOREIGN KEY (`rule_id`) REFERENCES `em_alarm_rules` (`id`)
    ON UPDATE CASCADE
    ON DELETE SET NULL,
  CONSTRAINT `fk_em_alarms_handler_user_id` FOREIGN KEY (`handler_user_id`) REFERENCES `em_users` (`id`)
    ON UPDATE CASCADE
    ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `em_bills` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `room_id` BIGINT UNSIGNED NOT NULL,
  `energy_type_id` BIGINT UNSIGNED NOT NULL,
  `bill_period` VARCHAR(7) NOT NULL,
  `usage` DECIMAL(18, 6) NOT NULL DEFAULT 0,
  `amount` DECIMAL(14, 2) NOT NULL DEFAULT 0,
  `status` ENUM('UNPAID', 'PAID') NOT NULL DEFAULT 'UNPAID',
  `due_date` DATE DEFAULT NULL,
  `paid_time` DATETIME(6) DEFAULT NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_em_bills_room_energy_period` (`room_id`, `energy_type_id`, `bill_period`),
  KEY `idx_em_bills_status` (`status`),
  KEY `idx_em_bills_due_date` (`due_date`),
  CONSTRAINT `fk_em_bills_room_id` FOREIGN KEY (`room_id`) REFERENCES `em_rooms` (`id`)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  CONSTRAINT `fk_em_bills_energy_type_id` FOREIGN KEY (`energy_type_id`) REFERENCES `em_energy_types` (`id`)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `em_recharge_records` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `room_id` BIGINT UNSIGNED NOT NULL,
  `amount` DECIMAL(14, 2) NOT NULL,
  `payment_method` VARCHAR(32) NOT NULL,
  `recharge_time` DATETIME(6) NOT NULL,
  `operator_user_id` BIGINT UNSIGNED DEFAULT NULL,
  `remark` VARCHAR(255) DEFAULT NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  KEY `idx_em_recharge_records_room_id` (`room_id`),
  KEY `idx_em_recharge_records_recharge_time` (`recharge_time`),
  CONSTRAINT `fk_em_recharge_records_room_id` FOREIGN KEY (`room_id`) REFERENCES `em_rooms` (`id`)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  CONSTRAINT `fk_em_recharge_records_operator_user_id` FOREIGN KEY (`operator_user_id`) REFERENCES `em_users` (`id`)
    ON UPDATE CASCADE
    ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `em_notices` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(200) NOT NULL,
  `content` TEXT NOT NULL,
  `notice_type` ENUM('NOTICE', 'ANNOUNCEMENT', 'KNOWLEDGE') NOT NULL DEFAULT 'NOTICE',
  `priority` ENUM('LOW', 'MEDIUM', 'HIGH', 'URGENT') NOT NULL DEFAULT 'MEDIUM',
  `publish_time` DATETIME(6) DEFAULT NULL,
  `is_published` TINYINT(1) NOT NULL DEFAULT 0,
  `publisher_user_id` BIGINT UNSIGNED DEFAULT NULL,
  `target_role` ENUM('ALL', 'ADMIN', 'USER') NOT NULL DEFAULT 'ALL',
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  KEY `idx_em_notices_notice_type` (`notice_type`),
  KEY `idx_em_notices_publish_time` (`publish_time`),
  KEY `idx_em_notices_is_published` (`is_published`),
  CONSTRAINT `fk_em_notices_publisher_user_id` FOREIGN KEY (`publisher_user_id`) REFERENCES `em_users` (`id`)
    ON UPDATE CASCADE
    ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `em_operation_logs` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` BIGINT UNSIGNED DEFAULT NULL,
  `action` VARCHAR(64) NOT NULL,
  `resource` VARCHAR(128) NOT NULL,
  `ip_address` VARCHAR(45) DEFAULT NULL,
  `user_agent` VARCHAR(512) DEFAULT NULL,
  `request_method` VARCHAR(16) DEFAULT NULL,
  `request_path` VARCHAR(255) DEFAULT NULL,
  `create_time` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  KEY `idx_em_operation_logs_user_id` (`user_id`),
  KEY `idx_em_operation_logs_action` (`action`),
  KEY `idx_em_operation_logs_create_time` (`create_time`),
  CONSTRAINT `fk_em_operation_logs_user_id` FOREIGN KEY (`user_id`) REFERENCES `em_users` (`id`)
    ON UPDATE CASCADE
    ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `em_energy_forecasts` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `energy_type_id` BIGINT UNSIGNED NOT NULL,
  `scope_type` ENUM('CAMPUS', 'BUILDING', 'DEVICE') NOT NULL,
  `dimension_key` VARCHAR(128) NOT NULL,
  `campus_id` BIGINT UNSIGNED DEFAULT NULL,
  `building_id` BIGINT UNSIGNED DEFAULT NULL,
  `device_id` BIGINT UNSIGNED DEFAULT NULL,
  `target_date` DATE NOT NULL,
  `horizon_days` INT UNSIGNED NOT NULL,
  `forecast_value` DECIMAL(18, 6) NOT NULL,
  `lower_bound` DECIMAL(18, 6) DEFAULT NULL,
  `upper_bound` DECIMAL(18, 6) DEFAULT NULL,
  `model_name` VARCHAR(64) DEFAULT NULL,
  `generated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_em_energy_forecasts_unique_dimension` (`dimension_key`, `energy_type_id`, `target_date`, `horizon_days`),
  KEY `idx_em_energy_forecasts_scope_type` (`scope_type`),
  KEY `idx_em_energy_forecasts_target_date` (`target_date`),
  KEY `idx_em_energy_forecasts_energy_type_id` (`energy_type_id`),
  KEY `idx_em_energy_forecasts_campus_id` (`campus_id`),
  KEY `idx_em_energy_forecasts_building_id` (`building_id`),
  KEY `idx_em_energy_forecasts_device_id` (`device_id`),
  CONSTRAINT `fk_em_energy_forecasts_energy_type_id` FOREIGN KEY (`energy_type_id`) REFERENCES `em_energy_types` (`id`)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,
  CONSTRAINT `fk_em_energy_forecasts_campus_id` FOREIGN KEY (`campus_id`) REFERENCES `em_campuses` (`id`)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,
  CONSTRAINT `fk_em_energy_forecasts_building_id` FOREIGN KEY (`building_id`) REFERENCES `em_buildings` (`id`)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,
  CONSTRAINT `fk_em_energy_forecasts_device_id` FOREIGN KEY (`device_id`) REFERENCES `em_devices` (`id`)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
