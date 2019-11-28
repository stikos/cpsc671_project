SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `raw_measurement`;
DROP TABLE IF EXISTS `geolocation`;
DROP TABLE IF EXISTS `weather_variable`;
DROP TABLE IF EXISTS `country`;
DROP TABLE IF EXISTS `city`;
DROP TABLE IF EXISTS `pattern`;
DROP TABLE IF EXISTS `pattern_class`;
DROP TABLE IF EXISTS `result_position`;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE `raw_measurement` (
    `raw_m_uid` INTEGER NOT NULL AUTO_INCREMENT,
    `wvl_uid` INTEGER NOT NULL,
    `date` DATE NOT NULL,
    `time` TIME NOT NULL,
    `geol_uid` INTEGER NOT NULL,
    `height` INTEGER NOT NULL,
    `vector_val` FLOAT NOT NULL,
    `vector_dir` TINYTEXT NOT NULL,
    PRIMARY KEY (`raw_m_uid`)
);

CREATE TABLE `geolocation` (
    `geol_uid` INTEGER NOT NULL AUTO_INCREMENT,
    `lat` FLOAT NOT NULL,
    `lon` FLOAT NOT NULL,
    `altitude` INTEGER NOT NULL,
    `ctr_uid` INTEGER NOT NULL,
    PRIMARY KEY (`geol_uid`)
);

CREATE TABLE `weather_variable` (
    `wvl_uid` INTEGER NOT NULL AUTO_INCREMENT,
    `variable` TINYTEXT NOT NULL,
    `description` TINYTEXT NOT NULL,
    PRIMARY KEY (`wvl_uid`)
);

CREATE TABLE `country` (
    `ctr_uid` INTEGER NOT NULL AUTO_INCREMENT,
    `name` TINYTEXT NOT NULL,
    PRIMARY KEY (`ctr_uid`)
);

CREATE TABLE `city` (
    `ct_uid` INTEGER NOT NULL AUTO_INCREMENT,
    `name` TINYTEXT NOT NULL,
    `geol_uid` INTEGER NOT NULL,
    PRIMARY KEY (`ct_uid`)
);

CREATE TABLE `pattern` (
    `ptrn_id` INTEGER NOT NULL,
    `ptrn` TINYTEXT NOT NULL,
    `length` INTEGER NOT NULL,
    `occurences` INTEGER NOT NULL,
    `geol_uid` INTEGER NOT NULL,
    PRIMARY KEY (`ptrn_id`)
);

CREATE TABLE `pattern_class` (
    `ptrn_c_uid` INTEGER NOT NULL AUTO_INCREMENT,
    `alphabet` TINYTEXT NOT NULL,
    `num_classes` INTEGER NOT NULL,
    PRIMARY KEY (`ptrn_c_uid`)
);

CREATE TABLE `result_position` (
    `res_pos_uid` INTEGER NOT NULL AUTO_INCREMENT,
    `ptrn_id` INTEGER NOT NULL,
    `wvl_uid` INTEGER NOT NULL,
    `position` INTEGER NOT NULL,
    PRIMARY KEY (`res_pos_uid`)
);
