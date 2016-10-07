import MySQLdb as db


# Connect
conn = db.connect(host="localhost", user="weather_program", db="weather")

x = conn.cursor()

x.execute("""INSERT INTO minute_data (humidity, light_level, temperature) VALUES ({},{}, {})""".format(1.1, 2.3, 30))
conn.commit()
try:
    x.execute("""INSERT INTO minute_data (humidity, light_level, temperature) VALUES ({},{}, {})""".format(1.1, 2.3, 30))
except:
    print("did not work")
