import pymysql

host = "127.0.0.1"
user = "root"
password = ""
db_name = "system_bd"

try:
    connection = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    print("successfully connected...")
    print("#" * 20)

    try:
        cursor = connection.cursor()

        with connection.cursor() as cursor:
            create_table_query = "CREATE TABLE `images`(id int AUTO_INCREMENT," \
                                 " name varchar(32)," \
                                 " face_analiz varchar(32)," \
                                 " images varchar(32), PRIMARY KEY (id));"
            cursor.execute(create_table_query)
            print("Table images created successfully")

        # insert data
        with connection.cursor() as cursor:
            insert_query = "INSERT INTO `images` (name, face_analiz, images) VALUES (" \
                           "'emilia-clarke', " \
                           "'[+] Статус: Студент гр ЭМС-19, возраст: 29 Пол: Woman', " \
                           "'emilia-clarke.jpg');"
            cursor.execute(insert_query)
            connection.commit()

        with connection.cursor() as cursor:
            create_table_query = "CREATE TABLE `picles`(id int AUTO_INCREMENT," \
                                 " picles varchar(32)," \
                                 " images blob, PRIMARY KEY (id));"
            cursor.execute(create_table_query)
            print("Table picles created successfully")

        with connection.cursor() as cursor:
            insert_query = "INSERT INTO `images` (name, face_analiz, images) VALUES (" \
                           "'emilia-clarke', " \
                           "'[+] Статус: Студент гр ЭМС-19, возраст: 29 Пол: Woman', " \
                           "'emilia-clarke.jpg');"
            cursor.execute(insert_query)
            connection.commit()

        with connection.cursor() as cursor:
            create_table_query = "CREATE TABLE `recognizers`(id int AUTO_INCREMENT," \
                                 " recognizers varchar(32), PRIMARY KEY (id));"
            cursor.execute(create_table_query)
            print("Table recognizers created successfully")

        with connection.cursor() as cursor:
            create_table_query = "CREATE TABLE `dataset_from_face`(id int AUTO_INCREMENT," \
                                 " name varchar(32)," \
                                 " images blob, PRIMARY KEY (id));"
            cursor.execute(create_table_query)
            print("Table dataset_from_face created successfully")


        with connection.cursor() as cursor:
            create_table_query = "CREATE TABLE `dataset_from_face_check`(id int AUTO_INCREMENT," \
                                 " name varchar(32)," \
                                 " images blob, PRIMARY KEY (id));"
            cursor.execute(create_table_query)
            print("Table dataset_from_face_check created successfully")

    finally:
        connection.close()

except Exception as ex:
    print("Connection refused...")
    print(ex)



