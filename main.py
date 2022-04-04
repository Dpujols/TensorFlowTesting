from werkzeug.utils import secure_filename
import os
import ImageHandler as Pictures
from flask import Flask, render_template, request, Response

app = Flask(__name__, template_folder='templates')

UPLOAD_FOLDER = 'images/'

app.config['SERVER_NAME']="172.18.79.246:8000"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ImageDetector, LabelList = Pictures.PrepareSystem(False)
VideoDetector, LabelList = Pictures.PrepareSystem(True)

def BeginImageDetection(FilePath):
    Image = Pictures.ImageDetection(FilePath, ImageDetector, LabelList)
    DetectedPath = "static/Processed.jpeg"
    ScannedPath = Pictures.cv2.imwrite(DetectedPath, Image)
    if ScannedPath:
        return DetectedPath

@app.route('/VideoDetection', methods=['GET', 'POST'])
def BeginVideoDetection():
    try:
        UserStream = request.stream['UserFeed']
    except:
        UserStream = False
    if UserStream:
        CVid = UserStream
    else:
        CVid = Pictures.cv2.VideoCapture(-1)
        CVid.set(Pictures.cv2.CAP_PROP_FRAME_HEIGHT, 720)
        CVid.set(Pictures.cv2.CAP_PROP_FRAME_WIDTH, 1280)


    while True:
        VStream = Pictures.VideoDetection(CVid, VideoDetector, LabelList)
        ret, Buffer = Pictures.cv2.imencode('.jpg', VStream)
        Image = Buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + Image + b'\r\n')
        if Pictures.cv2.waitKey(1) & 0xFF == ord('q'):
            CVid.release()
            Pictures.cv2.destroyAllWindows()
            break

@app.route('/video_feed')
def video_feed():
    return Response(BeginVideoDetection(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/VideoDetector.html') #This line including videofeed() and Videodetector.html are not mine
def BeginRender():
    return render_template('VideoDetector.html')

@app.route('/upload', methods=['GET', 'POST'])
def FileUpload():
    Image = request.files['uFile']
    UploadName = secure_filename(Image.filename)
    Image.save(os.path.join(app.config['UPLOAD_FOLDER'], UploadName))
    FPath = app.config['UPLOAD_FOLDER'] + UploadName
    ModifiedImage = BeginImageDetection(FPath)
    ModifiedImage = "<img src=\"" + ModifiedImage + "\">"
    return render_template("ImageDetector.html", FData=ModifiedImage)

@app.route('/')
def HomePage():
    return render_template("Home.html")

if __name__ == '__main__':
    port = 8000
    app.run(debug=True, host='0.0.0.0', port=port)
