import pickle

def load_dumbble_curl_model():
    with open("KNN_model.pkl", "wb") as file:
        dumbble_curl_model = pickle.load(file)
        print('lo')

    with open("./input_scaler.pkl", "rb") as file:
        input_scaler = pickle.load(file)
    print('hio')
    return dumbble_curl_model, input_scaler

# Determine important landmarks for plank
IMPORTANT_LMS_DUMBBLE_CURL = [
    "NOSE",
    "LEFT_SHOULDER",
    "RIGHT_SHOULDER",
    "RIGHT_ELBOW",
    "LEFT_ELBOW",
    "RIGHT_WRIST",
    "LEFT_WRIST",
    "LEFT_HIP",
    "RIGHT_HIP",
]

HEADERS = ["label"] # Label column


def get_headers_curl():
    for lm in IMPORTANT_LMS_DUMBBLE_CURL:
        HEADERS += [f"{lm.lower()}_x", f"{lm.lower()}_y", f"{lm.lower()}_z", f"{lm.lower()}_v"]
    return HEADERS
def extract_important_keypoints(results, landmarks) -> list:
    '''
    Extract important keypoints from mediapipe pose detection
    '''
    landmarks = results.pose_landmarks.landmark

    data = []
    for lm in IMPORTANT_LMS_DUMBBLE_CURL:
        keypoint = landmarks[mp_pose.PoseLandmark[lm].value]
        data.append([keypoint.x, keypoint.y, keypoint.z, keypoint.visibility])
    
    return np.array(data).flatten().tolist()