CREATE TABLE ten_minute_data
(
       avg_temperature    FLOAT(4, 2),
       avg_humidity       FLOAT(4, 2),
       avg_light_level    FLOAT(8, 2),
       power              INT(10),
       start_time_epoch   VARCHAR(50),
       end_time_epoch     VARCHAR(50),
       start_time         DATETIME,
       end_time           DATETIME,
       month              VARCHAR(20),
       `year`             VARCHAR(5),
       week               VARCHAR(3)
)
