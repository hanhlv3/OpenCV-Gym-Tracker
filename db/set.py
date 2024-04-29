
def insert_set(user_id, workout_id, excercise_id, repetition_left, repetition_right, mysql):
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO sets (user_id, workout_id, excercise_id, repetition_left, repetition_right) VALUES (%s, %s, %s, %s, %s)", 
                    (user_id, workout_id, excercise_id, repetition_left, repetition_right))
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        print(e)
        return False

def get_total_set(user_id, mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(DISTINCT set_id) AS total_set FROM sets WHERE user_id =%s", (user_id,))
    data = cur.fetchall()
    print(data[0][0])
    cur.close()
    return data[0][0]

def get_total_left_right(user_id, mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT SUM(repetition_left), SUM(repetition_right) FROM sets WHERE user_id =%s", (user_id,))
    data = cur.fetchall()
    print(data[0][0], data[0][1])
    cur.close()
    return data[0][0], data[0][1]