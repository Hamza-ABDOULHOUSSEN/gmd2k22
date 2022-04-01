import mysql.connector

host="neptune.telecomnancy.univ-lorraine.fr"
database="gmd"
login="gmd-read"
pwd="esial"

def print_metadata():
    conn = mysql.connector.connect(user=login, password=pwd, host=host, database=database)
    curs = conn.cursor()

    req = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'"

    table_list = []

    curs.execute(req)
    for table in curs.fetchall():
        table_list.append(table[0])

    stmt = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = %(table)s"

    for table in table_list:

        curs.execute(stmt, { 'table': table })

        print(f"#### {table} ####")

        for line in curs.fetchall():
            print(line[3])

        print()

    curs.close()


def main():
    print_metadata()

if __name__ == '__main__':
    main()