from flask import Flask, render_template, Response,jsonify, redirect, url_for, request, flash
import cv2
import numpy as np
import mediapipe as mp
from flask_mysqldb import MySQL
from db.user import get_user, save_user
from db.workout import get_workout, insert_workout, get_total_workouts,get_total_set_by_user_and_workout, get_total_left_right_by_date
from db.set import insert_set, get_total_set, get_total_left_right

# Initialize Flask app
app = Flask(__name__)

app.secret_key = 'hanhlevan'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gym_tracker'

mysql = MySQL(app)

# Initialize mediapipe pose class
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

show_message = False
counter_left = 0  # Define global variables for counters
counter_right = 0

counter = {
        1: {
            'right': 0,
            'left': 0,
        },
        2: {
            'right': 0,
            'left': 0,
        },
        3: {
            'right': 0,
            'left': 0,
        }
}


user = None

# Function to calculate the angle between three points
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle 

# Function to stream the video with landmarks and angles displayed
def video_stream(id):
    global counter_left, counter_right
    cap = cv2.VideoCapture(0)
    counter[id]['left'] = 0
    counter[id]['right'] = 0
    stage_left = None
    stage_right = None

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
        
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            
            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Calculate angles for left arm (similarly for right arm)
                # Left Arm
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                
                
                
               

                # Right Arm
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                
                #elbow angle
                left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
                
                #shoulder angle 
                left_shoulder_angle = calculate_angle(left_elbow, left_shoulder, left_hip)
                right_shoulder_angle = calculate_angle(right_elbow, right_shoulder, right_hip)
                
                #knee angle 
                knee_angle = calculate_angle(left_hip, left_knee, left_ankle)
                
                
                #Visualize angle
                if id == 1: 
                    # Visualize angle for left arm elbow
                    cv2.putText(image, f"Left Angle: {left_elbow_angle:.2f}", tuple(np.multiply(left_elbow, [640, 480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                    # Visualize angle for right arm elbow
                    cv2.putText(image, f"Right Angle: {right_elbow_angle:.2f}", tuple(np.multiply(right_elbow, [640, 480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                    # Counter logic for left arm
                
                    if left_elbow_angle > 160 and stage_left != 'down':
                        stage_left = "down"
                    if left_elbow_angle < 30 and stage_left == 'down':
                        stage_left = "up"
                        # Increase count value only when all landmarks are visible
                        counter[id]['left'] += 1
                      
                        if counter_left == 25:
                            counter_left = 0
                    # Inside the code block for right arm count
                    
                    if right_elbow_angle > 160 and stage_right != 'down':
                        stage_right = "down"
                    if right_elbow_angle < 30 and stage_right == 'down':
                        stage_right = "up"
                        # Increase count value only when all landmarks are visible
                        counter[id]['right'] += 1
                        if counter_right == 25:
                            counter_right = 0
                elif id == 2:
                    # Visualize angle for left arm shoulder
                    cv2.putText(image, f"Left Angle: {left_shoulder_angle:.2f}", tuple(np.multiply(left_shoulder, [640, 480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
  
                    # Visualize angle for right arm shoulder
                    cv2.putText(image, f"Right Angle: {right_shoulder_angle:.2f}", tuple(np.multiply(right_shoulder, [640, 480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                    if left_shoulder_angle >= 90 and stage_left == 'down': 
                            stage_left = "up"
                            counter[id]['left'] += 1
                    if left_shoulder_angle < 20 and stage_left != 'down' :
                            stage_left = "down"
                            
                    if right_shoulder_angle >= 90 and stage_right == 'down': 
                            stage_right = "up"
                            counter[id]['right'] += 1
                    if right_shoulder_angle < 20 and stage_right != 'down':
                            stage_right = "down" 
                elif id == 3:  
                    # Visualize angle for knee
                    cv2.putText(image, f"Left Angle: {knee_angle:.2f}", tuple(np.multiply(left_knee, [640, 480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                 # 3. Dumbbell Goblet Squat
                    if left_shoulder_angle < 90 and right_shoulder_angle < 90 and left_elbow_angle < 90 and right_shoulder_angle < 90:   
                        if knee_angle > 160 and stage_left == 'down':
                            stage_left = "up"
                            counter[id]['left'] += 1
                            counter[id]['right'] += 1
                        if knee_angle < 100 and stage_left != 'down': 
                            stage_left = "down"
                
            except:
                pass
            
            # Render counters
            cv2.putText(image, f"Left Count: {counter[id]['left']}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, f"Right Count: {counter[id]['right']}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )               
            
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()
    
# Route for the index page
@app.route('/')
def index():
    return render_template('home.html', user=user)



@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')

@app.route('/sign_in', methods=['POST'])
def sign_in_post():
    global user
    accountname = request.form.get('accountname')
    password = request.form.get('password')
    user = get_user(accountname, password, mysql)
    if user != ():
        tuple_value = user
        user_tuple = tuple_value[0]
        keys = ['id', 'accountname', 'user_name', 'password', 'created_at']
        user_dict = dict(zip(keys, user_tuple))
        user = user_dict
        
        ##  check workout
        workout = get_workout(user['id'], mysql)
        if workout == ():
           insert_workout(user['id'], mysql)
        
        return redirect(url_for('index'))
    else:
        # Login failed, show error message
        return redirect(url_for('sign_in'))

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html', user=user)

@app.route('/sign_up', methods=['POST'])
def sign_up_route():
    accountname = request.form.get('accountname')
    username = request.form.get('username')
    password = request.form.get('password')
    success = save_user(accountname, username, password, mysql)
    if success:
        # Sign up successful, redirect to home page
        return redirect(url_for('index'))
    else:
        # Sign up failed, show error message
        flash('Sign up failed')
        return redirect(url_for('sign_up'))


@app.route('/statical')
def statical():
    total_date = get_total_workouts(user['id'], mysql)
    total_set = get_total_set(user['id'], mysql)
    exercise_names, set_counts = get_total_set_by_user_and_workout(user['id'], mysql)
    repectition_left, repectition_right = get_total_left_right(user['id'], mysql)
    workout_date, total_set_day = get_total_left_right_by_date(user['id'], mysql)
    return render_template('statical.html', total_date=total_date, 
                           total_set=total_set, repectition_left=repectition_left,
                           repectition_right=repectition_right,
                           exercise_names = exercise_names  , set_counts = set_counts,
                           workout_date = workout_date, total_set_day = total_set_day)

@app.route('/excercise_type')
def display_excercise_type():
    return render_template('excercise_type.html')

@app.route('/dumbble_curl')
def dumbble_curl_page():
    global counter
    return render_template('dumbble_curl.html',counter_left=counter[1]['left'], counter_right=counter[1]['right'])

@app.route('/front_dumbble_raise')
def front_dumbble_raise_page():
    global counter 
    return render_template('front_dumbble_raise.html',counter_left=counter[2]['left'], counter_right=counter[2]['right'])

@app.route('/dumbble_squat')
def dumbble_squat_page():
    global counter 
    return render_template('dumbble_squat.html',counter_left=counter[3]['left'], counter_right=counter[3]['right'])



@app.route('/save_set/<int:id>')
def save_set(id):
    global counter, user
    workout = get_workout(user['id'], mysql)
    tuple_value = workout
    workout_tuple = tuple_value[0]
    keys = ['workout_id', 'user_id', 'workout_date']
    workout_dict = dict(zip(keys, workout_tuple))
    workout = workout_dict
    insert_set(user['id'], workout['workout_id'], id, counter[id]['left'], counter[id]['right'], mysql)
    if id == 1:
       return  redirect(url_for('dumbble_curl_page'))
    elif id == 2:
       return  redirect(url_for('front_dumbble_raise_page'))
    elif id == 3:
       return  redirect(url_for('dumbble_squat_page'))
    return render_template('home.html')


@app.route('/restart/<int:id>')
def restart(id):
    global counter
    counter[id]['left'] = 0
    counter[id]['right'] = 0
    if id == 1:
       return  redirect(url_for('dumbble_curl_page'))
    elif id == 2:
       return  redirect(url_for('front_dumbble_raise_page'))
    elif id == 3:
       return  redirect(url_for('dumbble_squat_page'))
    return render_template('home.html')

@app.route('/get_counts/<int:id>')
def get_counts(id):
    global counter
    # Return updated counts as JSON response
    return jsonify({'counter_left': counter[id]['left'], 'counter_right': counter[id]['right']})


# Route for video feed
@app.route('/video_feed/<int:id>')
def video_feed(id):
    print(id)
    return Response(video_stream(id), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
