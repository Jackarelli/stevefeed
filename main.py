from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)


#camera_url = "rtsp://Admin1:Admin1@192.168.0.187/live0"
camera_url = "rtsp://Steve1:Steve1@86.13.176.186:2525/live1"
def gen_frames():
    cap = cv2.VideoCapture(camera_url)  # Open the camera feed
    while True:
        success, frame = cap.read()  # Capture frame by frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')  # Home page template

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
