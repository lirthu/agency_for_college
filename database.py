import pymysql

connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='root',
    database='agency'
)

cur = connection.cursor()


def get_user_role(user_id):
    cur.execute("SELECT role FROM user WHERE id_user = %s", (user_id,))
    user = cur.fetchone()

    if user[0] == 'client':
        return 'client'
    else:
        return 'admin'