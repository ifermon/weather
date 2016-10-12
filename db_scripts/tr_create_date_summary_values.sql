DROP TRIGGER IF EXISTS weather.tr_create_date_summary_values;

CREATE TRIGGER weather.tr_create_date_summary_values
   BEFORE INSERT
   ON weather.ten_minute_data
   FOR EACH ROW
BEGIN
   SET NEW.start_time = FROM_UNIXTIME(NEW.start_time_epoch),
       NEW.end_time = FROM_UNIXTIME(NEW.end_time_epoch),
       NEW.month = FROM_UNIXTIME(NEW.start_time_epoch, '%m'),
       NEW.year = FROM_UNIXTIME(NEW.start_time_epoch, '%Y'),
       NEW.week = FROM_UNIXTIME(NEW.start_time_epoch, '%U');
END
