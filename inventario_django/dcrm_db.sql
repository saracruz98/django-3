-- SQL dump for Django project 'dcrm'
-- Import this file in phpMyAdmin (choose database dcrm_db).

DROP TABLE IF EXISTS `accounts_customuser`;
CREATE TABLE `accounts_customuser` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `password` VARCHAR(128) NOT NULL,
    `last_login` DATETIME NULL,
    `is_superuser` TINYINT(1) NOT NULL,
    `username` VARCHAR(150) NOT NULL UNIQUE,
    `first_name` VARCHAR(150) NOT NULL,
    `last_name` VARCHAR(150) NOT NULL,
    `email` VARCHAR(254) NOT NULL,
    `is_staff` TINYINT(1) NOT NULL,
    `is_active` TINYINT(1) NOT NULL,
    `date_joined` DATETIME NOT NULL,
    `telefono` VARCHAR(20) NULL,
    `rol` VARCHAR(20) NOT NULL DEFAULT 'customer'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Django auth tables (minimal set). You can let Django create them after configuring the DB,
-- but they are included here for convenience.
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `password` VARCHAR(128) NOT NULL,
    `last_login` DATETIME NULL,
    `is_superuser` TINYINT(1) NOT NULL,
    `username` VARCHAR(150) NOT NULL UNIQUE,
    `first_name` VARCHAR(150) NOT NULL,
    `last_name` VARCHAR(150) NOT NULL,
    `email` VARCHAR(254) NOT NULL,
    `is_staff` TINYINT(1) NOT NULL,
    `is_active` TINYINT(1) NOT NULL,
    `date_joined` DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(150) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `content_type_id` INT NOT NULL,
    `codename` VARCHAR(100) NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    UNIQUE (`content_type_id`, `codename`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Join tables
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `group_id` INT NOT NULL,
    UNIQUE (`user_id`, `group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `permission_id` INT NOT NULL,
    UNIQUE (`user_id`, `permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `app_label` VARCHAR(100) NOT NULL,
    `model` VARCHAR(100) NOT NULL,
    UNIQUE (`app_label`, `model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `app` VARCHAR(255) NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `applied` DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
