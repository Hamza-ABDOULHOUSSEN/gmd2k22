import mysql.connector

host="neptune.telecomnancy.univ-lorraine.fr"
database="gmd"
login="gmd-read"
pwd="esial"

def main():
    conn = mysql.connector.connect(user=login, password=pwd, host=host, database=database)
    curs = conn.cursor()

    req = "SELECT * FROM meddra_all_se WHERE stitch_compound_id1 = 'CID103086685' AND stitch_compound_id2 = 'CID006450551'"

    table_list = []

    curs.execute(req)
    for table in curs.fetchall():
        table_list.append(table)

    n = len(table_list)

    print(n)
    print(table_list)

    req = "SELECT * FROM meddra WHERE meddra_id = '1412749'"

    table_list = []

    curs.execute(req)
    for table in curs.fetchall():
        table_list.append(table)

    n = len(table_list)

    print(table_list)
    '''
    for k in range(n-100, n):
        print(table_list[k])
    '''

    curs.close()


if __name__ == '__main__':
    main()