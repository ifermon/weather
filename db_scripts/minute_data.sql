DROP TABLE IF EXISTS minute_data;
CREATE TABLE minute_data
(
       humidity      FLOAT(4, 2),
       light_level   INTEGER(10),
       temperature   FLOAT(4, 2),
       ts   TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);
