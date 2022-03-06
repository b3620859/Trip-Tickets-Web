# pip install mysql-connector-python
import mysql.connector
from mysql.connector import Error
import datetime

class Database:

    def SaveData2MySQL(self, datas):
        db_settings = {
                            "host": "localhost",
                            "user": "root",
                            "password": "123",
                            "database": "trip-ticketsDB",
                            "charset": "utf8",
                            "auth_plugin": "mysql_native_password"
                        }
        try:
            # Connect local MySQL
            connect = mysql.connector.connect(**db_settings)

            if connect.is_connected():
                print("Connection Successful")
                db_Info = connect.get_server_info()
                print("Database version: ", db_Info)

                # Print Current database
                cursor = connect.cursor()
                cursor.execute("SELECT DATABASE();")
                record = cursor.fetchone()  # fetchone() Take out the first data
                # fetchall() Take out all the data
                print("Current database: ", record)


                # Add data SQL syntax
                sql_command = "INSERT INTO Test_Table (Id , Location, Title, Rate, Market_price, Sell_price, Link, Timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
                # Create table
                # cursor.execute("CREATE TABLE Test_Table (Id INT(11) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, Date VARCHAR(255), Name VARCHAR(255), Time VARCHAR(255)) DEFAULT CHARSET=utf8")
                cursor.execute("CREATE TABLE IF NOT EXISTS Test_Table (Num INT(11) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, Id INT(11) UNSIGNED NOT NULL, Location VARCHAR(255), Title VARCHAR(255), Rate VARCHAR(255), Market_price INT(11), Sell_price INT(11), Link VARCHAR(255), Timestamp INT(11)) DEFAULT CHARSET=utf8")
                # Write data to the database
                for input_data in datas:
                    cursor.execute(sql_command, input_data)  # values has placeholders
                connect.commit()  # SQL statement used for saving the changes

        except Error as e:
            print("Connection Unsuccessful: ", e)
            connect.rollback()

        finally:
            if connect.is_connected():
                cursor.close()
                connect.close()
                print("Database connection is closed")

# Id , Location, Title, Rate, Market_price, Sell_price, Link, Timestamp

"""
Test_Table
+--------------+------------------+------+-----+---------+----------------+
| Field        | Type             | Null | Key | Default | Extra          |
+--------------+------------------+------+-----+---------+----------------+
| Num          | int(11) unsigned | NO   | PRI | NULL    | auto_increment |
| Id           | int(11) unsigned | NO   |     | NULL    |                |
| Location     | varchar(255)     | YES  |     | NULL    |                |
| Title        | varchar(255)     | YES  |     | NULL    |                |
| Rate         | varchar(255)     | YES  |     | NULL    |                |
| Market_price | int(11)          | YES  |     | NULL    |                |
| Sell_price   | int(11)          | YES  |     | NULL    |                |
| Link         | varchar(255)     | YES  |     | NULL    |                |
| Timestamp    | int(11)          | YES  |     | NULL    |                |
+--------------+------------------+------+-----+---------+----------------+
9 rows in set (0.01 sec)
"""


"""
def main():
    db = Database()
    db.SaveData2MySQL()


if __name__ == "__main__":
    main()
"""
