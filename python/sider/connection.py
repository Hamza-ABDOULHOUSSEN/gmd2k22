import mysql.connector

host="neptune.telecomnancy.univ-lorraine.fr"
database="gmd"
login="gmd-read"
pwd="esial"

def affiche(curs, table):
    req = f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'meddra'"
    print(req)
    req = f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}'"
    print(req)
    curs.execute(req)
    for line in curs.fetchall():
        print(line)


def test():
    conn = mysql.connector.connect(user=login, password=pwd, host=host, database=database)
    curs = conn.cursor()

    affiche(curs, "meddra")


def print_metadata():
    conn = mysql.connector.connect(user=login, password=pwd, host=host, database=database)
    curs = conn.cursor()

    req = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'"

    table_list = []

    curs.execute(req)
    for table in curs.fetchall():
        table_list.append(table[0])

    print(table_list)

    for table in table_list:
        req = f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}'"
        curs.execute(req)

        print(f"#### {table} ####")

        for line in curs.fetchall():
            print(line[3])

        print()

    curs.close()


def main():
    print_metadata()
    #test()

if __name__ == '__main__':
    main()