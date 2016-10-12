TYPE=TRIGGERS
triggers='CREATE DEFINER=`ifermon`@`%` TRIGGER weather.tr_create_date_summary_values\n   BEFORE INSERT\n   ON weather.ten_minute_data\n   FOR EACH ROW\nBEGIN\n   SET NEW.start_time = FROM_UNIXTIME(NEW.start_time_epoch),\n       NEW.end_time = FROM_UNIXTIME(NEW.end_time_epoch),\n       NEW.month = FROM_UNIXTIME(NEW.start_time_epoch, \'%m\'),\n       NEW.year = FROM_UNIXTIME(NEW.start_time_epoch, \'%Y\'),\n       NEW.week = FROM_UNIXTIME(NEW.start_time_epoch, \'%U\');\nEND'
sql_modes=2097152
definers='ifermon@%'
client_cs_names='utf8'
connection_cl_names='utf8_general_ci'
db_cl_names='latin1_swedish_ci'
