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


def get_total_set_by_user_and_workout(user_id, mysql):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT e.excercise_name, COUNT(*) AS total_sets 
        FROM excercises e 
        INNER JOIN sets s ON e.excercise_id = s.excercise_id 
        INNER JOIN user u ON s.user_id = u.id
        WHERE u.id = %s
        GROUP BY e.excercise_name
    """, (user_id,))
    data = cur.fetchall()
    exercise_names = [item[0] for item in data]
    set_counts = [item[1] for item in data]
    
    cur.close()

    return exercise_names, set_counts

def get_total_left_right_by_date(user_id, mysql):
    cur = mysql.connection.cursor()
    cur.execute('''
            SELECT workout_date, COUNT(*) AS total_sets
            FROM workouts
            INNER JOIN sets s ON workouts.workout_id = s.workout_id
            WHERE s.user_id = %s
            GROUP BY workout_date
            ORDER BY workout_date
        ''', (user_id,))
    data = cur.fetchall()
    workout_da = [item[0] for item in data]
    total_set_day = [item[1] for item in data] 
    workout_date = [date.strftime('%Y-%m-%d') for date in workout_da]
    print(workout_date, total_set_day)
    cur.close()
    return workout_date, total_set_day

def get_work_out_recent(user_id, mysql):
    cur = mysql.connection.cursor()
    cur.execute('''
           SELECT excercise_name, sets.repetition_left, sets.repetition_right,  workout_date
            FROM sets INNER JOIN `user` ON sets.user_id = `user`.id
            INNER JOIN excercises on sets.excercise_id = excercises.excercise_id
            INNER JOIN workouts on sets.workout_id = workouts.workout_id
            WHERE sets.user_id = %s	
            ORDER BY workout_date DESC
        ''', (user_id,))
    data = cur.fetchall()
    cur.close()
    formatted_data = [(a, b, c, d.strftime('%Y-%m-%d')) for a, b, c, d in data]
    array_data = [list(item) for item in formatted_data]
    print(array_data)
    return array_data
    