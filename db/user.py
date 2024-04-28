from datetime import datetime

current_time = datetime.now()

def get_user(accountname, password, mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user where account_name='%s' and password='%s'" % (accountname, password))
    data = cur.fetchall()
    cur.close()
    return data 

def save_user(accountname, username, password, mysql):
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user (account_name, user_name, password, created_at) VALUES (%s, %s, %s, %s)", (accountname, username, password, datetime.now()))
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        print(e)
        return False