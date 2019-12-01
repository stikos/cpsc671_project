DELIMITER $$
DROP PROCEDURE IF EXISTS get_box $$
CREATE PROCEDURE get_box(IN latN FLOAT, IN latS FLOAT, IN lonE FLOAT, IN lonW FLOAT)
BEGIN
    SELECT geol_uid
    FROM geolocation
    WHERE lonW - lon <= 0
    AND   lonE - lon >= 0
    AND   latN - lat >= 0
    AND   latS - lat <= 0;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS get_coords_by_name $$
CREATE PROCEDURE get_coords_by_name(IN ctname TINYTEXT)
BEGIN
    SELECT geolocation.lat, geolocation.lon
    FROM geolocation, city
    WHERE  geolocation.geol_uid = city.geol_uid AND LOWER(city.name) = ctname;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS get_top_5 $$
CREATE PROCEDURE get_top_5(IN var_type_uid INTEGER, IN points TEXT)
BEGIN
    SELECT DISTINCT temp2.ptrn_id, temp2.ptrn, COUNT(temp2.geol_uid)
    FROM (
        SELECT *
        FROM (
              SELECT pattern.ptrn_id, pattern.ptrn, pattern.occurences, pattern.geol_uid
              FROM pattern, result_position
              WHERE pattern.ptrn_id = result_position.ptrn_id AND result_position.wvl_uid = var_type_uid) AS temp1
        WHERE  FIND_IN_SET(CAST(temp1.geol_uid AS CHAR), points) > 0) AS temp2
    GROUP BY temp2.ptrn_id
    ORDER BY COUNT(temp2.geol_uid) DESC LIMIT 5;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS get_patterns $$
CREATE PROCEDURE get_patterns(IN num_class INTEGER, IN points TEXT)
BEGIN
    SELECT AVG(CHAR_LENGTH(temp2.ptrn))
    FROM (
        SELECT temp1.ptrn
        FROM (
              SELECT pattern.ptrn, pattern.geol_uid
              FROM pattern, result_position
              WHERE pattern.ptrn_id = result_position.ptrn_id AND result_position.wvl_uid = num_class) AS temp1
        WHERE  FIND_IN_SET(CAST(temp1.geol_uid AS CHAR), points) > 0) AS temp2;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS get_cities $$
CREATE PROCEDURE get_cities()
BEGIN
    SELECT name
    FROM city;
END$$
DELIMITER ;

