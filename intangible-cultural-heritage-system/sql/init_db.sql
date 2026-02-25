-- Intangible Cultural Heritage System database bootstrap script
-- Run with: mysql -u root -p < sql/init_db.sql
-- Default seeded admin account:
--   username: admin
--   password: Admin@123456

CREATE DATABASE IF NOT EXISTS heritage_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE heritage_db;

CREATE TABLE IF NOT EXISTS seed_categories (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  code VARCHAR(32) NOT NULL,
  name VARCHAR(64) NOT NULL,
  level SMALLINT NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_seed_categories_code (code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS seed_regions (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  country_code CHAR(2) NOT NULL,
  country_name VARCHAR(64) NOT NULL,
  latitude DECIMAL(9, 6) NOT NULL,
  longitude DECIMAL(9, 6) NOT NULL,
  continent VARCHAR(32) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_seed_regions_country_code (country_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DELIMITER $$

DROP PROCEDURE IF EXISTS init_heritage_seed_data $$
CREATE PROCEDURE init_heritage_seed_data()
BEGIN
  DECLARE has_auth_user INT DEFAULT 0;

  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    ROLLBACK;
    RESIGNAL;
  END;

  START TRANSACTION;

  INSERT INTO seed_categories (code, name, level)
  VALUES
    ('national', '国家级', 1),
    ('provincial', '省级', 2),
    ('city_county', '市县级', 3)
  ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    level = VALUES(level),
    updated_at = CURRENT_TIMESTAMP;

  INSERT INTO seed_regions (country_code, country_name, latitude, longitude, continent)
  VALUES
    ('CN', '中国', 35.861700, 104.195400, 'Asia'),
    ('JP', '日本', 36.204800, 138.252900, 'Asia'),
    ('KR', '韩国', 35.907800, 127.766900, 'Asia'),
    ('US', '美国', 37.090200, -95.712900, 'North America'),
    ('FR', '法国', 46.227600, 2.213700, 'Europe')
  ON DUPLICATE KEY UPDATE
    country_name = VALUES(country_name),
    latitude = VALUES(latitude),
    longitude = VALUES(longitude),
    continent = VALUES(continent),
    updated_at = CURRENT_TIMESTAMP;

  SELECT COUNT(1)
    INTO has_auth_user
    FROM information_schema.tables
   WHERE table_schema = DATABASE()
     AND table_name = 'auth_user';

  IF has_auth_user > 0 THEN
    INSERT INTO auth_user (
      password,
      last_login,
      is_superuser,
      username,
      first_name,
      last_name,
      email,
      is_staff,
      is_active,
      date_joined
    )
    VALUES (
      'pbkdf2_sha256$1000000$KxOEacFTHujc4927o4m0RJ$71TinwFZBN1Jwc3r1pUcS9Zc3/tbJEO3fDPDbyy+j+I=',
      NULL,
      1,
      'admin',
      '',
      '',
      'admin@example.com',
      1,
      1,
      CURRENT_TIMESTAMP
    )
    ON DUPLICATE KEY UPDATE
      is_superuser = VALUES(is_superuser),
      is_staff = VALUES(is_staff),
      is_active = VALUES(is_active),
      email = VALUES(email);
  END IF;

  COMMIT;
END $$

DELIMITER ;

CALL init_heritage_seed_data();
DROP PROCEDURE IF EXISTS init_heritage_seed_data;
