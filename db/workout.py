from datetime import datetime

def get_workout(user_id, mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM workouts WHERE user_id=%s AND workout_date=%s", (user_id, datetime.now().date()))
    data = cur.fetchall()
    cur.close()
    return data 

def insert_workout(user_id, mysql):
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO workouts (user_id, workout_date) VALUES (%s, %s)", (user_id, datetime.now().date()))
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        print(e)
        return False


def get_total_workouts(user_id, mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(DISTINCT workout_date) AS total_training_days FROM workouts WHERE user_id =%s", (user_id,))
    data = cur.fetchall()
    print(data[0][0])
    cur.close()
    return data[0][0]