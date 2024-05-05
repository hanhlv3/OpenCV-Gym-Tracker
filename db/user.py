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

def get_workout_by_date(user_id, date, mysql):
    cur = mysql.connection.cursor()
    
    cur.execute('''
            SELECT w.workout_date, e.excercise_name, count(e.excercise_name)
            FROM workouts w
            INNER JOIN sets s ON w.workout_id = s.workout_id
            INNER JOIN excercises e ON s.excercise_id = e.excercise_id
            WHERE w.user_id = %s AND w.workout_date = %s
            GROUP BY e.excercise_name
        ''', (user_id, date))
    data = cur.fetchall()
    cur.close()
    print(data)
   
    return data