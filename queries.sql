DELIMITER $$
DROP PROCEDURE IF EXISTS get_box $$
CREATE PROCEDURE get_box(IN latN FLOAT, IN latS FLOAT, IN lonE FLOAT, IN lonW FLOAT)
BEGIN
    SELECT geol_uid
    FROM geolocation
    WHERE lonW - lon >= 0
    AND   lonE - lon >= 0
    AND   latN - lat >= 0
    AND   latS - lat >= 0;
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