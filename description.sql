DROP TABLE IF EXISTS `raw_measurement`;
DROP TABLE IF EXISTS `geolocation`;
DROP TABLE IF EXISTS `weather_variable`;
DROP TABLE IF EXISTS `country`;
DROP TABLE IF EXISTS `city`;

CREATE TABLE `raw_measurement` (
    `raw_m_uid` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `wvl_uid` INTEGER NOT NULL,
    `time` TINYTEXT NOT NULL,
    `date` TINYTEXT NOT NULL,
    `geol_uid` INTEGER NOT NULL,
    `height` INTEGER NOT NULL,
    `vector_val` DECIMAL NOT NULL,
    `vector_dir` TINYTEXT NOT NULL
);

CREATE TABLE `geolocation` (
    `geol_uid` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `lat` FLOAT NOT NULL,
    `lon` FLOAT NOT NULL,
    `altitude` INTEGER NOT NULL,
    `ctr_uid` INTEGER NOT NULL
);

CREATE TABLE `weather_variable` (
    `wvl_uid` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `variable` TINYTEXT NOT NULL,
    `description` TINYTEXT NOT NULL
);

CREATE TABLE `country` (
    `ctr_uid` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` TINYTEXT NOT NULL
);

CREATE TABLE `city` (
    `ct_uid` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` TINYTEXT NOT NULL,
    `geol_uid` INTEGER NOT NULL
);
