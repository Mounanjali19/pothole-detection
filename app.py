import requests
import os
import json
import datetime
from ultralytics import YOLO
from werkzeug.utils import secure_filename
import requests

from flask import Flask, render_template, request

app = Flask(__name__)


#PYTHON FUNCTIONS:
model = YOLO('best.pt')

def get_geolocation():
        try:
            res= requests.get("https://ipinfo.io")
            data=res.json()
            city=data['city']
            print(city)
            location = data['loc'].split(',')
            latitude = float(location[0])
            longitude = float(location[1])
            return city,latitude,longitude
        except Exception as e:
            print(f"Error getting geolocation: {e}")
            return None, None,None


def detect(image):
    results = model.predict(source=image, save=True, project='static/output_images', name='predictions', exist_ok=True)
    severity = 0
    for r in results:
        for box in r.boxes:
            severity = severity + 1
    return severity


UPLOAD_FOLDER = 'inputs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/',methods=['GET','POST'])
@app.route('/uploader',methods=['GET','POST'])
def uploader():
    filename = None
    if request.method=='POST':
        file =  request.files['file']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            severity = detect(filepath)
            _,latitude,longitude = get_geolocation()
            time = datetime.datetime.now()
            output_path = '/' + os.path.join('static', 'output_images', 'predictions', filename).replace(os.sep, '/')



            json_data = {
                "input_image" : filepath,
                "severity" : severity,
                "time" : str(time),
                "output_image" : output_path,
                "longitude" : longitude, 
                "latitude": latitude
            }

            

            data_file = os.path.join('static', 'pothole_data.json')
            if not os.path.exists(data_file):
                with open(data_file,'w') as f:
                    json.dump([json_data],f,indent=4)
            else:
                with open(data_file,'r') as f:
                    data = json.load(f)
                data.append(json_data)
                with open(data_file,'w') as file: 
                    json.dump(data,file)


    return render_template('uploader.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/output')
def output():
    
    with open(data_file,'r') as f:
        data = json.load(f)
    
    image = data[-1].get("output_image")
    return render_template('output.html',image=image)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
