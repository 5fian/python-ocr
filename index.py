import ocr
from flask import Flask, render_template, request, redirect, url_for, send_file, make_response
import os
from pprint import pprint

app = Flask(__name__)

@app.route('/')
def index():
    threshold = 0
    if request.args.get('tval') :
        threshold = int(request.args.get('tval'))

    image_path = "contoh.jpg"
    binarize_image_path = "binarize.png"
    fileExists = os.path.isfile(image_path)
    retu = ""
    if fileExists and threshold:
        ocrLib = ocr.ocr(image_path, threshold)
        retu = ocrLib.image_to_text()
    elif fileExists:
        os.remove(image_path)
        os.remove(binarize_image_path)

    retu = retu.split('\n')
    return render_template('index.html', text=retu, imgExists=fileExists, tval=threshold)

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    thresholdVal = 0
    if request.method == 'POST':
        file = request.files['inputFile']
        file.save(os.getcwd() + '/contoh.jpg')
        thresholdVal = request.form['threshold']

    return redirect(url_for('index', tval=[thresholdVal]))

@app.route('/get-image', methods=['GET'])
def getImage():
    image_path = "contoh.jpg"
    print(bool(request.args.get('binarize')))
    if request.args.get('binarize'):
        image_path = "binarize.png"

    fileExists = os.path.isfile(image_path)
    if fileExists:
        return send_file(image_path, mimetype="image/jpg")

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__ == '__main__':
    app.run()
